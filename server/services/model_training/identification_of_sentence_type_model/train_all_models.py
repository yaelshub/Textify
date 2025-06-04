import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier
from sklearn.utils import shuffle
from xgboost import XGBClassifier
import joblib

# טעינת הנתונים
df = pd.read_csv("types_of_sentences.csv")
X = df["sentence"]
y = df["label"]

# וקטוריזציה של הטקסט
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000, stop_words="english")
X_vec = vectorizer.fit_transform(X)

# חלוקה לנתוני אימון ובדיקה
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# רשימת המודלים לבדיקה
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(n_estimators=100),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=100),
    "MultinomialNB": MultinomialNB(),
    "SVC": SVC(kernel="linear", probability=True),
    "RidgeClassifier": RidgeClassifier(),
    "KNeighbors": KNeighborsClassifier(n_neighbors=5),
    "DecisionTree": DecisionTreeClassifier(max_depth=10),
    "AdaBoost": AdaBoostClassifier(n_estimators=100),
    "ExtraTrees": ExtraTreesClassifier(n_estimators=100),
    "XGBoost": XGBClassifier(eval_metric='mlogloss')
}

best_model = None
best_score = 0

# הרצה והשוואה של כל מודל
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy: {score:.4f}")

    if score > best_score:
        best_score = score
        best_model = model
        best_model_name = name

# שמירת המודל הטוב ביותר
joblib.dump(best_model, "sentence_type_model.pkl")
joblib.dump(vectorizer, "sentence_type_vectorizer.pkl")

print(f"\nBest model: {best_model_name} with accuracy {best_score:.4f}")
