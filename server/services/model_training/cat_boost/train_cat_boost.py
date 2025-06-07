import pandas as pd
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

# הפרדת מאפיינים ותוויות
def split_features_and_labels(data: pd.DataFrame):
    X = data.drop('author', axis=1)
    y = data['author']
    return X, y

# פיצול לאימון ובדיקה
def split_train_test(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

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
    data = load_and_label_data(csv_paths)
    X, y = split_features_and_labels(data)
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    model = train_catboost_classifier(X_train, y_train)
    evaluate_model_performance(model, X_train, y_train, X_test, y_test)
    save_trained_model(model, model_output_path)
