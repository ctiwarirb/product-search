# Image-Based Product Search Using ResNet50 and KNN with SQLite

This project implements an image-based product search system for a retailer. The system stores product images and their embeddings in an SQLite database and performs search queries by matching new product images to existing ones using ResNet50 for feature extraction and K-Nearest Neighbors (KNN) for matching.

## Features

- **ResNet50-based embedding creation**: Uses a pre-trained ResNet50 model to generate embeddings from product images.
- **KNN-based search**: Uses K-Nearest Neighbors (KNN) to find the closest product matches based on image embeddings.
- **SQLite database**: Product information and embeddings are stored in SQLite.
- **Supports multiple image formats**: Images can be in `.jpeg`, `.jpg`, `.webp`, or `.png` format.
- **Streamlit Frontend**: A web app interface for uploading and testing product images.

## Tech Stack

- **Python 3.11**
- **TensorFlow/Keras** for ResNet50 embedding creation
- **SQLite** for product data storage
- **scikit-learn** for KNN
- **Streamlit** for the web app frontend

## Project Structure

