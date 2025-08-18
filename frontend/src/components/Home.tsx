import { useState } from 'react';
import AddProduct from './AddProduct';
import ProductList from './ProductList';

import LoginButton from './LoginButton';
import UserProfile from './UserProfile';
import DarkModeToggle from './DarkModeToggle';
import { useAuth } from '../contexts/AuthContext';

function Home() {
  const [activeTab, setActiveTab] = useState<'products' | 'add'>('products');
  const { state } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-200">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center mb-4 relative">
            <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
              Student Store
            </h1>
            
            {/* Authentication Section */}
            <div className="flex items-center space-x-4">
              <DarkModeToggle />
              {state.isAuthenticated ? (
                <UserProfile />
              ) : (
                <LoginButton />
              )}
            </div>
          </div>
          
          {/* Navigation Tabs - Only show if authenticated */}
          {state.isAuthenticated && (
            <div className="flex space-x-1">
              <button
                onClick={() => setActiveTab('products')}
                className={`px-4 py-2 rounded-md font-medium transition-colors duration-200 ${
                  activeTab === 'products'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                Browse Products
              </button>
              <button
                onClick={() => setActiveTab('add')}
                className={`px-4 py-2 rounded-md font-medium transition-colors duration-200 ${
                  activeTab === 'add'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                Add Product
              </button>

            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="py-8">
        {state.isLoading ? (
          <div className="flex justify-center items-center min-h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
            </div>
          </div>
        ) : state.isAuthenticated ? (
          activeTab === 'products' ? <ProductList /> :
          activeTab === 'add' ? <AddProduct /> :
          <ProductList />
        ) : (
          <div className="max-w-2xl mx-auto text-center">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Welcome to Student Store
              </h2>
              <p className="text-gray-600 mb-6">
                Sign in with your Google account to browse and add products to the student store.
              </p>
              <LoginButton />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home; 