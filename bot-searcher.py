import logging
import sys

from threading import Thread
from telegram import InlineQuery
from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, \
        MessageHandler, RegexHandler, Filters, CallbackQueryHandler, PicklePersistence
from telegram.ext import messagequeue as mq

from config import *
from handlers import *
from messages import *

import error_handler
import utils




logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )


    
# my_persistence = PicklePersistence(filename='persistence_file', store_user_data=True)
# mybot = Updater(TOKEN, persistence=my_persistence, use_context=True)

mybot = Updater(TOKEN, use_context=True)

def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    mybot.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

def restart(update, context):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()


def main():   

    create_user_base()     
    
    # Инициализируем MessageQueue 
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается.')    

    dp = mybot.dispatcher
    

    approve_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_or_not_user_access)], 

        states={
            '1': [MessageHandler(Filters.text, get_real_name),
                  CallbackQueryHandler(pass_get_real_name, pattern='passs')]
        }, 

        fallbacks=[]
    )

    block_user_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Закрыть доступ)$'), block_user_start),
                      CommandHandler('delete', block_user_start)], 

        states={
            '1': [MessageHandler(Filters.text, send_matched_users),
                  CommandHandler('cancel', cancel_block_user)],

            '2': [MessageHandler(Filters.text, block_user), 
                  CommandHandler('cancel', cancel_block_user)]

            
        }, 

        fallbacks=[MessageHandler(Filters.text, fallback_block_user)]
    )





    search_conv = ConversationHandler(
        entry_points=[CommandHandler('search', user_search)], 

        states={
            '1': [MessageHandler(Filters.text, send_search_result),
                  CommandHandler('cancel', cancel_conv)]
        }, 

        fallbacks=[]
    )





    dp.add_handler(
        MessageHandler(Filters.regex('^(Запросить доступ к боту)$'), user_request_add_to_bot))

    dp.add_handler(CallbackQueryHandler(query_handler, pattern='^start_conv'))
    dp.add_handler(block_user_conv)
    dp.add_handler(search_conv)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(approve_conv)
    dp.add_handler(CommandHandler('send_invitation', send_invitation))
    dp.add_handler(CommandHandler('new_user', user_request_add_to_bot))
    dp.add_handler(CommandHandler('all_users', get_all_users))
    dp.add_handler(CommandHandler('help', help_message))
    dp.add_handler(CommandHandler('add', user_add_in_blocklist))

    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(DEV_ID)))
    dp.add_handler(CallbackQueryHandler(add_or_not_user_access))
    dp.add_error_handler(error_handler.error)

    dp.add_handler(MessageHandler(Filters.user(TG_ADMIN_ID), send_admin_message_to_user))
    dp.add_handler(
        MessageHandler(Filters.text & (~ Filters.user(TG_ADMIN_ID)), send_all_user_messages_to_admin)
        )



    # webhook_domain = 'https://python-developer.ru'    
    # PORT = 5015

    # mybot.start_webhook(listen='127.0.0.1',
    #                 port=PORT,
    #                 url_path=TOKEN,
    #                 webhook_url=f'{webhook_domain}/{TOKEN}'     
    #                 )

    # mybot.bot.set_webhook(f'{webhook_domain}/{TOKEN}')
    
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()