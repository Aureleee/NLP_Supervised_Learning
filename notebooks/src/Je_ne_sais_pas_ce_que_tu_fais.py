import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def categorize_sentiment(note):
    if note == 'NaN':
        return None
    elif note <= 2:
        return 'Negative'
    elif note == 3:
        return 'Neutral'
    else:
        return 'Positive'
    
def train_sim_model(df, max_features=3000, max_iter=1000):
    
    X = df["avis_en"]
    y = df["sentiment"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    nlp_model = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=max_features, stop_words='english')),
        ('regressor', LogisticRegression(max_iter=max_iter, class_weight='balanced'))
    ])

    nlp_model.fit(X_train, y_train)

    return nlp_model, X_test, y_test

def evaluate_sim_model(nlp_model, X_test, y_test):
    
    y_pred = nlp_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred, labels=['Negative', 'Neutral', 'Positive'])

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Negative', 'Neutral', 'Positive'], 
                yticklabels=['Negative', 'Neutral', 'Positive'])
    plt.ylabel('True Sentiment')
    plt.xlabel('Predicted Sentiment')
    plt.title('Confusion Matrix')
    plt.show()