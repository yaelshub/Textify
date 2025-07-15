import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def identifying_sentence_type():
    # טעינת הנתונים
    df = pd.read_csv("types_of_sentences.csv")
    X = df["sentence"]
    y = df["label"]

    # המרת טקסט לוקטור תכונות
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)

    # חלוקת הנתונים ל-Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    # אימון מודל Logistic Regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # תחזית ובדיקת דיוק
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("\nLabel distribution:\n", df["label"].value_counts())

    # שמירת המודל המאומן כאובייקט כפייתון 
    joblib.dump(model, "identifying_sentence_type.pkl")
    #שמירת הוקטורייזר- הדרך בה נהפכו המשפטים למספרים.
    joblib.dump(vectorizer, "vectorizer.pkl")
