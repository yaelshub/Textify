import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from scipy.sparse import hstack
import matplotlib.pyplot as plt
import xgboost as xgb

def split_train_test_stratified_books(X, y, book_names, test_size=0.2, random_state=42):
    
    # יצירת טבלה עם מידע על ספרים
    df_books = pd.DataFrame({
        'author': y,
        'book_name': book_names
    }).drop_duplicates()
    
    # ספירת ספרים לכל מחבר
    books_per_author = df_books.groupby('author')['book_name'].count()
    
    # חישוב כמה ספרים לבדיקה לכל מחבר
    train_books = []
    test_books = []
    
    for author in books_per_author.index:
        author_books = df_books[df_books['author'] == author]['book_name'].tolist()
        n_books = len(author_books)
        n_test = max(1, int(n_books * test_size))
                
        # בחירה אקראית של ספרים לטסט
        np.random.seed(random_state)
        test_books_for_author = np.random.choice(author_books, size=n_test, replace=False)
        train_books_for_author = [book for book in author_books if book not in test_books_for_author]
        
        train_books.extend(train_books_for_author)
        test_books.extend(test_books_for_author)
    
    # יצירת מסכות לפיצול
    train_mask = book_names.isin(train_books)
    test_mask = book_names.isin(test_books)
    
    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]

    return X_train, X_test, y_train, y_test

csv_paths = {
    'Charles Dickens': 'data/Charles Dickens.csv',
    'H. G. Wells': 'data/H. G. Wells.csv',
    'Jane Austen': 'data/Jane Austen.csv',
    'Mark Twain': 'data/Mark Twain.csv'
}

# פונקציה לטעינת הקבצים והוספת עמודת author
def load_and_label_data(csv_paths: dict) -> pd.DataFrame:
    dataframes = []
    for author, path in csv_paths.items():
        df = pd.read_csv(path)
        df['author'] = author
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

df = load_and_label_data(csv_paths)

book_col = 'book' if 'book' in df.columns else 'book_name'
if book_col not in df.columns:
    exit()

vectorizer = TfidfVectorizer(max_features=500)
X_tfidf = vectorizer.fit_transform(df['text'])

features_df = df.drop(columns=['text', 'author', book_col])
features_df = features_df.select_dtypes(include=['number'])

X_combined = hstack([X_tfidf, features_df.values])

y = df['author']
book_names = df[book_col]


X_train, X_test, y_train, y_test = split_train_test_stratified_books(
    X_combined, y, book_names, test_size=0.2, random_state=42
)

model = xgb.XGBClassifier(
    use_label_encoder=False,
    eval_metric='mlogloss',
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred, labels=np.unique(y))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))
disp.plot(cmap=plt.cm.Blues)
plt.show()