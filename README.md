# Student Store API

A FastAPI application for a student marketplace with MongoDB integration.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `env.example` to `.env`
   - Update the values in `.env` with your actual configuration:
     - `DATABASE_URL`: Your MongoDB connection string
     - `CLOUDINARY_*`: Your Cloudinary credentials (for image uploads)

3. **Start MongoDB:**
   Make sure MongoDB is running on your system or use a cloud MongoDB instance.

## Running the Application

### Option 1: Using the run script
```bash
python run.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs:** http://localhost:8000/docs
- **ReDoc documentation:** http://localhost:8000/redoc

## API Endpoints

- `POST /api/v1/products` - Add a new product
- `GET /api/v1/products` - Get all products
- `GET /api/v1/products/{id}` - Get a specific product
- `PUT /api/v1/products/{id}` - Update a product
- `DELETE /api/v1/products/{id}` - Delete a product
- `PATCH /api/v1/products/{id}/sold` - Mark product as sold

## Project Structure

```
app/
├── api/
│   ├── endpoints/
│   │   └── products.py
│   └── api.py
├── core/
│   └── config.py
├── db/
│   └── session.py
├── models/
│   └── product.py
├── schema/
│   └── product.py
└── main.py
``` 