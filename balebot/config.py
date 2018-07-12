import logging
import os


class Config:
    base_url = os.environ.get('BASE_URL', None) or "wss://api.bale.ai/v1/bots/"
    # base_url = os.environ.get('BASE_URL', None) or "ws://192.168.3.195:5555/v1/bots/"

    request_timeout = int(os.environ.get('REQUEST_TIMEOUT', None) or 5)
    # 0:print to output        1:use graylog       2:both 0 and 1
    use_graylog = os.environ.get('SDK_USE_GRAYLOG', None) or "2"
    source = os.environ.get('LOG_SOURCE', None) or "bot_source"
    graylog_host = os.environ.get('SDK_GRAYLOG_HOST', None) or "192.168.3.172"
    graylog_port = int(os.environ.get('SDK_GRAYLOG_PORT', None) or "12201")
    log_level = int(os.environ.get('SDK_LOG_LEVEL', None) or logging.DEBUG)
    log_facility_name = os.environ.get('SDK_LOG_FACILITY_NAME', None) or "python_bale_bot"
    monitoring_hash = os.environ.get('MONITORING_HASH', None) or "cabb3f498ac5a037f669f658f1be08c3-"
    real_time_fetch_updates = os.environ.get('REAL_TIME_FETCH_UPDATES', None) or True
    continue_last_processed_seq = os.environ.get('CONTINUE_LAST_PROCESSED_SEQ', None) or False
    timeInterval = os.environ.get('TIME_INTERVAL', None) or 1  # unit for time interval is second
    updates_number = os.environ.get('UPDATES_NUMBER', None) or 3

    rows_per_query = int(os.environ.get('ROWS_PER_QUERY', None) or 10)
    max_retries = int(os.environ.get('MAX_RETRIES', None) or 1)
    check_interval = float(os.environ.get('CHECK_INTERVAL', None) or 0.5)

    time_sleep = float(os.environ.get('TIME_SLEEP', None) or 0.5)
    send_delay = float(os.environ.get('SEND_DELAY', None) or 5)

    latitude_range = float(os.environ.get('VERTICAL_RANGE', None) or 0.005)
    longitude_range = float(os.environ.get('HORIZONTAL_RANGE', None) or 0.005)

    admin_user_id = os.environ.get('ADMIN_USER_ID', None) or "1157162171"

    channel_user_id = int(os.environ.get('CHANNEL_USER_ID', None) or 980604623)
    channel_access_hash = os.environ.get('CHANNEL_ACCESS_HASH', None) or "3768034619353982124"

    max_perform_check_failure = int(os.environ.get('MAX_PERFORM_CHECK_FAILURE', None) or 50)
    max_total_send_failure = int(os.environ.get('MAX_TOTAL_SEND_FAILURE', None) or 10)
    active_next_limit = int(os.environ.get('ACTIVE_NEXT_LIMIT', None) or 40)

    bot_token = os.environ.get('BOT_TOKEN', None) or "1f9610ea2f56c115f880fc602a729ea09aecee53"
    # bot_token = os.environ.get('BOT_TOKEN', None) or "0daf0f5ad1823360facc11738d2a233e8e209b00"

    bot_user_id = os.environ.get('BOT_USER_ID', None) or "41"