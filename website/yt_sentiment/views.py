from django.shortcuts import render
from pathlib import Path
from . import yt_comments
from . import load_model
from transformers import pipeline
import environ

env = environ.Env()
environ.Env.read_env()

GOOGLE_API_KEY = env("GOOGLE_API_KEY")
model_path = Path("website\yt_sentiment\nlp_models\twitter-roberta-base-sentiment")
model, tokenizer = load_model.load_model(path=model_path)

nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def yt_sentiment(request):
    if request.method == "POST":
        text = request.POST.get("text")
        comments = yt_comments.main(text, GOOGLE_API_KEY)
        result = [nlp(comment, model)[0]["label"] for comment in comments]
        return render(request, "yt_sentiment/result.html", {"sentiment": result})
    else:
        return render(request, "yt_sentiment/yt_sentiment.html")
