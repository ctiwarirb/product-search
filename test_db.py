from search.database import ProductDatabase


def setup_database():
    db = ProductDatabase()
    db.create_table_if_not_exists()
    print("Product table created (if it didn't exist).")

if __name__ == "__main__":
    setup_database()