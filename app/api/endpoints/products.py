# app/api/endpoints/products.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID
import cloudinary.uploader
from PIL import Image
import io
import os

# Import the Beanie Document model and Pydantic schemas
from app.models.product import Product
from app.schema.product import ProductUpdate, ProductCreate # You should move schemas here

router = APIRouter()

def compress_image(image_file: UploadFile, max_size_mb: float = 0.75) -> bytes:
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
    
    # Start with high quality
    quality = 95
    output = io.BytesIO()
    
    # Compress with decreasing quality until file size is under limit
    while True:
        output.seek(0)
        output.truncate()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        
        # Check file size
        file_size_mb = len(output.getvalue()) / (1024 * 1024)
        
        if file_size_mb <= max_size_mb or quality <= 10:
            break
        
        quality -= 5
    
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
        # Compress the image to max 0.75MB
        compressed_image_data = compress_image(img, max_size_mb=0.75)
        
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
        seller_id=UUID("00000000-0000-0000-0000-000000000000") # Placeholder for auth user
    )

    await new_product.insert()
    return new_product

@router.get("/products", response_model=List[Product], tags=["Products"])
async def get_home_feed():
    """
    Get the home feed of all products.
    """
    products = await Product.find_all().to_list()
    return products

@router.get("/products/{id}", response_model=Product, tags=["Products"])
async def view_product(id: UUID):
    """
    View a single product by its ID.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{id}", response_model=Product, tags=["Products"])
async def edit_product(id: UUID, product_update: ProductUpdate):
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
    return product

@router.delete("/products/{id}", status_code=204, tags=["Products"])
async def delete_product(id: UUID):
    """
    Delete a product.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await product.delete()
    # You should also delete images from Cloudinary here
    return None

@router.patch("/products/{id}/sold", response_model=Product, tags=["Products"])
async def mark_as_sold(id: UUID):
    """
    Mark a product as sold.
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_sold = True
    await product.save()
    return product