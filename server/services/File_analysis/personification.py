import joblib
import os


# פונקציה שבודקת האם משפט כולל האנשה
def check_personification(sentence: str) -> bool:
    # הגדרת נתיבים לקבצים
    BASE_DIR = os.path.dirname(__file__)
    MODEL_PATH = os.path.join(BASE_DIR, '..', 'model_training', 'personification_model', 'personification_model.pkl')
    VECTORIZER_PATH = os.path.join(BASE_DIR, '..', 'model_training', 'personification_model', 'vectorizer.pkl')

    # טעינת המודל והוקטוריזר
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    X_vec = vectorizer.transform([sentence])
    prediction = model.predict(X_vec)[0]

    return prediction == 1  

# פונקציה שמקבלת רשימת משפטים ומחזירה כמה מתוכם הם האנשה
def count_personifications(sentences: list[str]) -> int:
    count = 0
    for sentence in sentences:
        if check_personification(sentence):
            count += 1
    return count
