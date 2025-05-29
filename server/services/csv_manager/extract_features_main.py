from author_processor import process_author
from config import BASE_PATH, AUTHORS

def main():
    for author in AUTHORS:
        try:
            process_author(author, BASE_PATH)
        except Exception as e:
            print(f"Error processing author {author}: {e}")
    print("Feature extraction completed!")

if __name__ == "__main__":
    main()
