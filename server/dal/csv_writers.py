import pandas as pd

def write_segments_to_a_CSV_file(chapters, filename):
    df = pd.DataFrame({'chapter_text': chapters})
    df.to_csv(filename, index=False, encoding='utf-8')
    df = pd.read_csv(filename)

# chapters = [
#     "Once upon a time in a land far away...",
#     "The journey continued through the mountains.",
#     "At last, they reached the ancient city."
#     ]

# filename = 'd:/Textify/server/data/Jane_Austen.csv'
# write_segments_to_a_CSV_file(chapters, filename)
