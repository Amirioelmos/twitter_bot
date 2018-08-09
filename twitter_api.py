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
        return result
    except ValueError:
        return False


def get_home_time_line(final_oauth_token, final_oauth_token_secret):
    twitter = Twython(APP_KEY, APP_SECRET,
                      final_oauth_token, final_oauth_token_secret)
    try:
        result = twitter.get_home_timeline(exclude_replies=True, count=BotConfig.tweet_count)
        return result
    except ValueError:
        return False


def search_api(final_oauth_token, final_oauth_token_secret, query):
    twitter = Twython(APP_KEY, APP_SECRET,
                      final_oauth_token, final_oauth_token_secret)
    try:
        result = twitter.search(q=query, count=BotConfig.tweet_count)
        return result
    except ValueError:
        return False
