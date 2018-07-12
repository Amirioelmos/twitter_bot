from twython import Twython, TwythonError

APP_KEY = 'vNo9Sp0r1YuQM3jAHjL3C2qvR'
APP_SECRET = 'o0eLxGxMBT78KOrOmFbq5HrhgGQ15ge7Ae5geNWdowWVTZSKjI'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
print(ACCESS_TOKEN)
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
status=twitter.search(q='python', result_type='popular').get("statuses")
for i in status:
    print(i.get("text"))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n\n\n\n\n")



# twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
# auth = twitter.get_authentication_tokens()
#
# print(auth['auth_url'])
#
# oauth_verifier = input('Enter your pin:')
#
# final_step = twitter.get_authorized_tokens(oauth_verifier)
#
#
# FINAL_OAUTH_TOKEN = final_step['oauth_token']
# FINAL_OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
#
# twitter = Twython(APP_KEY, APP_SECRET,
#                   FINAL_OAUTH_TOKEN, FINAL_OAUTH_TOKEN_SECRET)
#
# print(twitter.get_home_timeline())
