import os


class BotConfig:
    rows_per_query = int(os.environ.get('ROWS_PER_QUERY', None) or 50)
    max_retries = int(os.environ.get('MAX_RETRIES', None) or 3)
    check_interval = float(os.environ.get('CHECK_INTERVAL', None) or 0.5)
    time_sleep = float(os.environ.get('TIME_SLEEP', None) or 0.5)

    max_perform_check_failure = int(os.environ.get('MAX_PERFORM_CHECK_FAILURE', None) or 50)
    max_total_send_failure = int(os.environ.get('MAX_TOTAL_SEND_FAILURE', None) or 10)
    active_next_limit = int(os.environ.get('ACTIVE_NEXT_LIMIT', None) or 40)

    bot_token = os.environ.get('TOKEN', None) or "1f9610ea2f56c115f880fc602a729ea09aecee53"
    bot_user_id = os.environ.get('USER_ID', None) or "41"

    app_key = os.environ.get('APP_KEY', None) or "vNo9Sp0r1YuQM3jAHjL3C2qvR"
    app_secret = os.environ.get('APP_SECRET', None) or "o0eLxGxMBT78KOrOmFbq5HrhgGQ15ge7Ae5geNWdowWVTZSKjI"
    tweet_count = int(os.environ.get('TWEET_COUNT', None) or 10)
