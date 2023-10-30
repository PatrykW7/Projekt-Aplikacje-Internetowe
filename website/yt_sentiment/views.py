from django.shortcuts import render
from pathlib import Path
from . import yt_comments
from . import load_model
from transformers import pipeline
import environ
import pandas as pd

env = environ.Env()
environ.Env.read_env()

GOOGLE_API_KEY = env("GOOGLE_API_KEY")
base_path = Path(__file__).parent
model_path = Path(base_path, "nlp_models/twitter-roberta-base-sentiment")
model, tokenizer = load_model.load_model(path=model_path)

nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

result = {}


def yt_sentiment(request):
    if request.method == "POST":
        text = request.POST.get("text")
        comments = yt_comments.main(text, GOOGLE_API_KEY)
        analysed_comments = [nlp(comment, model)[0]["label"] for comment in comments]
        df_result = pd.DataFrame(analysed_comments)
        sentiment_percentage = df_result.value_counts() / len(df_result)
        result = {
            "num_comments": len(df_result),
            "sentiment_percentage": sentiment_percentage,
        }

        return render(request, "yt_sentiment/result.html", {"sentiment": result})
    else:
        return render(request, "yt_sentiment/yt_sentiment.html")
