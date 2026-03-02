import pandas as pd
import re
from sklearn.utils import resample

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)         # remove URLs
    text = re.sub(r'#\S+', '', text)            # remove hashtags
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)    # remove special characters
    text = re.sub(r'\s+', ' ', text).strip()    # remove extra spaces

def main():
    # Load Dataset
    df = pd.read_csv(
        "WELFake_Dataset.csv",
        engine="python",
        on_bad_lines="skip"
    )
    print("Original Shape:", df.shape)

    # Dropping null values
    df = df.dropna()

    print("After Dropping null values:", df.shape)

    # Dropping unneccessary column
    df = df.drop(columns=['Unnamed: 0'])

    # Merging title and text into a single column
    df['content'] = df['title'] + ' ' + df['text']

    df = df[['content', 'label']]

    df['content'] = df['content'].apply(clean_text)
    df = df[df['content'].str.strip() != '']

    print(df['label'].value_counts())       # so it contains 1 corrupted value

    df['label'] = pd.to_numeric(df['label'], errors='coerce')
    df = df.dropna(subset=['label'])
    df['label'] = df['label'].astype(int)

    print(df['label'].value_counts())  



    fake = df[df.label == 0]
    real = df[df.label == 1]    

    min_count = min(len(fake), len(real))

    fake_sample = resample(fake, replace=False, n_samples=min_count, random_state=42)
    real_sample = resample(real, replace=False, n_samples=min_count, random_state=42)

    balanced_df = pd.concat([fake_sample, real_sample])           # Shuffle
    balanced_df = balanced_df.sample(n=20000, random_state=42)    # Reduce Sample size

    print("Final Shape:", balanced_df.shape)

    balanced_df.to_csv("cleaned_news.csv", index=False)


if __name__ == "__main__":
    main()
