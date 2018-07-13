class ReadyMessage:
    start_conversation = "سلام.\nبه بات *توییتر همراه* خوش آمدید. لطفا یکی از گزینه های زیر را انتخاب کنید."
    send_verify_number = "لطفا وارد لینک زیر شوید و عدد دریافتی را برای من بفرستید.\n" \
                         "{}"
    send_text_twitter = "لطفا متن توییت خود را ارسال کنید.\n" \
                        "*توجه:* ممکن است ارسال توییت کمی زمان‌بر باشد. از شکیبایی شما متشکریم"
    send_search_text = "لطفا متن مورد نظر برای جست و جو را وارد نمایید."
    success_tweet = "توییت شما با موفقیت ارسال گردید."
    fail_tweet = "متاسفانه! ارسال توییت موفق نبود."
    error = "*خطایی رخ داده است. *" \
            " لطفا دوباره امتحان کنید."
    information = "Created by:\n" \
                  "@EhsanBarkhordar"
    send_name = "لطفا نام خود را ارسال کنید."
    send_phone_number = "لطفا تلفن همراه خود را ارسال کنید."
    success_insert_user = "نام شما با موفقیت در بات ثبت شد."
    fail_insert_user = "متاصفانه نام شما با موفقیت در بات ثبت نشد."
    not_register = "شما اولین بار است که ازین بات استفاده میکنید.\n" \
                   "لطفا برای شروع روی دکمه زیر کلیک کنید."
    tweet_message = "{}\n" \
                    "کاربر: {}\n" \
                    "لایک: {} --- ریتویت:{}\n" \
                    "{}"


class TMessage:
    cancel = "لغو"
    keep_on = "تایید و ادامه"
    edit = "اصلاح میکنم"
    start = "ادامه"
    info = "راهنما"
    back = "بازگشت به منو اصلی"
    send_tweet = "ارسال تويیت"
    get_time_line = "خواندن تایم لاین"
    register = "ثبت نام کاربری"
    search = "جستجو توییت"


class LogMessage:
    start = "conversation started"
    success_send_message = "success send message"
    fail_send_message = "success send message"
    max_fail_retried = "max fails retried"
    invalid_game = "invalid game"
    edit_name = "edit name started"

    fail_notification = "notification push failed"
    success_notification = "{} notification pushed"

    insert_predict_error = "error in insertion predicts"
    no_game = "no game is valid"
    new_user_detected = "new user start conversation"

    bot_error = "there is a problem with bot, program is exiting"
    request_game_id = "a game id result requested"

    get_prediction_started = "take prediction started"
    wrong_prediction = "wrong prediction occurred"
    right_prediction = "right prediction occurred"
    cancel_progress = "progress canceled"

    respond_notification = "respond to push message"

    info = "info showed"

    got_name = "name received"
    got_phone_number = "phone number received"

    take_iran_goals = "taking iran goals"
    take_opponent_team = "take opponent team"

    get_past_prediction = "get past prediction started"

    request_valid_predictions = "request valid predictions"

    change_template_failed = "change template message failed"

    change_template_success = "change template message success"
    check_db_connection = "Check db connection"
    fail_to_connect_db = "fail to connect db"
    success_connect_db = "db is connected"
    db_string_executed = "db string executed"

    fail_create_table = "fail create table"
    success_create_table = "success create table or table existed before"

    success_user_registration = "user registration was successful"
    invalid_phone_number = "phone number is invalid"


class Regex:
    phone_number_regex = '(^(\+98|0098|0)?9\d{9})|(^(\+۹۸|۰۰۹۸|۰)?۹[۰-۹]{9})$'
    score_regex = '(^[0-9]+)$|(^[۰-۹]+)$'
    quarter_regex = '^(([1-9]|1[0-6])-([1-9]|1[0-6])-([1-9]|1[0-6])-([1-9]|1[0-6]))$' \
                    '|^(([۱-۹]|۱[۰-۶])-([۱-۹]|۱[۰-۶])-([۱-۹]|۱[۰-۶])-([۱-۹]|۱[۰-۶]))$'
