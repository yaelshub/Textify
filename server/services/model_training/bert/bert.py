import torch
import torch.nn.functional as F
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

def analyze_text(text, model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    #Prediction mode, not training
    model.eval()

    label_encoder = LabelEncoder()
    #List of original author names
    label_encoder.classes_ = np.load(f"{model_path}/label_encoder_classes.npy", allow_pickle=True)

    #Transform text into input that BERT understands
    inputs = tokenizer(text, padding=True, truncation=True, max_length=500, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    #Prediction
    # Canceling gradient calculation because we are not in training.
    with torch.no_grad():
        #Send the input to the model and receive the outputs.
        outputs = model(**inputs)
    #The raw output
    logits = outputs.logits
    #Converts logits to probabilities
    probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
    #Selects the index with the highest probability
    prediction = torch.argmax(logits, dim=-1).cpu().numpy()[0]
    #Converts the predicted number back to a connector name.
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    # Creates a dictionary where the keys are the names of the authors, and the values ​​are the probabilities for each of them
    label_probs = dict(zip(label_encoder.classes_, [round(p, 4) for p in probs]))
    #Returns the name of the author that the model thinks is most appropriate and the dictionary of probabilities for each author.
    return predicted_label, label_probs
