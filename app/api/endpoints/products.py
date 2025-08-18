# app/api/endpoints/products.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import cloudinary.uploader
from PIL import Image
import io
import os

# Import the Beanie Document model and Pydantic schemas
from app.models.product import Product
from app.schema.product import ProductUpdate, ProductCreate, ProductResponse # You should move schemas here

router = APIRouter()

def compress_image(image_file: UploadFile, max_size_kb: int = 200) -> bytes:
    """
    Compress an image to a maximum file size while maintaining quality.
    
    Args:
        image_file: The uploaded image file
        max_size_mb: Maximum file size in MB (default: 0.75MB)
    
    Returns:
        Compressed image as bytes
    """
    # Read the image
    image_data = image_file.file.read()
    image_file.file.seek(0)  # Reset file pointer for potential reuse
    
    # Open image with PIL
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB if necessary (for JPEG compatibility)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Start with a high quality and progressively reduce
    quality = 90
    output = io.BytesIO()

    # Progressive compression: reduce quality first, then downscale if needed
    attempts = 0
    min_side_limit = 256  # do not downscale below this on the shortest side
    while True:
        attempts += 1
        if attempts > 30:
            break  # safety guard

        output.seek(0)
        output.truncate()
        image.save(output, format='JPEG', quality=quality, optimize=True)

        file_size_kb = len(output.getvalue()) // 1024
        if file_size_kb <= max_size_kb:
            break

        # Reduce quality until 40, then start downscaling dimensions
        if quality > 40:
            quality -= 5
            continue

        # Downscale dimensions by 10% steps if still too large
        new_width = int(image.width * 0.9)
        new_height = int(image.height * 0.9)
        if min(new_width, new_height) <= min_side_limit:
            # As a last resort, allow quality to go down to 10
            if quality > 10:
                quality -= 5
                continue
            else:
                break
        image = image.resize((new_width, new_height), Image.LANCZOS)
    
    return output.getvalue()

@router.post("/products", response_model=Product, tags=["Products"])
async def add_product(
    name: str = Form(...),
    price: float = Form(...),
    location: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    images: List[UploadFile] = File(...)
):
    """
    Add a new product. Images are compressed and uploaded to Cloudinary.
    """
    image_urls = []
    
    for img in images:
        # Compress the image to max 200KB
        compressed_image_data = compress_image(img, max_size_kb=200)
        
        # Upload compressed image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            io.BytesIO(compressed_image_data),
            resource_type="image"
        )
        image_urls.append(upload_result["url"])

    product_data = ProductCreate(
        name=name,
        price=price,
        location=location,
        category=category,
        description=description
    )

    new_product = Product(
        **product_data.dict(),
        image_urls=image_urls,
        seller_id="000000000000000000000000" # Placeholder for auth user (24-char ObjectId)
    )

    await new_product.insert()
    return new_product

@router.get("/products", response_model=List[ProductResponse], tags=["Products"])
async def get_home_feed():
    """
    Get the home feed of all products.
    """
    products = await Product.find_all().to_list()
    return [ProductResponse.model_validate(p, from_attributes=True) for p in products]

@router.get("/products/{id}", response_model=ProductResponse, tags=["Products"])
async def view_product(id: str):
    """
    View a single product by its ID.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse.model_validate(product, from_attributes=True)

@router.put("/products/{id}", response_model=ProductResponse, tags=["Products"])
async def edit_product(id: str, product_update: ProductUpdate):
    """
    Edit a product's details.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    await product.save()
    
    return ProductResponse.model_validate(product, from_attributes=True)

@router.delete("/products/{id}", status_code=204, tags=["Products"])
async def delete_product(id: str):
    """
    Delete a product.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await product.delete()
    # You should also delete images from Cloudinary here
    return None

@router.patch("/products/{id}/sold", response_model=ProductResponse, tags=["Products"])
async def mark_as_sold(id: str):
    """
    Mark a product as sold.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_sold = True
    await product.save()
    
    return ProductResponse.model_validate(product, from_attributes=True)