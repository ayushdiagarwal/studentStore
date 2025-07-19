import type { Product, CreateProductData } from '../types/product';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const createProduct = async (productData: CreateProductData): Promise<Product> => {
  const formData = new FormData();
  
  // Add text fields
  formData.append('name', productData.name);
  formData.append('price', productData.price.toString());
  formData.append('location', productData.location);
  formData.append('category', productData.category);
  
  if (productData.description) {
    formData.append('description', productData.description);
  }
  
  // Add image files
  productData.images.forEach((image) => {
    formData.append('images', image);
  });

  const response = await fetch(`${API_BASE_URL}/products`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Failed to create product: ${response.statusText}`);
  }

  return response.json();
};

export const getProducts = async (): Promise<Product[]> => {
  const response = await fetch(`${API_BASE_URL}/products`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch products: ${response.statusText}`);
  }

  return response.json();
};

export const getProduct = async (id: string): Promise<Product> => {
  const response = await fetch(`${API_BASE_URL}/products/${id}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch product: ${response.statusText}`);
  }

  return response.json();
}; 