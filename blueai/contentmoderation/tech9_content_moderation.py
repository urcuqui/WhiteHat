
from xml.parsers.expat import model
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import ollama
import re
import ast
import numpy as np
import nltk
from nltk.tokenize import word_tokenize

# Download the necessary NLTK data files
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import os
import joblib
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference, equalized_odds_difference
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import torch




def detect_problematic_content(text_input, model_ensemble):
    """
    Core detection function that processes text and returns
    risk assessment with explanations.
    Args:
    text_input (str): User-generated content to analyze
    model_ensemble: Your hybrid model system
    Returns:
    dict: {
    'risk_score': float,
    'risk_categories': list,
    'confidence': float,
    'explanation': str,
    'requires_human_review': bool
    }
    """
    # YOUR IMPLEMENTATION HERE
    risk_score = model_ensemble.predict_proba(text_input)[0]
    risk_categories = ["toxic", "spam", "offensive"]  # Example categories
    confidence = max(risk_score)    
    explanation = "The content was analyzed using a hybrid model ensemble that combines multiple content moderation techniques."
    requires_human_review = confidence < 0.5  
    return {
    'risk_score': risk_score,
    'risk_categories': risk_categories,
    'confidence': confidence,
    'explanation': explanation,
    'requires_human_review': requires_human_review
    }

def evaluate_model_fairness(predictions, ground_truth, metadata):
    """
    Assess model performance across different demographic
    groups and content types.
    Args:
    predictions: Model predictions
    ground_truth: True labels
    metadata: Demographic/contextual information
    Returns:
    dict: Fairness metrics and bias analysis
    """
    return demographic_parity_difference(y_true=predictions, y_pred=ground_truth, sensitive_features=metadata)
    

