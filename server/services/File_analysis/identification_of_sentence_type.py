import joblib
from collections import Counter
import os
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model_training"))

# נתיבי המודל והוקטורייזר
sentence_model_path = os.path.join(base_dir, "identification_of_sentence_type_model", "identifying_sentence_type.pkl")
sentence_vectorizer_path = os.path.join(base_dir, "identification_of_sentence_type_model", "vectorizer.pkl")

# טעינה
model = joblib.load(sentence_model_path)
vectorizer = joblib.load(sentence_vectorizer_path)

# מיפוי מספרים לסוגים מילוליים
label_mapping = {
    0: "Simple",
    1: "Compound",
    2: "Complex"
}

def classify_sentence_type(sentences):
    # וקטוריזציה של כל המשפטים
    sentence_vectors = vectorizer.transform(sentences)
    
    # תחזית לכל המשפטים
    predictions = model.predict(sentence_vectors)

    # מיפוי התחזיות לטקסט
    predicted_labels = [label_mapping[p] for p in predictions]

    # ספירה
    counts = Counter(predicted_labels)
    total = len(sentences)

    # חישוב אחוזים
    percentages = {}
    for label in label_mapping.values():
        percentage = round((counts[label] / total) * 100, 2)
        percentages[label] = percentage
        
    # מציאת הסוג השולט
    most_common = counts.most_common(1)[0][0]

    return {
        "counts": dict(counts),
        "percentages": percentages,
        "most_frequent_type": most_common
    }
