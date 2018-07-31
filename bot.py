from balebot.filters import TemplateResponseFilter, TextFilter, DefaultFilter
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import TemplateMessageButton, TextMessage, TemplateMessage, PhotoMessage
from balebot.updater import Updater
from balebot.utils.logger import Logger
from bot_config import BotConfig
from constant.message import ReadyMessage, TMessage, LogMessage, Regex
from db.db_handler import create_all_table, insert_user, get_user
import asyncio

from twitter_api import get_verify_link, send_tweet_api, final_verify, get_home_time_line, search_api
from utils.utils import eng_to_arabic_number

updater = Updater(token=BotConfig.bot_token,
                  loop=asyncio.get_event_loop())
bot = updater.dispatcher.bot
dispatcher = updater.dispatcher

my_logger = Logger.logger
create_all_table()


def success(response, user_data):
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    my_logger.info(LogMessage.success_send_message, extra={"user_id": user_peer.peer_id, "tag": "info"})


def failure(response, user_data):
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    try_times = int(user_data["try_times"])
    message = user_data["message"]
    if try_times < BotConfig.max_total_send_failure:
        try_times += 1
        my_logger.error(LogMessage.fail_send_message, extra={"user_id": user_peer.peer_id, "tag": "error"})
        kwargs = {"message": message, "user_peer": user_peer, "try_times": try_times}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    else:
        my_logger.error(LogMessage.max_fail_retried, extra={"tag": "error"})


def check_user_registration(update, user_peer, user):
    if user:
        return user
    else:
        general_message = TextMessage(ReadyMessage.not_register)
        btn_list = [TemplateMessageButton(text=TMessage.register, value=TMessage.register, action=0)]
        template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
        kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        dispatcher.finish_conversation(update)
        return False


@dispatcher.message_handler(
    filters=[TemplateResponseFilter(keywords=[TMessage.start, TMessage.back]), TextFilter(keywords="start")])
def start_conversation(bot, update):
    user_peer = update.get_effective_user()
    general_message = TextMessage(ReadyMessage.start_conversation)
    btn_list = [TemplateMessageButton(text=TMessage.send_tweet, value=TMessage.send_tweet, action=0),
                TemplateMessageButton(text=TMessage.get_home_time_line, value=TMessage.get_home_time_line, action=0),
                TemplateMessageButton(text=TMessage.search, value=TMessage.search, action=0),
                TemplateMessageButton(text=TMessage.info, value=TMessage.info, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[TMessage.register]))
def registration(bot, update):
    dispatcher.clear_conversation_data(update)
    user_peer = update.get_effective_user()
    auth = get_verify_link()
    dispatcher.set_conversation_data(update, "auth", auth)
    verify_link = auth['auth_url']
    text_message = TextMessage(ReadyMessage.send_verify_number.format(verify_link))
    kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, [CommandHandler("info", info),
                                                                MessageHandler(TextFilter(), verify),
                                                                MessageHandler(DefaultFilter(), start_conversation)])


