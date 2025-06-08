from server.services.csv_manager.convert_author_pdfs_to_features import process_author
from server.services.csv_manager.config import BASE_PATH, AUTHORS

def main():
    for author in AUTHORS:
        try:
            process_author(author, BASE_PATH)
        except Exception as e:
            print(f"Error processing author {author}: {e}")
    print("Feature extraction completed!")

main()
