import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from scipy.sparse import hstack
import matplotlib.pyplot as plt
import xgboost as xgb
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

# שלב 2: יצירת TF-IDF מהעמודה 'text'
vectorizer = TfidfVectorizer(max_features=500)
X_tfidf = vectorizer.fit_transform(df['text'])

# שלב 3: חילוץ תכונות מספריות בלבד
features_df = df.drop(columns=['text', 'author'])
features_df = features_df.select_dtypes(include=['number'])

# שלב 4: שילוב כל הפיצ'רים
X_combined = hstack([X_tfidf, features_df.values])

# שלב 5: תוויות
y = df['author']

# שלב 6: Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_combined, y, test_size=0.2, stratify=y, random_state=42
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
