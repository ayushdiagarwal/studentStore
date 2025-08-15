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

## Interaction between user and seller.
- **Anonymous Listings**: No seller contact info shown initially.
- **Contact Reveal Flow**: Buyers send a request to the seller; seller approves before sharing contact.
- **Request Management**: Sellers can accept or decline requests.
- **Buyer Dashboard**: Buyers can see status of their requests and view contact info if approved.


## 🚀 TODO List

### �� **Authentication & User Management (HIGH PRIORITY)**
- [ ] Implement user registration and login system
- [x] Add JWT token authentication
- [ ] Create user profiles with student verification
- [ ] Add role-based access control (student, admin)

### 🛍️ **Product Management (MEDIUM PRIORITY)**
- [ ] My listing section
- [ ] My hostel section
- [ ] Pagination / lazy-loading
- [ ] Product search and filtering (by category, price, location, tags)
- [ ] Allow user to add multiples images while uploading a product.
- [ ] Product sorting (by date, price, popularity)
- [ ] Product favorites/wishlist functionality
- [ ] Product status tracking (available, reserved, sold)
- [ ] Product analytics (views, favorites, inquiries)

### 🔍 **Search & Discovery (MEDIUM PRIORITY)**
- [ ] Advanced search with filters (price range, location radius, category)
- [ ] fuzzy search
- [ ] Search suggestions and autocomplete
- [ ] Personalized product recommendations
- [ ] Trending products algorithm
- [ ] Search analytics and insights

### 📱 **Frontend Improvements (MEDIUM PRIORITY)**
- [ ] Responsive design for mobile devices
- [ ] Dark mode theme
- [ ] Product image gallery with zoom
- [ ] Infinite scroll for product lists
- [ ] Advanced filtering UI components

### 💬 **Communication & Messaging (LOW PRIORITY)**
- [ ] Real-time chat between buyers and sellers
- [ ] Product inquiry system
- [ ] Notification system (email, push notifications)
- [ ] Message history and archiving
- [ ] Chat moderation and spam protection 

### 📊 **Analytics & Reporting (LOW PRIORITY)**
- [ ] Admin dashboard with analytics
- [ ] Real-time statistics

### 🔒 **Security & Performance (HIGH PRIORITY)**
- [ ] Input validation and sanitization
- [ ] XSS protection
- [ ] CORS configuration optimization
- [ ] Database indexing optimization

### 🚀 **Deployment & DevOps (LOW PRIORITY)**
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Caching implementation (Redis)
- [ ] Environment configuration management
- [ ] Monitoring and logging (Prometheus, Grafana)
- [ ] Backup and recovery procedures
- [ ] Load balancing configuration
- [ ] SSL certificate setup

### 🧪 **Testing & Quality (LOW PRIORITY)**
- [ ] Unit tests for all endpoints
- [ ] Integration tests
- [ ] API endpoint testing
- [ ] Frontend component testing
- [ ] Performance testing
- [ ] Security testing
- [ ] Automated testing pipeline

### 📚 **Documentation & Onboarding (LOW PRIORITY)**
- [ ] API documentation with examples
- [ ] User manual and tutorials
- [ ] Developer setup guide
- [ ] Deployment guide
- [ ] Troubleshooting guide
- [ ] FAQ section

---

**Current Implementation Status:**
- ✅ Basic product CRUD operations
- ✅ Image upload and compression
- ✅ Cloudinary integration
- ✅ Basic frontend with React + TypeScript
- ✅ Product listing and creation forms
- ✅ MongoDB integration with Beanie ODM

**Next Steps:**
1. **Start with Authentication** - This is foundational for user-specific features
2. **Implement User Management** - Essential for personalization
3. **Add Search & Filtering** - Improves user experience significantly
4. **Enhance Frontend** - Better UI/UX and mobile responsiveness
5. **Add Security Features** - Protect against common vulnerabilities