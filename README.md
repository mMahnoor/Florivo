# 🌸 Florivo Backend – Flower Marketplace API

**Florivo** is a backend system for an online flower marketplace, built with **Django** and **Django REST Framework (DRF)**.  
It provides all the essential APIs for buying and selling flowers, user authentication, order management, and admin controls — forming the backbone of a future full-stack flower-selling platform.

---

## 🌼 Project Overview

The Florivo backend is designed to power a vibrant flower marketplace where:

- 🌷 Users can browse and purchase flowers.
- 🌺 Sellers and admins can manage listings and orders.
- 🌻 The system automatically handles order placement, email notifications, and account verification.

This backend serves as the foundation for future integration with a web or mobile frontend and a payment gateway.

---

## ⚙️ Features Implemented

### 1. Catalog

- API endpoints for listing flowers (image, name, description, price, and category).
- “Buy Now” functionality handled via order creation endpoint.
- Filtering flowers by category through query parameters.

### 2. User Registration and Authentication

- Registration, login, and logout APIs using Django’s authentication system and DRF tokens.
- Email verification upon registration — accounts activate after clicking the verification link.

### 3. Placing Orders

- Authenticated users can place orders for flowers.
- After placing an order:
  - Confirmation email sent to user.
  - Flower quantity reduced accordingly.
  - Order status set to **“Pending”**.

### 4. Order History

- Users can view their past orders via API.
- Each order shows its current status (**Pending / Delivered**).

### 5. Admin Dashboard

- Implemented using Django’s built-in **Admin Interface**.
- Admins can:
  - Add, edit, or delete flower listings.
  - View and manage all user orders.

### 6. Order Management

- Admins can update order statuses (e.g., “Pending” → “Ready To Deliver”).
- Status update emails automatically sent to users.
- Updated status reflected in user order history.

### 7. Future Payment Gateway Integration _(Placeholder)_

- Ready for future integration with **Stripe** or **PayPal**.

---

## 🧩 Tech Stack

| Component      | Technology                       |
| -------------- | -------------------------------- |
| Framework      | Django 5.x                       |
| API Layer      | Django REST Framework (DRF)      |
| Database       | PostgreSQL (hosted on Supabase)  |
| Authentication | Django Auth + Email Verification |
| Email Service  | Django SMTP Backend              |
| Deployment     | Vercel                           |

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/mmahnoor/florivo-backend.git
cd florivo-backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set Up Environment Variables

Create a `.env` file in the project root directory and include:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_supabase_database_url
EMAIL_HOST=smtp.yourmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Your backend should now be running at:
👉 http://127.0.0.1:8000

## 📡 API Endpoints Overview

| Endpoint              | Method      | Description                  |
| --------------------- | ----------- | ---------------------------- |
| `/api/flowers/`       | GET         | List all flowers             |
| `/api/flowers/<id>/`  | GET         | Retrieve a specific flower   |
| `/api/orders/`        | POST        | Place an order               |
| `/api/orders/`        | GET         | View user’s order history    |
| `/api/auth/register/` | POST        | Register a new user          |
| `/api/auth/login/`    | POST        | Log in user                  |
| `/api/auth/logout/`   | POST        | Log out user                 |
| `/api/admin/orders/`  | GET / PATCH | Manage orders _(admin only)_ |

## 🗃️ Database Schema (Simplified)

### Flower

| Field       | Type      |
| ----------- | --------- |
| id          | Integer   |
| name        | String    |
| category    | String    |
| description | Text      |
| price       | Decimal   |
| quantity    | Integer   |
| image       | URL/Image |

### Orders

| Field      | Type                                |
| ---------- | ----------------------------------- |
| id         | Integer                             |
| user       | ForeignKey (User)                   |
| flower     | ForeignKey (Flower)                 |
| status     | ChoiceField _(Pending / Delivered)_ |
| created_at | DateTime                            |

### Users

| Field       | Type          |
| ----------- | ------------- |
| id          | Integer       |
| username    | String        |
| email       | Email         |
| is_verified | Boolean       |
| password    | Hashed String |

## 📬 Email Notifications

Handled through Django’s SMTP backend for:

✉️ Account verification

🧾 Order confirmation

🚚 Order completion updates

## 🧱 Deployment

Database: Supabase (PostgreSQL)

Backend: Deployed on Vercel

## ➡️ Next Steps

Implement frontend using React or Django Templates

Integrate payment gateway (Stripe / PayPal)

Add user reviews and ratings

Enhance admin dashboard UI

## 🪴 License

This project is licensed under the MIT License — free to use, modify, and distribute with attribution.

## 👤 Author

Florivo Backend developed by Mahnur Akther
A Django-based project for a modern flower marketplace 🌸
