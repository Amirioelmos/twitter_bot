from twython import Twython

from bot_config import BotConfig

APP_KEY = BotConfig.app_key
APP_SECRET = BotConfig.app_secret


def get_verify_link():
    twitter = Twython(BotConfig.app_key, BotConfig.app_secret)

    auth = twitter.get_authentication_tokens()

    print(auth['auth_url'])
    return auth


# I manually open this url in the browers and
# set oaut_verifier to the value like seen below.
def tweet_api(auth, oauth_verifier, tweet_text):
    OAUTH_TOKEN = auth['oauth_token']

    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    print("OAUTH_TOKEN: ", OAUTH_TOKEN)
    print("OAUTH_TOKEN_SECRET", OAUTH_TOKEN_SECRET)
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    final_step = twitter.get_authorized_tokens(oauth_verifier)

    FINAL_OAUTH_TOKEN = final_step['oauth_token']
    FINAL_OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

    twitter = Twython(APP_KEY, APP_SECRET,
                      FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET)

    # print(twitter.update_status())
    try:
        result = twitter.update_status(status=tweet_text)
        print(result)
        return True
    except ValueError:
        return False
