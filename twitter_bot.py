from balebot.filters import TemplateResponseFilter, TextFilter, DefaultFilter, LocationFilter
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.base_models import Peer, Location
from balebot.models.constants.peer_type import PeerType
from balebot.models.messages import TemplateMessageButton, TextMessage, TemplateMessage, JsonMessage
from balebot.models.messages.location_message import LocationMessage
from balebot.updater import Updater
from balebot.utils.logger import Logger
from bot_config import BotConfig
from constant.message import ReadyMessage, TMessage, LogMessage, Regex
from db.db_handler import create_all_table, insert_user, get_user
import asyncio

from twitter_api import get_verify_link, send_tweet_api, final_verify

updater = Updater(token=BotConfig.bot_token,
                  loop=asyncio.get_event_loop())
bot = updater.bot
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


@dispatcher.message_handler(
    filters=[TemplateResponseFilter(keywords=[TMessage.start, TMessage.back]), TextFilter(keywords="start")])
def start_conversation(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id

    general_message = TextMessage(ReadyMessage.start_conversation)
    btn_list = [TemplateMessageButton(text=TMessage.send_tweet, value=TMessage.send_tweet, action=0),
                TemplateMessageButton(text=TMessage.get_time_line, value=TMessage.get_time_line, action=0),
                TemplateMessageButton(text=TMessage.send_direct, value=TMessage.send_direct,
                                      action=0),
                TemplateMessageButton(text=TMessage.info, value=TMessage.info, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    my_logger.info(LogMessage.info, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.send_tweet),
                                                            get_tweet_text),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.info),
                                                            info)
                                                        ])


@dispatcher.command_handler(["/adduser"])
def add_user(bot, update):
    dispatcher.clear_conversation_data(update)
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    text_message = TextMessage(ReadyMessage.send_name)
    kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    my_logger.info(LogMessage.start, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.back),
                                                            start_conversation),
                                                        MessageHandler(TextFilter(), get_name)])


def get_name(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    name = update.get_effective_message().text
    dispatcher.set_conversation_data(update, "name", name)
    text_message = TextMessage(ReadyMessage.send_phone_number)
    kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    my_logger.info(LogMessage.start, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.back),
                                                            start_conversation),
                                                        MessageHandler(TextFilter(), get_phone_number)])


def get_phone_number(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    phone_number = update.get_effective_message().text
    dispatcher.set_conversation_data(update, "phone_number", phone_number)
    auth = get_verify_link()
    dispatcher.set_conversation_data(update, "auth", auth)
    verify_link = auth['auth_url']
    text_message = TextMessage(ReadyMessage.send_verify_number.format(verify_link))
    kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    my_logger.info(LogMessage.start, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(TextFilter(), verify)])


def verify(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    auth = dispatcher.get_conversation_data(update, "auth")
    oauth_verifier = update.get_effective_message().text
    access_hash = user_peer.access_hash
    name = dispatcher.get_conversation_data(update, "name")
    phone_number = dispatcher.get_conversation_data(update, "phone_number")
    print(auth['oauth_token'])
    print(auth['oauth_token_secret'])

    final_dict = final_verify(oauth_verifier=oauth_verifier, oauth_token=auth['oauth_token'],
                              oauth_token_secret=auth['oauth_token_secret'])

    result = insert_user(name=name, user_id=user_id, access_hash=access_hash, phone_number=phone_number,
                         final_oauth_token=final_dict.get("final_oauth_token"),
                         final_oauth_token_secret=final_dict.get("final_oauth_token_secret"))
    if not result:
        text_message = TextMessage(ReadyMessage.fail_insert_user)

        kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        my_logger.info(LogMessage.start, extra={"user_id": user_id, "tag": "info"})
        dispatcher.finish_conversation(update)
        return None
    general_message = TextMessage(ReadyMessage.success_insert_user)

    btn_list = [TemplateMessageButton(text=TMessage.send_tweet, value=TMessage.send_tweet, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)

    my_logger.info(LogMessage.start, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.send_tweet),
                                                            get_tweet_text),
                                                        ])


@dispatcher.message_handler(TemplateResponseFilter(keywords=[TMessage.send_tweet]))
def get_tweet_text(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    text_message = TextMessage(ReadyMessage.send_text_twitter)
    kwargs = {"message": text_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success, failure_callback=failure,
                     kwargs=kwargs)
    my_logger.info(LogMessage.start, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.back),
                                                            start_conversation),
                                                        MessageHandler(TextFilter(), send_tweet)])


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
    my_logger.info(LogMessage.info, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update,
                                                       [CommandHandler("start", start_conversation),
                                                        CommandHandler("info", info),
                                                        MessageHandler(
                                                            TemplateResponseFilter(keywords=TMessage.back),
                                                            start_conversation)])


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
    my_logger.info(LogMessage.info, extra={"user_id": user_id, "tag": "info"})
    dispatcher.finish_conversation(update)


updater.run()
