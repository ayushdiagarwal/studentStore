export interface Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  date_added: string;
  seller_id: string;
  image_urls: string[];
  location: string;
  category: string;
  tags?: string[];
  is_sold: boolean;
}

export interface CreateProductData {
  name: string;
  price: number;
  location: string;
  category: string;
  description?: string;
  images: File[];
} 