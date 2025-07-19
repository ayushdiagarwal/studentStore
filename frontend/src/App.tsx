import { useState } from 'react';
import AddProduct from './components/AddProduct';
import ProductList from './components/ProductList';

function App() {
  const [activeTab, setActiveTab] = useState<'products' | 'add'>('products');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            Student Store
          </h1>
          
          {/* Navigation Tabs */}
          <div className="flex space-x-1">
            <button
              onClick={() => setActiveTab('products')}
              className={`px-4 py-2 rounded-md font-medium transition-colors duration-200 ${
                activeTab === 'products'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Browse Products
            </button>
            <button
              onClick={() => setActiveTab('add')}
              className={`px-4 py-2 rounded-md font-medium transition-colors duration-200 ${
                activeTab === 'add'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Add Product
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="py-8">
        {activeTab === 'products' ? <ProductList /> : <AddProduct />}
      </div>
    </div>
  );
}

export default App;
