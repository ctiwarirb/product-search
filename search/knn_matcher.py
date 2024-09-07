import numpy as np
from sklearn.neighbors import NearestNeighbors
from search.image_utils import extract_embedding
from search.logger import logger
from search.database import ProductDatabase

class KNNMatcher:
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.knn_model = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto')

    def fit_model(self, embeddings):
        self.knn_model.fit(embeddings)
        logger.info("KNN model fitted with embeddings.")

    def match_new_image(self, new_image_path):
        embedding = extract_embedding(new_image_path)
        embedding = np.array(embedding).reshape(1, -1)

        distances, indices = self.knn_model.kneighbors(embedding, n_neighbors=1)
        logger.info(f"Found {self.n_neighbors} similar products.")
        return distances, indices
