import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib


def train_author_classifier(csv_paths: dict, model_output_path: str = 'author_identifier_model.pkl'):
    dataframes = []
    # קריאה ואיחוד הנתונים
    for author, path in csv_paths.items():
        df = pd.read_csv(path)
        df['author'] = author
        dataframes.append(df)
    
    # איחוד לטבלה אחת
    data = pd.concat(dataframes, ignore_index=True)

    # הפרדת מאפיינים (X) ותוויות (y)
    X = data.drop('author', axis=1)
    y = data['author']

    # פיצול לסט אימון ובדיקה
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # אימון המודל
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # הערכת דיוק לזיהוי overfitting
    print("דיוק על סט האימון:", model.score(X_train, y_train))
    print("דיוק על סט הבדיקה:", model.score(X_test, y_test))

    # חיזוי על סט הבדיקה
    y_pred = model.predict(X_test)

    # תוצאות
    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    # שמירת המודל
    joblib.dump(model, model_output_path)
    print(f"המודל נשמר בשם {model_output_path}")

csv_files = {
    'Charles Dickens': 'data/Charles Dickens.csv',
    'H. G. Wells': 'data/H. G. Wells.csv',
    'Jane Austen': 'data/Jane Austen.csv',
    'Mark Twain': 'data/Mark Twain.csv'
}

train_author_classifier(csv_files)