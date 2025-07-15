import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def train_personification_model():
    df = pd.read_csv("data.csv")
    X = df["sentence"]
    y = df["label"]
    
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))    
    X_vec = vectorizer.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy:", model.score(X_test, y_test))
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("y_test:", y_test.tolist())
    print("y_pred:", y_pred.tolist())
    print(df["label"].value_counts())
   
    joblib.dump(model, "personification_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
   
   