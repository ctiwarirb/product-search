import sqlite3
import numpy as np
from search.logger import logger

class ProductDatabase:
    def __init__(self, db_path='product_search.db'):
        self.db_path = db_path
        self.conn = None
        

    def open_connection(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_path)
                logger.info("Database connection opened.")
            except sqlite3.Error as e:
                logger.error(f"Error opening connection: {e}")

    def create_table_if_not_exists(self):
        """Create the products table if it doesn't exist."""
        self.open_connection()
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                embedding BLOB NOT NULL
            )
        ''')
        self.conn.commit()
        self.close_connection()

    def delete_product(self, product_id):
        self.open_connection()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products WHERE product_id=?", (product_id,))
        self.conn.commit()
        logger.info(f"Deleted product {product_id} from the database.")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed.")

    def insert_product_with_embedding_if_not_exists(self, product_id, image_filename, embedding):
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO products (product_id, product_name, image_filename, embedding)
                VALUES (?, ?, ?, ?)
            ''', (product_id, f'Product {product_id}', image_filename, embedding))
            self.conn.commit()
            logger.info(f"Inserted product {product_id} into the database.")
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")

    def fetch_all_products(self):
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT product_id, product_name, image_filename, embedding FROM products")
            products = cursor.fetchall()
            return products
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")

  
    def get_all_embeddings(self):
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute('SELECT product_id, product_name, embedding FROM products')
            rows = cursor.fetchall()
            product_ids = []
            embeddings = []
            for row in rows:
                product_id, product_name, embedding_blob = row
                embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                product_ids.append((product_id, product_name))
                embeddings.append(embedding)
            return np.array(embeddings), product_ids
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
