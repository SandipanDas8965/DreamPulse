# DreamPulse: Dream Journal Pattern Analyzer

A Flask web app that detects emotions and recurring symbols in dream entries,
using a Logistic Regression model trained from scratch (90.48% test accuracy).

## Links
- Documentation: [docs/DreamPulse_Documentation.pdf](docs/DreamPulse_Documentation.pdf)
- Presentation: [docs/DreamPulse_Presentation.pptx](docs/DreamPulse_Presentation.pptx)
- Training notebook: [notebooks/training.ipynb](notebooks/training.ipynb)
- Dataset source: https://huggingface.co/datasets/dair-ai/emotion

## Run locally
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000

## Tech stack
Python, scikit-learn, Flask, SQLite, HTML/CSS/JavaScript, Chart.js

## Team
Sandipan Das, Subhamoy Ghosh, Md Faryaad Sha