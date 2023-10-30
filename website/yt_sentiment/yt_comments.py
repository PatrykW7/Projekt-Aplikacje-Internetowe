import googleapiclient.discovery
import googleapiclient.errors
import os
import re


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


def main(url, api_key):
    # Disable OAuthlib's HTTPs verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    video_id = re.search(r"(?<==)[^&]+", url)[0]
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    comments = get_comments(
        youtube, part="snippet", videoId=video_id, textFormat="plainText"
    )
    return comments


def get_video_comments(video_id, api_key):
    return main(video_id, api_key)
