import torch
# softmax פונקציות מתמטיות כמו 
import torch.nn.functional as F
import numpy as np
# ספרייה של HuggingFace מכילה את BERT
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

def analyze_text(text, model_path):
    #אם יש GPU פנוי – המודל ירוץ עליו, אחרת ירוץ על CPU.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = BertTokenizer.from_pretrained(model_path)
    #סוג מיוחד של מודל BERT שיודע לעשות סיווג טקסטים
    model = BertForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    #מצב חיזוי אמין ולא אקראי
    model.eval()

    label_encoder = LabelEncoder()
    #List of original author names
    label_encoder.classes_ = np.load(f"{model_path}/label_encoder_classes.npy", allow_pickle=True)

    #לוקח את הטקסט ומפרק אותם ל־מספרים
    inputs = tokenizer(text, padding=True, truncation=True, max_length=500, return_tensors="pt")
    #שולחת את הכל ל־GPU או CPU 
    inputs = {k: v.to(device) for k, v in inputs.items()}

#בלי חישוב גרדיאנטים, אנחנו בשלב חיזוי
    with torch.no_grad():
        #מכניס את הקלט למודל ומחזיר את התוצאה
        outputs = model(**inputs)
    #ציון פנימי שמראה כמה המודל חושב על כל סופר
    logits = outputs.logits
    # הופך את logits ל־הסתברויות בין 0 ל־1, שהסכום שלהן = 1
    probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
    #מחזיר את ההסתברות הכי גבוהה ואז את האינדקס של המחבר הכי סביר.
    prediction = torch.argmax(logits, dim=-1).cpu().numpy()[0]
    #הופך את המספר לשם המחבר האמיתי
    predicted_label = label_encoder.inverse_transform([prediction])[0]
    # בונה מילון עם שמות המחברים וההסתברויות שלהם
    label_probs = dict(zip(label_encoder.classes_, [round(p, 4) for p in probs]))
#מחזיר את השם הכי סביר ואת ההסתברויות של כולם
    return predicted_label, label_probs
