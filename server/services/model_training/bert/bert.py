import torch
import torch.nn.functional as F
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

def analyze_text(text, model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # טען את המודל וה-tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()

    # טען את Label Encoder
    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.load(f"{model_path}/label_encoder_classes.npy", allow_pickle=True)

    # טוקניזציה
    inputs = tokenizer(text, padding=True, truncation=True, max_length=500, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # ניבוי
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
    prediction = torch.argmax(logits, dim=-1).cpu().numpy()[0]
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    # החזר גם את התחזית וגם את ההסתברויות לכל מחבר
    label_probs = dict(zip(label_encoder.classes_, [round(p, 4) for p in probs]))
    return predicted_label, label_probs

# דוגמה להפעלה ישירה (לבדיקות בלבד)
if __name__ == "__main__":
    import time
    start_time = time.time()

    text = """Langford, Dec.
    MY DEAR BROTHER,—I can no longer refuse myself the pleasure of profiting..."""
    
    model_path = "model_folder"  # שנה לתיקיה שלך
    predicted_label, probabilities = analyze_text(text, model_path)

    print(f"Prediction: {predicted_label}")
    print("Probabilities per author:")
    for label, prob in probabilities.items():
        print(f"  {label}: {prob*100:.2f}%")

    print(f"זמן ריצה: {time.time() - start_time:.2f} שניות")