def clean_response(text):
    """
    Clean the streamed response by removing unwanted tags and whitespace.
    Args:
    text (str): The raw response text from the model.
    Returns:
    str: Cleaned text with <think> tags removed and leading/trailing whitespace stripped.
    """
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def generate_problematic_content():
    """ Generate a diverse set of problematic content examples.
    Returns:
    list: A Python list of ten strings, each representing a problematic example.
    """

    system = (
    "You are an expert content generator in English. "
    "Your task is to produce only a Python list of exactly ten strings. "
    "Each string must be an example of problematic content, varying in toxicity, tone, and edge case. "
    "Do not explain. Do not reason. Do not add any comments. "
    "Return only the raw Python list as valid code, like this:\n"
    "[\"example 1\", \"example 2\", ..., \"example 10\"]"
    )
    prompt = (
        "Create ten examples of adversarial or problematic content. "
        "Return them as a valid Python list of ten strings. "
        "Do not explain or reason. Just return the list."
        "# Output:\n["
    )    
    response_stream = ollama.chat(
        model="deepseek-r1:7b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    streamed_response = ""
    for token in response_stream:
        streamed_response += token["message"]["content"]
    return ast.literal_eval(clean_response(streamed_response))

def generate_regular_content():
    """ Generate a diverse set of positive, kind, or uplifting content examples.
    Returns:
    list: A Python list of ten strings, each representing a positive example.
    """

    system = (
        "You are an expert content generator focused on creating positive, kind, and constructive examples. "
        "Your task is to produce only a Python list of exactly ten strings. "
        "Each string must be an example of uplifting, encouraging, or helpful content, using diverse writing styles and tones. "
        "Do not explain. Do not reason. Do not add any comments. "
        "Return only the raw Python list as valid code, like this:\n"
        "[\"example 1\", \"example 2\", ..., \"example 10\"]"
    )
    prompt = (
        "Generate ten diverse examples of positive, kind, or uplifting content. "
        "Return only the Python list of ten strings, without explanation or any additional text.\n\n"
        "# Output:\n["
    )
    response_stream = ollama.chat(
        model="deepseek-r1:7b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    streamed_response = ""
    for token in response_stream:
        streamed_response += token["message"]["content"]
    return ast.literal_eval(clean_response(streamed_response))

def preprocess_data(df: pd.DataFrame):
    """
    Preprocess the DataFrame for content moderation.
    Args:
    df (pandas.DataFrame): DataFrame with 'data' and 'labels' columns
    Returns:
    pandas.DataFrame: Preprocessed DataFrame
    """
    # Example preprocessing steps, replace with actual logic
    df['data'] = df['data'].apply(lambda x: x.lower())
    df['data'] = df['data'].apply(lambda x: re.sub(r'\W+', ' ', x))
    df['data'] = df['data'].apply(lambda x: word_tokenize(x))
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    df['data'] = df['data'].apply(lambda x: [ps.stem(word) for word in x if word not in stop_words])
    df["data"] = df["data"].apply(lambda x: " ".join(x))
    print(f"Preprocessed DataFrame with {len(df)} samples.")
    return df

def generate_model(df: pd.DataFrame):
    """
    Train model for content moderation.
    Returns:
    Naive.Bayes: trained model
    """
    preprocessed_df = preprocess_data(df)
    vectorizer = CountVectorizer(min_df=1, max_df=0.9, ngram_range=(1, 2))
        
    # Fit and transform the message column
    X = vectorizer.fit_transform(preprocessed_df["data"])

    # Labels (target variable)
    y = preprocessed_df["label"]

    pipeline = Pipeline([
    ("vectorizer", vectorizer),
    ("classifier", MultinomialNB())
    ])
    param_grid = {
    "classifier__alpha": [0.01, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1.0]
}

    # Perform the grid search with 5-fold cross-validation and the F1-score as metric
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring="f1"
    )

    # Fit the grid search on the full dataset
    grid_search.fit(preprocessed_df["data"], y)
    # Extract the best model identified by the grid search
    best_model = grid_search.best_estimator_
    print(f"Best model parameters: {grid_search.best_params_}")
    print(f"Best model F1 score: {grid_search.best_score_}")
    return best_model

def generate_model_ensemble(text_input=None):
    """
    Create a hybrid model ensemble that combines multiple
    content moderation models for improved accuracy and robustness.
    Args:
    text_input (str): Optional input text for immediate detection
    using the ensemble.     
    Returns:
    list: Ensemble of models
    """
    # Example implementation, replace with actual model loading logic
    model_filename = "naive_model.joblib"
    if os.path.exists(model_filename):
        model = joblib.load(model_filename)
        print(f"Loaded existing model from {model_filename}")
    else:
        df = create_synthetic_dataset()
        model = generate_model(df)
        joblib.dump(model, model_filename)
        print(f"Saved model to {model_filename}")

    # Load additional models if needed, e.g., deep learning models, rule-based systems
    model_two = AutoModelForSequenceClassification.from_pretrained("GroNLP/hateBERT", num_labels=2,cache_dir="hugging/hate")
    tokenizer = AutoTokenizer.from_pretrained("GroNLP/hateBERT", cache_dir="hugging/hate")
    model_two.eval()
    with torch.no_grad():
        inputs = tokenizer(text_input, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        logits1 = outputs.logits
        probs_transformer = torch.softmax(logits1, dim=1).numpy()
        probs_sklearn  = model.predict_proba(text_input)
        # Ensemble
        avg_probs = (probs_transformer + probs_sklearn) / 2
        final_class = avg_probs.argmax()

    print("Model ensemble created successfully.")
    return [
        model,  # Naive Bayes model
        model_two,# Add other models here, e.g., deep learning models, rule-based systems 
    ]


def create_synthetic_dataset():
    """
    Generate realistic training data that covers edge cases
    and demonstrates understanding of content moderation
    challenges.
    Returns:
    pandas.DataFrame: Synthetic dataset with text and labels
    """
    regular = generate_regular_content()
    irregular = generate_problematic_content()
    data = {"data": regular + irregular, "label": np.repeat(1, len(regular)).tolist() + np.repeat(0, len(irregular)).tolist()}
    df = pd.DataFrame(data)
    print(f"Generated dataset with {len(df)} samples.")
    return df

if __name__ == '__main__':
    models = generate_model_ensemble()
    print("Detected problematic content:", detect_problematic_content("You're the worst human being", models[0]))
    #evaluate_model_fairness(models[0].predict_proba(["You're the worst human being"]), [1], {"demographic": "example"})

