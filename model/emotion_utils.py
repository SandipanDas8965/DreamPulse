import pickle
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'emotion_model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

with open(os.path.join(BASE_DIR, 'label_names.pkl'), 'rb') as f:
    label_names = pickle.load(f)

dream_symbols = {
    "water": ["water", "ocean", "sea", "rain", "river", "swimming"],
    "falling": ["falling", "fell", "fall"],
    "flying": ["flying", "fly", "flew"],
    "teeth": ["teeth", "tooth"],
    "being_chased": ["chasing", "chased", "running from", "being followed"],
    "exam": ["exam", "test", "studied", "studying"],
    "death": ["died", "death", "dying", "dead"],
    "school": ["school", "classroom", "teacher"],
}

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    sentences = [s for s in sentences if s.strip()]
    return sentences

def get_top_emotion(text):
    sentences = split_into_sentences(text)

    if not sentences:
        sentences = [text]

    vectors = vectorizer.transform(sentences)

    all_probabilities = model.predict_proba(vectors)

    avg_probabilities = all_probabilities.mean(axis=0)

    top_index = avg_probabilities.argmax()
    emotion = label_names[top_index]
    confidence = round(float(avg_probabilities[top_index]), 2)

    return emotion, confidence

def find_symbols(text):
    text_lower = text.lower()
    found = []
    for symbol, keywords in dream_symbols.items():
        for keyword in keywords:
            if keyword in text_lower:
                found.append(symbol)
                break
    return found

def analyze_entry(text):
    emotion, confidence = get_top_emotion(text)
    symbols = find_symbols(text)
    return {
        "emotion": emotion,
        "confidence": confidence,
        "symbols": symbols
    }

def get_emotion_breakdown(text):
    sentences = split_into_sentences(text)
    if not sentences:
        sentences = [text]

    vectors = vectorizer.transform(sentences)
    predictions = model.predict(vectors)

    breakdown = []
    for sentence, pred in zip(sentences, predictions):
        breakdown.append({
            "sentence": sentence,
            "emotion": label_names[pred]
        })
    return breakdown