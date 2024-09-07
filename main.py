from search.knn_matcher import KNNMatcher
from search.database import ProductDatabase
from search.config import DB_PATH

def main():
    db = ProductDatabase(DB_PATH)
    matcher = KNNMatcher()

    # Load products from the database and fit the model
    products = db.fetch_all_products()
    product_ids, embeddings = zip(*products)
    matcher.fit_model(np.array(embeddings))

    # Match a new image
    new_image_path = 'predict/new_image.jpg'
    distances, indices = matcher.match_new_image(new_image_path)

    matched_product_ids = [product_ids[i] for i in indices[0]]
    print("Matched Product IDs:", matched_product_ids)

if __name__ == "__main__":
    main()
