import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.utils.class_weight import compute_class_weight
from datasets import Dataset
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve, f1_score, roc_auc_score, average_precision_score,confusion_matrix,recall_score
from sklearn.metrics import accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

csv_file_path = os.path.join(os.getcwd(), "texts_authors.csv")

def compute_metrics(pred):
      labels = pred.label_ids
      preds = pred.predictions.argmax(-1)
      f1 = f1_score(labels, preds, average='weighted')
      acc = accuracy_score(labels, preds)
      return {
          'accuracy': acc,
          'f1': f1,
      }

def show_confusin_matrix(y_test,y_pred):
        class_names =np.unique(y_test)  
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.show()

def show_plt(x1,x2,titlex1,titlex2,plot_title):
        plt.figure(figsize=(10, 6))
        plt.plot(x1, label=titlex1)
        plt.plot(x2, label=titlex2)
        plt.xlabel(titlex1)
        plt.ylabel(titlex2)
        plt.title(plot_title)
        plt.legend()
        plt.grid(True)
        plt.show()

def plot_loss(train_losses,val_losses,k):
        plt.figure(figsize=(12, 6))

        for i in range(k):
            plt.plot(train_losses[i], label=f'Train Loss Fold {i+1}')

        for i in range(k):
            plt.plot(val_losses[i], label=f'Validation Loss Fold {i+1}', linestyle='--')

        plt.title('Loss Function Across K-Folds')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

dataset = pd.read_csv(csv_file_path, encoding='utf-8',sep='§')
dfds = pd.DataFrame(dataset)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

texts = dfds['text']
labels = dfds['author']
# הופכת את שמות המחברים למספרים
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)
#ם יש מחבר נדיר ומחבר שכיח יש לאזן את התרומה של כל מחבר כך שהמודל לא יטה כל הזמן למחבר הכי נפוץ.
class_weights = compute_class_weight('balanced', classes=np.unique(labels_encoded), y=labels_encoded)
class_weights = torch.tensor(class_weights, dtype=torch.float).to(device)

# טעינת טוקנייזר ומודל BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased',
                                                            num_labels=len(set(labels_encoded)))
model.to(device)
def tokenize_function(examples):
     return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=500)
# יצירת DataFrame
df = pd.DataFrame({'text': texts, 'label': labels_encoded})
# ם יש מחבר נדיר ומחבר שכיח – את מאזנת את התרומה של כל מחבר כך שהמודל לא יטה כל הזמן למחבר הכי נפוץ.
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df['text'], df['label'], test_size=0.2, stratify=df['label'], random_state=42)
# יצירת DataFrame מחדש לכל סט
train_df = pd.DataFrame({'text': train_texts, 'label': train_labels})
test_df = pd.DataFrame({'text': test_texts, 'label': test_labels})
# המרת ה-DataFrames ל-Hugging Face Datasets
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)
#מבצעת טוקניזציה על כל הדאטה 
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_test = test_dataset.map(tokenize_function, batched=True)
# הגדרת רשימה לערכי האיבוד (loss)
loss_values = []

#מחזירה מדדים חשובים כמו דיוק (accuracy) וממוצע F1.
training_args = TrainingArguments(
    output_dir="./results",
    #2e-5 = 0.00002
    learning_rate=2e-5,
    num_train_epochs=4,
    #To prevent overfitting
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    gradient_accumulation_steps=4,
    fp16=False,
    dataloader_num_workers=4,
    report_to="none",
    prediction_loss_only=False  
)
# שימוש ב-Trainer לאימון המודל
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    compute_metrics=compute_metrics
)
# אימון המודל עם מעקב אחרי איבוד (loss)
for epoch in range(int(training_args.num_train_epochs)):
    train_results = trainer.train()
    trainer.log_metrics("train", train_results.metrics)
    # שמירת ערכי האיבוד (loss) לכל epoch
    current_loss = train_results.metrics['train_loss']
    loss_values.append(current_loss)

#The model is run on the test set, and returns results such as accuracy and loss.
results = trainer.evaluate()  

# חיזוי התוויות על סט הבדיקה
predictions = trainer.predict(tokenized_test)

# spending the expected labels
y_pred = predictions.predictions.argmax(axis=-1)
y_true = predictions.label_ids
#Converts the numbers back to the names of the authors
y_pred_original = label_encoder.inverse_transform(y_pred)
Y_test_original = label_encoder.inverse_transform(y_true)
y_pred = y_pred_original
y_true = Y_test_original


# confusion matrix
print(confusion_matrix(y_true, y_pred))
show_confusin_matrix(y_true,y_pred)

# classification report
target_names = label_encoder.classes_.astype(str)
class_report = classification_report(y_true, y_pred, target_names=target_names)
print(class_report)

# loss values
plt.figure(figsize=(10, 6))
plt.plot(loss_values, label='Training Loss')
plt.title('Training Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid()
plt.show()
