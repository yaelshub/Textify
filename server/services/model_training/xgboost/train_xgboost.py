# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
# from scipy.sparse import hstack
# import matplotlib.pyplot as plt
# import xgboost as xgb
# csv_paths = {
#     'Charles Dickens': 'data/Charles Dickens.csv',
#     'H. G. Wells': 'data/H. G. Wells.csv',
#     'Jane Austen': 'data/Jane Austen.csv',
#     'Mark Twain': 'data/Mark Twain.csv'
# }

# # פונקציה לטעינת הקבצים והוספת עמודת author
# def load_and_label_data(csv_paths: dict) -> pd.DataFrame:
#     dataframes = []
#     for author, path in csv_paths.items():
#         df = pd.read_csv(path)
#         df['author'] = author
#         dataframes.append(df)
#     return pd.concat(dataframes, ignore_index=True)

# # שלב 1: טען את הדאטה
# df = load_and_label_data(csv_paths)

# # שלב 2: יצירת TF-IDF מהעמודה 'text'
# vectorizer = TfidfVectorizer(max_features=500)
# X_tfidf = vectorizer.fit_transform(df['text'])

# # שלב 3: חילוץ תכונות מספריות בלבד
# features_df = df.drop(columns=['text', 'author'])
# features_df = features_df.select_dtypes(include=['number'])

# # שלב 4: שילוב כל הפיצ'רים
# X_combined = hstack([X_tfidf, features_df.values])

# # שלב 5: תוויות
# y = df['author']

# # שלב 6: Train/Test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X_combined, y, test_size=0.2, stratify=y, random_state=42
# )

# # שלב 7: אימון מודל XGBoost
# model = xgb.XGBClassifier(
#     use_label_encoder=False,
#     eval_metric='mlogloss',
#     random_state=42
# )
# model.fit(X_train, y_train)

# # שלב 8: ניבוי ותצוגת תוצאות
# y_pred = model.predict(X_test)

# print("=== Classification Report ===")
# print(classification_report(y_test, y_pred))

# print("=== Confusion Matrix ===")
# cm = confusion_matrix(y_test, y_pred, labels=np.unique(y))
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))
# disp.plot(cmap=plt.cm.Blues)
# plt.show()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from scipy.sparse import hstack
import matplotlib.pyplot as plt
import xgboost as xgb

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
    
    # פיצול הנתונים - שמירה על sparse matrix
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
    print(f"אימון: {len(y_train)} פרקים מ-{len(train_books)} ספרים")
    print(f"בדיקה: {len(y_test)} פרקים מ-{len(test_books)} ספרים")
    
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

# שלב 1: טען את הדאטה
df = load_and_label_data(csv_paths)

# 🎯 בדיקה שיש עמודת book
book_col = 'book' if 'book' in df.columns else 'book_name'
if book_col not in df.columns:
    print("⚠️ שגיאה: חסרה עמודת book או book_name!")
    print("עמודות קיימות:", df.columns.tolist())
    exit()

# שלב 2: יצירת TF-IDF מהעמודה 'text'
vectorizer = TfidfVectorizer(max_features=500)
X_tfidf = vectorizer.fit_transform(df['text'])

# שלב 3: חילוץ תכונות מספריות בלבד
# 🎯 הסר גם author וגם book/book_name
features_df = df.drop(columns=['text', 'author', book_col])
features_df = features_df.select_dtypes(include=['number'])

# שלב 4: שילוב כל הפיצ'רים
X_combined = hstack([X_tfidf, features_df.values])

# שלב 5: תוויות ושמות ספרים
y = df['author']
book_names = df[book_col]

# שלב 6: Train/Test split החדש
# 🎯 השתמש בפיצול החדש במקום train_test_split
X_train, X_test, y_train, y_test = split_train_test_stratified_books(
    X_combined, y, book_names, test_size=0.2, random_state=42
)

# שלב 7: אימון מודל XGBoost
model = xgb.XGBClassifier(
    use_label_encoder=False,
    eval_metric='mlogloss',
    random_state=42
)
model.fit(X_train, y_train)

# שלב 8: ניבוי ותצוגת תוצאות
y_pred = model.predict(X_test)

print("=== Classification Report ===")
print(classification_report(y_test, y_pred))

print("=== Confusion Matrix ===")
cm = confusion_matrix(y_test, y_pred, labels=np.unique(y))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))
disp.plot(cmap=plt.cm.Blues)
plt.show()