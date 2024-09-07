import streamlit as st
import os
from PIL import Image
import io
from search.database import ProductDatabase
from search.knn_matcher import KNNMatcher
from search.image_utils import extract_embedding
import numpy as np

# Initialize the database and matcher
db = ProductDatabase()
matcher = KNNMatcher(n_neighbors=5)

# Streamlit app title
st.title("Image-Based Product Search")

# --- SECTION 1: Insert Products into the Database ---
st.header("Insert Product Images")
st.write("Upload up to 5 product images for insertion into the database.")

# Upload product images (up to 5 images)
uploaded_files = st.file_uploader("Choose up to 5 images", type=["jpeg", "jpg", "png", "webp"], accept_multiple_files=True, key="product_images")

if len(uploaded_files) > 5:
    st.warning("You can only upload a maximum of 5 images at a time.")
else:
    for file in uploaded_files:
        image = Image.open(file)
        image_filename = file.name
        
        # Extract product ID from the filename (without extension)
        product_id = os.path.splitext(image_filename)[0]
        

        # Convert image to embedding
        embedding = extract_embedding(file)
        embedding_blob = embedding.tobytes()

        # Insert into the database
        db.insert_product_with_embedding_if_not_exists(product_id, image_filename, embedding_blob)
        #print('fetching product-------\n',db.fetch_all_products())
        st.success(f"Inserted product {product_id} into the database.")

# --- SECTION 2: Test New Image for Product Matching ---
st.header("Test Product Search")
st.write("Upload a new image to find matching products in the database.")

# Upload a test image
test_image_file = st.file_uploader("Choose a test image", type=["jpeg", "jpg", "png", "webp"], key="test_image")

if test_image_file is not None:
    test_image = Image.open(test_image_file)
    test_image_path = test_image_file.name
    print(f'test_image_path===>>>>',test_image_path)
    
    # Retrieve all products from the database
    products = db.fetch_all_products()
    embeddings, product_ids = db.get_all_embeddings()

    # Fit the KNN model wi10691111960th embeddings
    matcher.fit_model(embeddings)

    # Match the new image
    distances, indices = matcher.match_new_image(test_image_file)

    # Display matched products
    st.write(f"Top 5 matched products for the test image:")
    matched_products = [product_ids[i] for i in indices[0]]

    for i, product_id in enumerate(matched_products):
        st.write(f"{i+1}. Product ID: {product_id} (Distance: {distances[0][i]:.4f})")

# --- SECTION 3: View Database Entries ---
st.header("View Products in the Database")
if st.button("Show Database Entries"):
    products = db.fetch_all_products()
    if products:
        st.write("Product ID", "Image Filename")
        for product in products:
            st.write(product[0], ' | ', product[1],' | ', product[2])
    else:
        st.write("No products found in the database.")

# --- SECTION 4: Delete a Product from the Database ---
st.header("Delete a Product")
product_id_to_delete = st.text_input("Enter Product ID to delete:")
if st.button("Delete Product"):
    if product_id_to_delete:
        db.delete_product(product_id_to_delete)
        st.success(f"Product {product_id_to_delete} has been deleted.")
    else:
        st.warning("Please enter a valid product ID.")
