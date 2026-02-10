# Smart Product Recommendation & Customer Intelligence System
## 📌 Project Overview

This project is an end-to-end backend + machine learning system that simulates a real e-commerce recommendation engine.

The system:

* manages users and products
* tracks user behavior (views, cart, purchases)
* stores interaction data
* prepares data for recommendation models
* generates product recommendations

This project is built to understand how real production recommender systems work.


## 🧱 Tech Stack
**Backend**

* Python
* Flask
* SQLite
**Data & ML**

* Pandas
* RetailRocket dataset

**Frontend (basic)**
* HTML
* CSS

## ⚙️ Features Implemented

### Backend

* User registration & login
* Database integration
* Product storage
* Interaction tracking

### Interaction Tracking stores:

* product views
* add to cart
* purchases
* timestamps

This data will be used to train recommendation models.

## 📊 Dataset Used

RetailRocket Recommender Dataset:

* events.csv → user interactions
* category_tree.csv → product categories
* item_properties_part1.csv
* item_properties_part2.csv

Currently using a subset (~3000 rows) for development and testing.

## 🧠 Recommendation System Plan

Phase 1:

* Popularity-based recommendation

Phase 2:

* Collaborative filtering

Phase 3:

* Hybrid recommendation (behavior + product features)

## 📌 Future Improvements

* Password hashing
* Session-based authentication
* Dynamic product loading
* Model training pipeline
* API-based recommendation service
* Deployment

## 🎯 Goal

To build a production-style backend system that connects:

User → Behavior → Data → ML → Recommendations

This project focuses on understanding system design, backend development, and machine learning integration.
