# Josmee Online Shopping - Installation Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Step 1: Clone or Extract Project
\`\`\`bash
cd josmee_projects
\`\`\`

### Step 2: Create Virtual Environment
\`\`\`bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
\`\`\`

### Step 3: Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 4: Database Setup
\`\`\`bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Setup initial data
python scripts/setup_complete_database.py
\`\`\`

### Step 5: Run Development Server
\`\`\`bash
python manage.py runserver
\`\`\`

Visit: **http://127.0.0.1:8000**

## 👥 Default Accounts

### Admin Account
- **URL**: http://127.0.0.1:8000/admin
- **Username**: `admin`
- **Password**: `admin123`

### Vendor Account
- **Username**: `vendor1`
- **Password**: `vendor123`

## ⚙️ Configuration

### Twilio OTP Setup (Optional)
Edit `josmee_projects/settings.py`:

\`\`\`python
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_FROM_NUMBER = '+1234567890'
\`\`\`

**Note**: OTP will print to console if Twilio isn't configured.

## 📦 Features

### For Sellers
1. Register as vendor
2. Complete 4-step registration
3. Upload products with images
4. Manage inventory
5. Track orders
6. View analytics

### For Buyers
1. Browse products
2. Search functionality
3. Add to cart
4. Place orders
5. Track deliveries
6. Leave reviews

### Admin Features
1. Manage all vendors
2. Approve/reject sellers
3. View all products
4. Manage categories
5. Edit hero sliders
6. Full database access

## 🎨 Design Features
- Modern creative warm color theme
- Fully responsive mobile design
- WhatsApp integration
- Search functionality
- Admin-controlled hero slider
- Product image gallery
- Meesho-style category cards

## 🔧 Troubleshooting

### Issue: Module not found
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Issue: Database errors
\`\`\`bash
python manage.py migrate --run-syncdb
\`\`\`

### Issue: Static files not loading
\`\`\`bash
python manage.py collectstatic
\`\`\`

## 📞 Support
- **Mobile**: 9442085847
- **Phone**: 04636 250411
- **Email**: devasindianfoods@gmail.com

## 🔐 Security Notes
- Change SECRET_KEY in production
- Set DEBUG = False in production
- Configure ALLOWED_HOSTS properly
- Use environment variables for sensitive data
\`\`\`

\`\`\`txt file="" isHidden
