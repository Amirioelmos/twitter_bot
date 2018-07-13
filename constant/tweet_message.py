from balebot.models.messages import TemplateMessageButton, TextMessage, TemplateMessage, JsonMessage
from constant.message import ReadyMessage


def make_tweet_message(user_name, text, profile_image_url, favorite_count, retweet_count):
    message = TextMessage(
        ReadyMessage.tweet_message.format(text, user_name, favorite_count, retweet_count,
                                          profile_image_url))
    return message
