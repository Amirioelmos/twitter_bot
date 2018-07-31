from balebot.models.messages import TemplateMessageButton, TextMessage, TemplateMessage, JsonMessage
from constant.message import ReadyMessage
from utils.utils import datetime_converter


def make_tweet_message(user_name, text, profile_image_url, favorite_count, retweet_count):
    message = TextMessage(
        ReadyMessage.tweet_message.format(text, user_name, favorite_count, retweet_count,
                                          profile_image_url))
    return message


def extend_tweets(tweets):
    tweets_list = []
    for tweet in tweets:
        user = tweet.get("user")
        print(tweet)
        retweeted_status = tweet.get("retweeted_status")
        if retweeted_status:
            favorite_count = retweeted_status.get("favorite_count")
        else:
            favorite_count = tweet.get("favorite_count")
        entities = tweet.get("entities")
        media = entities.get("media")
        if media:
            media = media[0]
            media_url = media.get("media_url")
            sizes = media.get("sizes")
            medium = sizes.get("medium")
            height = medium.get("h")
            width = medium.get("w")
            media_dict = {"media_url": media.get("media_url"), "height": height, "width": width}
        else:
            media_dict = {}
        dict = {"name": user.get("name"), "text": tweet.get("text"),
                "screen_name": "https://twitter.com/" + user.get("screen_name"),
                "tweet_link": "https://twitter.com/statuses/" + tweet.get("id_str"),
                "profile_image_url": user.get("profile_image_url"),
                "favorite_count": favorite_count,
                "retweet_count": tweet.get("retweet_count"),
                "datetime": datetime_converter(tweet.get("created_at", None)),
                "media_dict": media_dict
                }

        tweets_list.append(dict)
    return tweets_list
