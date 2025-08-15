import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { createProduct } from '../services/products';
import type { CreateProductData } from '../types/product';

export default function AddProduct() {
  const { state } = useAuth();
  const [formData, setFormData] = useState<Omit<CreateProductData, 'images' | 'location'>>({
    name: '',
    price: 0,
    category: '',
    description: '',
  });
  const [images, setImages] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'price' ? parseFloat(value) || 0 : value
    }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const fileArray = Array.from(e.target.files);
      setImages(fileArray);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      if (images.length === 0) {
        throw new Error('Please select at least one image');
      }

      const productData: CreateProductData = {
        ...formData,
        location: state.user?.hostel || '',
        images
      };

      const newProduct = await createProduct(productData);
      setSuccess(`Product "${newProduct.name}" created successfully!`);
      
      // Reset form
      setFormData({
        name: '',
        price: 0,
        category: '',
        description: '',
      });
      setImages([]);
      
      // Reset file input
      const fileInput = document.getElementById('images') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create product');
    } finally {
      setIsLoading(false);
    }
  };

  // Check if user has completed their profile
  const hasCompletedProfile = state.user?.gender && state.user?.hostel;
  
  if (!hasCompletedProfile) {
    return (
      <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Complete Your Profile First</h2>
        
        <div className="mb-4 p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded">
          <p className="font-medium mb-2">Profile Incomplete</p>
          <p className="text-sm">
            You need to set your gender and hostel before adding products. 
            Click on your profile in the header to complete your profile.
          </p>
        </div>
        
        <div className="text-center">
          <p className="text-gray-600 mb-4">
            Current Status:
          </p>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Gender:</span>
              <span className={state.user?.gender ? 'text-green-600 font-medium' : 'text-red-600'}>
                {state.user?.gender || 'Not set'}
              </span>
            </div>
            <div className="flex justify-between">
              <span>Hostel:</span>
              <span className={state.user?.hostel ? 'text-green-600 font-medium' : 'text-red-600'}>
                {state.user?.hostel || 'Not set'}
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Add New Product</h2>
      
      <div className="mb-4 p-3 bg-blue-100 border border-blue-400 text-blue-700 rounded">
        <p className="text-sm">
          <strong>Location:</strong> Your product will be listed in <strong>{state.user?.hostel}</strong>
        </p>
      </div>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Product Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label htmlFor="price" className="block text-sm font-medium text-gray-700 mb-1">
            Price *
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleInputChange}
            min="0"
            step="0.01"
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>



        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
            Category *
          </label>
          <select
            id="category"
            name="category"
            value={formData.category}
            onChange={handleInputChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a category</option>
            <option value="Electronics">Electronics</option>
            <option value="Books">Books</option>
            <option value="Clothing">Clothing</option>
            <option value="Furniture">Furniture</option>
            <option value="Sports">Sports</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label htmlFor="images" className="block text-sm font-medium text-gray-700 mb-1">
            Images *
          </label>
          <input
            type="file"
            id="images"
            name="images"
            onChange={handleImageChange}
            multiple
            accept="image/*"
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {images.length > 0 && (
            <p className="text-sm text-gray-600 mt-1">
              Selected {images.length} image(s)
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Creating Product...' : 'Add Product'}
        </button>
      </form>
    </div>
  );
} 