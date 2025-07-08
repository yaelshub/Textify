import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from catboost import CatBoostClassifier, Pool
import joblib

# טעינת קבצים ואיחוד
def load_and_label_data(csv_paths: dict) -> pd.DataFrame:
    dataframes = []
    for author, path in csv_paths.items():
        df = pd.read_csv(path)
        df['author'] = author
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# # הפרדת מאפיינים ותוויות
# def split_features_and_labels(data: pd.DataFrame):
#     X = data.drop('author', axis=1)
#     y = data['author']
#     return X, y

# # פיצול לאימון ובדיקה
# def split_train_test(X, y, test_size=0.2, random_state=42):
#     return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


# 🎯 הוסף את הפונקציה החדשה
def split_train_test_stratified_books(X, y, book_names, test_size=0.2, random_state=42):
    """פיצול שמבטיח שכל מחבר יהיה גם באימון וגם בבדיקה"""
    
    print("=== פיצול מבוסס ספרים עם שימור מחברים ===")
    
    # יצירת טבלה עם מידע על ספרים
    df_books = pd.DataFrame({
        'author': y,
        'book_name': book_names
    }).drop_duplicates()
    
    # ספירת ספרים לכל מחבר
    books_per_author = df_books.groupby('author')['book_name'].count()
    print("ספרים לכל מחבר:")
    for author, count in books_per_author.items():
        print(f"  {author}: {count} ספרים")
    
    # חישוב כמה ספרים לבדיקה לכל מחבר
    train_books = []
    test_books = []
    
    for author in books_per_author.index:
        author_books = df_books[df_books['author'] == author]['book_name'].tolist()
        n_books = len(author_books)
        n_test = max(1, int(n_books * test_size))
        n_train = n_books - n_test
        
        print(f"{author}: {n_train} ספרים לאימון, {n_test} ספרים לבדיקה")
        
        # בחירה אקראית של ספרים לטסט
        np.random.seed(random_state)
        test_books_for_author = np.random.choice(author_books, size=n_test, replace=False)
        train_books_for_author = [book for book in author_books if book not in test_books_for_author]
        
        train_books.extend(train_books_for_author)
        test_books.extend(test_books_for_author)
    
    # יצירת מסכות לפיצול
    train_mask = book_names.isin(train_books)
    test_mask = book_names.isin(test_books)
    
    # פיצול הנתונים
    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    
    # בדיקות בטיחות
    print("\n=== בדיקת הפיצול ===")
    print(f"ספרי אימון: {sorted(train_books)}")
    print(f"ספרי בדיקה: {sorted(test_books)}")
    
    # ודא שכל מחבר מיוצג בשתי הקבוצות
    authors_train = set(y_train)
    authors_test = set(y_test)
    
    if authors_train == authors_test == set(y.unique()):
        print("✅ כל המחברים מיוצגים גם באימון וגם בבדיקה!")
    else:
        print("⚠️ בעיה: לא כל המחברים מיוצגים בשתי הקבוצות")
        print(f"באימון: {authors_train}")
        print(f"בבדיקה: {authors_test}")
    
    # ודא שאין חפיפת ספרים
    overlap = set(train_books) & set(test_books)
    if overlap:
        print(f"⚠️ חפיפת ספרים: {overlap}")
    else:
        print("✅ אין חפיפת ספרים!")
    
    print(f"\nתוצאה סופית:")
    print(f"אימון: {len(X_train)} פרקים מ-{len(train_books)} ספרים")
    print(f"בדיקה: {len(X_test)} פרקים מ-{len(test_books)} ספרים")
    
    return X_train, X_test, y_train, y_test

def train_catboost_classifier(X_train, y_train, random_state=42):
    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.1,
        depth=6,
        random_seed=random_state,
        verbose=0  # מונע הדפסות מיותרות
    )
    model.fit(X_train, y_train)
    return model

# הערכת ביצועים
def evaluate_model_performance(model, X_train, y_train, X_test, y_test):
    print("accuracy on the training set:", model.score(X_train, y_train))
    print("accuracy on the test set:", model.score(X_test, y_test))

    y_pred = model.predict(X_test)

    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

# שמירת המודל המאומן
def save_trained_model(model, model_output_path: str):
    joblib.dump(model, model_output_path)
    print(f"Model saved to {model_output_path}")

# פונקציית ריצה מלאה
def train_author_classifier_catboost(csv_paths: dict, model_output_path: str = 'author_identifier_catboost_model.pkl'):
     # טעינת נתונים
    data = load_and_label_data(csv_paths)
    
    # 🎯 בדיקה שיש עמודת book
    book_col = 'book' if 'book' in data.columns else 'book_name'
    if book_col not in data.columns:
        print("⚠️ שגיאה: חסרה עמודת book או book_name!")
        print("עמודות קיימות:", data.columns.tolist())
        return
    
    # 🎯 פיצול נכון - הסר author ו-book
    X = data.drop(['author', book_col], axis=1)
    y = data['author']
    book_names = data[book_col]
    
    # 🎯 השתמש בפיצול החדש
    X_train, X_test, y_train, y_test = split_train_test_stratified_books(X, y, book_names)
    
    # אימון המודל
    model = train_catboost_classifier(X_train, y_train)
    
    # הערכה ושמירה
    evaluate_model_performance(model, X_train, y_train, X_test, y_test)
    save_trained_model(model, model_output_path)
