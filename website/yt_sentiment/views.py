from django.shortcuts import render
from pathlib import Path
from .yt_comments import get_video_comments
from .load_model import load_model
from transformers import pipeline
import environ
import pandas as pd
from django.contrib.auth.decorators import login_required
from urllib.error import HTTPError
from googleapiclient.errors import HttpError
import pandas as pd

env = environ.Env()
environ.Env.read_env()

GOOGLE_API_KEY = env("GOOGLE_API_KEY")
base_path = Path(__file__).parent
model_path = Path(base_path, "nlp_models/twitter-roberta-base-sentiment")
model, tokenizer = load_model(path=model_path)
tokenizer_kwargs = {"padding": True, "truncation": True, "max_length": 512}

nlp = pipeline(
    "sentiment-analysis", model=model, tokenizer=tokenizer, **tokenizer_kwargs
)

result = {}


@login_required(login_url="/login")
def yt_sentiment(request):
    if request.method == "POST":
        try:
            text = request.POST.get("text")
            comments = get_video_comments(text, GOOGLE_API_KEY)

            
           


            if not comments:
                result = {"available": "No comments available"}

                return render(
                    request, "yt_sentiment/yt_sentiment.html", {"sentiment": result}
                )
            else:
                analysed_comments = [nlp(comment, model)[0] for comment in comments]
                df_result = pd.DataFrame(analysed_comments)

                sentiment_percentage = df_result["label"].value_counts().values / len(
                    df_result
                )
                sentiment_percentage = [round(num, 2) for num in sentiment_percentage]
                num_comments = len(df_result)
                percents = df_result["label"].value_counts()
                lab = df_result["label"]
                percent_help = {}

                for label, value in zip(percents.index, percents.values):
                    percent_help[label] = value

                labels = list(percent_help.keys())
                values = list(percent_help.values())

                index = []
                [index.append(i+1) for i in range(len(comments))]
                df_comments = pd.DataFrame({
                    'comments': comments,
                    'labels': lab, 
                })


        except HttpError:
            result = {"available": "No comments available"}

            return render(
                request, "yt_sentiment/yt_sentiment.html", {"sentiment": result}
            )

        try:
            most_pos_com_id = df_result[df_result["label"] == "positive"][
                "score"
            ].idxmax()
            most_pos_com = comments[most_pos_com_id]
        except ValueError:
            most_pos_com = "You have no positive comments 🙁"

        try:
            most_neg_com_id = df_result[df_result["label"] == "negative"][
                "score"
            ].idxmax()
            most_neg_com = comments[most_neg_com_id]

        except ValueError:
            most_neg_com = "You have no negative comments! 🥳"

        result = {
            "num_comments": num_comments,
            "most_pos_com": most_pos_com,
            "most_neg_com": most_neg_com,
            "percents": percent_help.items,
            "labels": labels,
            "values": values,
            
        }

        return render(
            request,
            "yt_sentiment/yt_sentiment.html",
            {"sentiment": result, "df": df_comments},
        )
    else:
        return render(request, "yt_sentiment/yt_sentiment.html")
