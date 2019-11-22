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
    
    # Инициализируем MessageQueue 
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается.')    

    dp = mybot.dispatcher
    

    dp.add_handler(CallbackQueryHandler(output_format_handler, pattern='text'))
    dp.add_handler(CommandHandler('start', start))


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