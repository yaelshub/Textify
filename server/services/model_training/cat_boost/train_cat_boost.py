import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# טען את הנתונים
df = pd.read_csv("sentences_features.csv")

# נניח שיש עמודה בשם "label" עם הערכים: פשוט, מחובר, מורכב
X = df.drop("label", axis=1)
y = df["label"]

# אם יש עמודות קטגוריות (למשל 'contains_shimur'), רשום את שמן כאן:
cat_features = [col for col in X.columns if X[col].dtype == 'object']

# פיצול לנתוני אימון ובדיקה
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# הגדרת Pool ל-CatBoost (מומלץ)
train_pool = Pool(X_train, y_train, cat_features=cat_features)
test_pool = Pool(X_test, y_test, cat_features=cat_features)

# יצירת המודל ואימון
model = CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1, verbose=0)
model.fit(train_pool)

# חיזוי
y_pred = model.predict(X_test)

# תוצאות
print(classification_report(y_test, y_pred, digits=3))
