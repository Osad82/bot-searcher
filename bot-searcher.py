import logging

from telegram import InlineQuery
from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, \
        MessageHandler, RegexHandler, Filters, CallbackQueryHandler
from telegram.ext import messagequeue as mq

from config import *
from handlers import *
from messages import *
import utils



logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )


    

    




mybot = Updater(TOKEN, use_context=True)

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
    dp.add_handler(
        MessageHandler(Filters.text & (~ Filters.user(TG_ADMIN_ID)), send_all_user_messages_to_admin)
        )
    dp.add_handler(approve_conv)
    dp.add_handler(CommandHandler('send_invitation', send_invitation))
    dp.add_handler(CommandHandler('new_user', user_request_add_to_bot))
    dp.add_handler(CommandHandler('help', help_message))

    dp.add_handler(MessageHandler(Filters.user(TG_ADMIN_ID), send_admin_message_to_user))
    
    dp.add_handler(CallbackQueryHandler(add_or_not_user_access))


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