def verify(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    auth = dispatcher.get_conversation_data(update, "auth")
    oauth_verifier = update.get_effective_message().text
    access_hash = user_peer.access_hash
    final_dict = final_verify(oauth_verifier=oauth_verifier, oauth_token=auth['oauth_token'],
                              oauth_token_secret=auth['oauth_token_secret'])
    result = insert_user(user_id=user_id, access_hash=access_hash,
                         final_oauth_token=final_dict.get("final_oauth_token"),
                         final_oauth_token_secret=final_dict.get("final_oauth_token_secret"))
    if not result or not final_dict:
        text_message = TextMessage(ReadyMessage.fail_insert_user)
        kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        dispatcher.finish_conversation(update)
        return 0
    general_message = TextMessage(ReadyMessage.success_insert_user)
    btn_list = [TemplateMessageButton(text=TMessage.send_tweet, value=TMessage.send_tweet, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[TMessage.send_tweet]))
def get_tweet_text(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    user = get_user(user_id=user_id)
    if not check_user_registration(update, user_peer, user):
        return 0
    general_message = TextMessage(ReadyMessage.send_text_twitter)
    btn_list = [TemplateMessageButton(text=TMessage.cancel, value=TMessage.cancel, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("info", info),
                                                        MessageHandler(TextFilter(), send_tweet),
                                                        MessageHandler(DefaultFilter(), start_conversation)])


def send_tweet(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    tweet_text = update.get_effective_message().text
    user = get_user(user_id=user_id)
    result = send_tweet_api(final_oauth_token=user.final_oauth_token,
                            final_oauth_token_secret=user.final_oauth_token_secret, tweet_text=tweet_text)
    if result:
        general_message = TextMessage(ReadyMessage.success_tweet)
    else:
        general_message = TextMessage(ReadyMessage.fail_tweet)
    btn_list = [TemplateMessageButton(text=TMessage.back, value=TMessage.back, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[TMessage.get_home_time_line, TMessage.show_more]))
def get_home_time_line(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    user = get_user(user_id=user_id)
    if not check_user_registration(update, user_peer, user):
        return 0
    time_line = get_home_time_line(final_oauth_token=user.final_oauth_token,
                                   final_oauth_token_secret=user.final_oauth_token_secret)
    a = 1
    for tweet in time_line:
        media_dict = tweet.get("media_dict")
        if media_dict:
            print("meddddddddddddiiiiiiiiiiiiiaaaaaaaaaaa")
            media_url = media_dict.get("media_url")
            print(media_url)
            # import ast
            # media_url = ast.literal_eval(media_url)
            print(media_url)
            height = media_url.get("height")
            width = media_url.get("width")

            def file_upload_success(result, user_data):
                print("upload was successful : ", result)
                print(user_data)
                file_id = str(user_data.get("file_id", None))
                access_hash = str(user_data.get("user_id", None))
                file_size = str(user_data.get("file_size", None))

                photo_message = PhotoMessage(file_id=file_id, access_hash=access_hash, name="Bale", file_size='11337',
                                             mime_type="image/jpeg", caption_text=TextMessage(text="Bale"),
                                             file_storage_version=1, thumb=None)

                bot.send_message(photo_message, user_peer, success_callback=success, failure_callback=failure)

            bot.upload_file(file="media_url", file_type="file", success_callback=file_upload_success,
                            failure_callback=failure)

        message = TextMessage(
            ReadyMessage.tweet_message.format(tweet.get("text"),
                                              tweet.get("tweet_link"),
                                              tweet.get("name"), tweet.get("screen_name"),
                                              eng_to_arabic_number(tweet.get("favorite_count")),
                                              eng_to_arabic_number(tweet.get("retweet_count")),
                                              eng_to_arabic_number(tweet.get("datetime"))
                                              ))
        if a == len(time_line):
            btn_list = [TemplateMessageButton(text=TMessage.show_more, value=TMessage.show_more, action=0)]
            template_message = TemplateMessage(general_message=message, btn_list=btn_list)
            kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
            bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                             kwargs=kwargs)
            break
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        a += 1
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[TMessage.search]))
def get_search_text(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    user = get_user(user_id=user_id)
    if not check_user_registration(update, user_peer, user):
        return 0
    text_message = TextMessage(ReadyMessage.send_search_text)
    kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("info", info),
                                                        MessageHandler(TextFilter(), search_tweets),
                                                        MessageHandler(DefaultFilter(), start_conversation) ])


def search_tweets(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    query = update.get_effective_message().text
    user = get_user(user_id=user_id)
    statuses = search_api(final_oauth_token=user.final_oauth_token,
                          final_oauth_token_secret=user.final_oauth_token_secret, query=query)
    for status in statuses:
        media_url = status.get("media_url", None)
        height = status.get("height")
        width = status.get("width")
        if media_url:
            print("meddddddddddddiiiiiiiiiiiiiaaaaaaaaaaa")
            print(media_url)

            def file_upload_success(result, user_data):
                print("upload was successful : ", result)
                print(user_data)
                file_id = str(user_data.get("file_id", None))
                access_hash = str(user_data.get("user_id", None))
                file_size = str(user_data.get("file_size", None))

                photo_message = PhotoMessage(file_id=file_id, access_hash=access_hash, name="Bale", file_size='11337',
                                             mime_type="image/jpeg", caption_text=TextMessage(text="Bale"),
                                             file_storage_version=1, thumb=None)

                bot.send_message(photo_message, user_peer, success_callback=success, failure_callback=failure)

            bot.upload_file(file="media_url", file_type="file", success_callback=file_upload_success,
                            failure_callback=failure)

        message = TextMessage(
            ReadyMessage.tweet_message.format(status.get("text"),
                                              status.get("tweet_link"),
                                              status.get("name"), status.get("screen_name"),
                                              eng_to_arabic_number(status.get("favorite_count")),
                                              eng_to_arabic_number(status.get("retweet_count")),
                                              ))
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)

    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[TMessage.info]))
def info(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    btn_list = [TemplateMessageButton(text=TMessage.back, value=TMessage.back, action=0)]
    general_message = TextMessage(ReadyMessage.information)
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


updater.run()
