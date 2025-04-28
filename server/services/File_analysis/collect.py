import pandas as pd
from collections import Counter
from services.File_analysis.tokenization import tok 


# יצירת טבלה עם מידע על המילים
def create_word_table(words):
    # ספירת מילים
    word_count = Counter(words)
    num_words = len(words)
    
    # יצירת DataFrame
    data = {
        "Wo rd": list(word_count.keys()),
        "Count": list(word_count.values()),
        "Frequency": [count / num_words for count in word_count.values()],
        "Length": [len(word) for word in word_count.keys()]
    }
    df = pd.DataFrame(data)
    
    # מיון לפי מספר הופעות (אופציונלי)
    df = df.sort_values(by="Count", ascending=False).reset_index(drop=True)
    return df

# שימוש בפונקציה
words = tok["words"]  # רשימת המילים מהטקסט
word_table = create_word_table(words)

# הצגת הטבלה
print(word_table)

# דוגמה לשליפת מידע מהירה
print("Top 10 most frequent words:")
print(word_table.head(10))  # עשר המילים הנפוצות ביותר