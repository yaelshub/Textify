import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# טעינת קבצים,ואיחוד לטבלה אחת 
def load_and_label_data(csv_paths: dict) -> pd.DataFrame:
    dataframes = []
    for author, path in csv_paths.items():
        df = pd.read_csv(path)
        df['author'] = author
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# מפצל בין מאפיינים לתויות 
def split_features_and_labels(data: pd.DataFrame):
    X = data.drop('author', axis=1)
    y = data['author']
    return X, y

# פיצול נתונים לבדיקה ואימון
def split_train_test(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def train_random_forest_classifier(X_train, y_train, random_state=42):
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)
    return model

# מציג את דיוק המודל 
def evaluate_model_performance(model, X_train, y_train, X_test, y_test):
    print("accuracy on the training set:", model.score(X_train, y_train))
    print("accuracy on the test set:", model.score(X_test, y_test))

    y_pred = model.predict(X_test)

    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))


def save_trained_model(model, model_output_path: str):
    joblib.dump(model, model_output_path)
    print(f"Histogram graph {model_output_path}")


def train_author_classifier(csv_paths: dict, model_output_path: str = 'author_identifier_model.pkl'):
    # טעינת הנתונים ואיחוד
    data = load_and_label_data(csv_paths)
    # פיצול ל-X ו-y
    X, y = split_features_and_labels(data)
    # פיצול לסט אימון וסט בדיקה
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    # אימון המודל
    model = train_random_forest_classifier(X_train, y_train)
    # הערכת ביצועים
    evaluate_model_performance(model, X_train, y_train, X_test, y_test)
    # שמירת המודל
    save_trained_model(model, model_output_path)


# הרצה בפועל עם קבצי CSV
csv_files = {
    'Charles Dickens': 'data/Charles Dickens.csv',
    'H. G. Wells': 'data/H. G. Wells.csv',
    'Jane Austen': 'data/Jane Austen.csv',
    'Mark Twain': 'data/Mark Twain.csv'
}

train_author_classifier(csv_files)
