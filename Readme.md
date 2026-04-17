---
title: Smart Product Recommender
emoji: 🛍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "4.44.0"
python_version: "3.11"
app_file: app.py
pinned: false
---

# Smart Product Recommendation System

This project demonstrates a recommendation engine using user interaction data.

## Features

- Hybrid recommendation system
- Collaborative filtering
- Content-based filtering
- Trending & popular products

## How to Use

1. Enter a user ID
2. Get product recommendations

## Tech Stack

- Python
- Pandas
- Scikit-learn
- Gradio

## Vercel Deployment

This project is configured to deploy on Vercel using `vercel.json` and the Python runtime.

- `app.py` is served by Vercel's Python builder.
- `runtime.txt` is included to pin Python 3.11.
- Use Vercel Environment Variables for `SECRET_KEY`.
- For persistence, set `DATABASE_URL` to a hosted database; local SQLite on Vercel is ephemeral.

To deploy:
1. Install the Vercel CLI or use the Vercel dashboard.
2. Run `vercel` from the project root.
3. Set `SECRET_KEY` and optional `DATABASE_URL` in Vercel project settings.
4. If you use a hosted database, point `DATABASE_URL` to that service.

> Note: `data/` is ignored in deployment so the app bundle stays small. If your app relies on a separate dataset source in production, use an external storage solution.
