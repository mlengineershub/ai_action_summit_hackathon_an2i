from workspace.src.db_utils import (
    get_database, 
    get_table 
)

def show_first_ten_entries(table_name: str = "Consultation") -> None:
    """
    Retrieve and display the first ten entries from the specified MongoDB collection.
    """
    # Get MongoDB client, database, and collection
    db = get_database()
    table = get_table(db, table_name)

    # Retrieve the first ten documents from the collection
    documents = table.find().limit(10)

    # Print the documents in a readable format
    print(f"First 10 entries from the '{table_name}' collection:")
    for i, doc in enumerate(documents, start=1):
        print(f"\nEntry {i}:")
        for key, value in doc.items():
            print(f"{key}: {value}")

# Example usage
if __name__ == "__main__":
    show_first_ten_entries()