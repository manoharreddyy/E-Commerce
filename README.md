# 🛒 E-Commerce Gadgets Store – Flask Web Application

This is a full-stack **E-commerce web application** for selling electronic gadgets like smartphones, smartwatches, laptops, and more. The project is built using **Python Flask** on the backend and HTML/CSS for the frontend. It also includes payment integration using **Razorpay**.

---

## 🌟 Features

- 👤 User login & registration
- 🛍️ View products in a responsive grid layout
- 🛒 Add products to shopping cart
- 💳 Buy Now with Razorpay payment gateway
- 📦 Checkout and order confirmation
- 🔐 Secure form handling with POST methods
- 📱 Mobile-friendly design

---

## 🧰 Technologies Used

| Category    | Tools Used                     |
|-------------|--------------------------------|
| Frontend    | HTML5, CSS3, JavaScript        |
| Backend     | Python 3, Flask                |
| Database    | SQLite / MySQL (you choose)    |
| Payment     | Razorpay                       |
| Deployment  | Render / PythonAnywhere        |

---

## 📁 Project Structure

ecommerce-gadgets/
│
├── static/
│ ├── images/ # Product images
│ ├── css/ # Optional CSS files
│
├── templates/
│ ├── index.html # Home page
│ ├── products.html # Products listing
│ ├── cart.html # Shopping cart
│ └── login.html # Login page
│
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── Procfile # For deployment
└── README.md

2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Run the app
   python app.py


💳 Razorpay Payment Integration
Sign up at razorpay.com

Generate test API keys

In your HTML/JS, replace the key:
    key: "rzp_test_YourKeyHere"




