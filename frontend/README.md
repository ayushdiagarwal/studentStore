# Student Store Frontend

A React TypeScript frontend for the Student Store application.

## Features

- **Browse Products**: View all products in a responsive grid layout
- **Add Products**: Create new products with images and details
- **Tab Navigation**: Easy switching between browsing and adding products
- **Form validation** and error handling
- **Responsive design** with Tailwind CSS
- **TypeScript** for type safety
- **Real-time updates** with refresh functionality

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5173`

## Usage

### Browse Products Tab
- **Product Grid**: View all products in a responsive card layout
- **Product Cards**: Each card shows:
  - Product image (or placeholder if no image)
  - Product name and price
  - Description (if available)
  - Location and category
  - Date added
  - Tags (up to 3 shown)
  - Sold status indicator
- **Refresh Button**: Manually refresh the product list
- **Action Buttons**: View Details and Contact Seller (for available products)

### Add Product Tab
The form allows you to:

- **Product Name**: Enter the name of your product
- **Price**: Set the price (supports decimals)
- **Location**: Specify where the product is located
- **Category**: Choose from predefined categories
- **Description**: Optional detailed description
- **Images**: Upload multiple images (required)

### Navigation
- **Tab-based navigation** at the top of the page
- **Active tab highlighting** for better UX
- **Smooth transitions** between views

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api/v1`.

**API Endpoints Used:**
- `GET /api/v1/products` - Fetch all products
- `POST /api/v1/products` - Create new product

Make sure your backend is running before using the frontend.

## Project Structure

```
src/
├── components/
│   ├── AddProduct.tsx     # Product creation form
│   └── ProductList.tsx    # Product browsing grid
├── services/
│   └── products.ts        # API service functions
├── types/
│   └── product.ts         # TypeScript interfaces
├── App.tsx               # Main application with navigation
├── main.tsx             # Application entry point
└── index.css            # Tailwind CSS styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features in Detail

### Product List Features
- **Responsive Grid**: Adapts to different screen sizes
- **Loading States**: Spinner while fetching data
- **Error Handling**: User-friendly error messages with retry options
- **Empty States**: Helpful message when no products exist
- **Image Handling**: Graceful fallback for missing images
- **Price Formatting**: Proper currency formatting
- **Date Formatting**: Human-readable dates
- **Sold Status**: Visual indication for sold products

### Add Product Features
- **Form Validation**: Required field validation
- **File Upload**: Multiple image support
- **Success Feedback**: Confirmation messages
- **Form Reset**: Automatic form clearing after successful submission
- **Loading States**: Button states during submission
