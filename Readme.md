# Smart Product Recommendation & Customer Intelligence System

## Project Overview

This project is an end-to-end backend and machine learning system that simulates a real-world e-commerce recommendation engine.

The system:

- manages users and products  
- tracks user interactions (view, cart, purchase)  
- stores behavioral data  
- processes data for recommendation models  
- generates personalized product recommendations  

The goal is to understand how real production recommendation systems are designed and implemented.

---

## Tech Stack

### Backend
- Python  
- Flask  
- SQLite  

### Data & Machine Learning
- Pandas  
- Scikit-learn  
- RetailRocket Dataset  

### Frontend
- HTML  
- CSS  
- JavaScript (for API calls)

---

## Features

### Backend
- User registration and login  
- Session-based authentication  
- Database integration  
- Product storage and retrieval  
- Interaction tracking API  

### Interaction Tracking
The system records:
- product views  
- add to cart actions  
- purchases  
- timestamps  

This data is used for building recommendation models.

---

## Recommendation System

The system implements multiple recommendation strategies:

### 1. Popular Products
- Based on total interaction count  

### 2. Trending Products
- Based on recent interactions (last 7 days)  

### 3. Collaborative Filtering
- Uses user-item interaction matrix  
- Computes similarity between users  
- Recommends products liked by similar users  

### 4. Content-Based Filtering
- Uses product categories  
- Recommends products from categories the user has interacted with  

### 5. Hybrid Recommendation
- Combines:
  - collaborative filtering  
  - content-based filtering  
  - trending products  
  - popular products  
- Handles cold-start users  

---

## Dataset

RetailRocket Recommender Dataset:

- `events.csv` → user interactions  
- `item_properties_part1.csv`  
- `item_properties_part2.csv`  

A subset of the dataset is used for development and testing.

---

## Project Structure
│
├── app.py # Flask application
├── database.py # Database setup and connection
├── recommender.py # Recommendation logic
├── ml_train.py # Data processing pipeline
├── models.py # Feature extraction
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── products.html
│
├── static/
│ └── style.css
│
├── data/ # Dataset files
└── users.db # SQLite database


---

## How It Works

1. User registers and logs in  
2. User interacts with products (view, cart, purchase)  
3. Interactions are stored in the database  
4. Recommendation engine processes user behavior  
5. System returns personalized recommendations  

---

## Future Improvements

- Password hashing (security improvement)  
- Better recommendation ranking (weighted hybrid model)  
- Real product details (name, price, images)  
- API optimization and caching  
- Deployment (Render / AWS / Docker)  

---

## Goal

To build a production-style system that connects:

User → Interaction → Data → Machine Learning → Recommendations

This project focuses on backend engineering, system design, and practical machine learning integration.
