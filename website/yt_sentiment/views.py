from django.shortcuts import render
from transformers import pipeline, AutoTokenizer, TFAutoModelForSequenceClassification
import googleapiclient.discovery
import googleapiclient.errors
import os

base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, "nlp_models", "twitter-roberta-base-sentiment")

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = TFAutoModelForSequenceClassification.from_pretrained(model_path)

nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


api_key = "AIzaSyDdoevpmj4XGD2YaquRlvx101kDKH94ji4"


def get_comments(youtube, **kwargs):
    comments = []
    results = youtube.commentThreads().list(**kwargs).execute()

    while results:
        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # check if there are more comments
        if "nextPageToken" in results:
            kwargs["pageToken"] = results["nextPageToken"]
            results = youtube.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments


def main(video_id, api_key):
    # Disable OAuthlib's HTTPs verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    comments = get_comments(
        youtube, part="snippet", videoId=video_id, textFormat="plainText"
    )
    return comments


def get_video_comments(video_id):
    return main(video_id, api_key)


def yt_sentiment(request):
    if request.method == "POST":
        text = request.POST.get("text")
        comments = main(text, api_key)
        result = [nlp(comment, model)[0]["label"] for comment in comments]
        return render(request, "yt_sentiment/result.html", {"sentiment": result})
    else:
        return render(request, "yt_sentiment/yt_sentiment.html")
