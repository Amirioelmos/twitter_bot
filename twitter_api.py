from twython import Twython

from bot_config import BotConfig

APP_KEY = BotConfig.app_key
APP_SECRET = BotConfig.app_secret


def get_verify_link():
    twitter = Twython(BotConfig.app_key, BotConfig.app_secret)
    auth = twitter.get_authentication_tokens()
    return auth


def final_verify(oauth_verifier, oauth_token, oauth_token_secret):
    twitter = Twython(APP_KEY, APP_SECRET, oauth_token, oauth_token_secret)
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    final_oauth_token = final_step['oauth_token']
    final_oauth_token_secret = final_step['oauth_token_secret']
    final_dict = {"final_oauth_token": final_oauth_token, "final_oauth_token_secret": final_oauth_token_secret}
    return final_dict


def send_tweet_api(final_oauth_token, final_oauth_token_secret, tweet_text):
    twitter = Twython(APP_KEY, APP_SECRET,
                      final_oauth_token, final_oauth_token_secret)
    try:
        result = twitter.update_status(status=tweet_text)
        return True
    except ValueError:
        return False


def get_home_time_line(final_oauth_token, final_oauth_token_secret):
    twitter = Twython(APP_KEY, APP_SECRET,
                      final_oauth_token, final_oauth_token_secret)
    try:
        result = twitter.get_home_timeline(exclude_replies=True, count=BotConfig.tweet_count)
        tweets_list = []
        for tweet in result:
            user = tweet.get("user")
            retweeted_status = tweet.get("retweeted_status")
            if retweeted_status:
                favorite_count = retweeted_status.get("favorite_count")
            else:
                favorite_count = tweet.get("favorite_count")
            dict = {"name": user.get("name"), "text": tweet.get("text"),
                    "screen_name": "https://twitter.com/" + user.get("screen_name"),
                    "tweet_link": "https://twitter.com/statuses/" + tweet.get("id_str"),
                    "profile_image_url": user.get("profile_image_url"),
                    "favorite_count": favorite_count,
                    "retweet_count": tweet.get("retweet_count")}
            tweets_list.append(dict)
        return tweets_list
    except ValueError:
        return False


def search_api(final_oauth_token, final_oauth_token_secret, query):
    twitter = Twython(APP_KEY, APP_SECRET,
                      final_oauth_token, final_oauth_token_secret)
    try:
        result = twitter.search(q=query, count=BotConfig.tweet_count)
        statuses = result.get("statuses")
        tweets_list = []
        for status in statuses:
            user = status.get("user")
            retweeted_status = status.get("retweeted_status")
            if retweeted_status:
                favorite_count = retweeted_status.get("favorite_count")
            else:
                favorite_count = status.get("favorite_count")
            dict = {"name": user.get("name"), "text": status.get("text"),
                    "screen_name": "https://twitter.com/" + user.get("screen_name"),
                    "tweet_link": "https://twitter.com/statuses/" + status.get("id_str"),
                    "profile_image_url": user.get("profile_image_url"),
                    "favorite_count": favorite_count,
                    "retweet_count": status.get("retweet_count")}
            tweets_list.append(dict)
        return tweets_list
    except ValueError:
        return False

# search_api("981164432905658368-zKY664sjNQKRmVaq9eIWBFHuHnvPufK", "mtezuUYBYPyD7gpvWyex5An7GcpL3FC10rrNsfrLs0Jmv",
#            "python")
