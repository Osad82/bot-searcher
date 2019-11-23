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



    dp.add_handler(
        MessageHandler(Filters.regex('^(Запросить доступ к боту)$'), user_request_add_to_bot))

    dp.add_handler(approve_conv)
    dp.add_handler(CommandHandler('start', start))
    # dp.add_handler(CallbackQueryHandler(add_or_not_user_access))


    # webhook_domain = 'https://translatebot.ru'    
    # PORT = 5003

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