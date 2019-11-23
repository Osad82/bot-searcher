from telegram.ext import ConversationHandler

from config import *
from utils import *



def start(update, context):
    user_id = update.message.from_user.id
    data = get_initial_data(update)
    write_initial_data_to_base(data)
    update.message.reply_text(
        'Вы может подписаться на бот', 
        reply_markup=get_reply_kb(user_id))
        


def user_request_add_to_bot(update, context):
    user_id = update.message.from_user.id
    if is_subscriber(user_id):
        update.message.reply_text('Вы уже подпиисаны на бот')
    else:
        admin_notification(update, context)
        update.message.reply_text('Ваш запрос отправлен админу')

    
def add_or_not_user_access(update, context):
    query = update.callback_query
    if 'yes' in query.data:
        save_target_user_data_to_context(update, context)
        write_entry_to_base('access', 'yes', context.user_data['target_user_id'])
        context.bot.send_message(
            chat_id=TG_ADMIN_ID, 
            # text=f'Пользователю {target_username} разрешён доступ к боту'
            text=f'Введите реальное имя пользователя или пропустите этот шаг, если имя уже есть',
            reply_markup=get_pass_inline_keyboard()
        )
        return '1'

    if 'no' in query.data:
        save_target_user_data_to_context(update, context)
        write_entry_to_base('access', 'no', context.user_data['target_user_id'])
        context.bot.send_message(
            chat_id=TG_ADMIN_ID, 
            text=f'Пользователю {context.user_data["target_user_id"]} запрещён доступ к боту'
        )
        return ConversationHandler.END
    

def get_real_name(update, context):
    real_name = update.message.text
    target_user_id = context.user_data['target_user_id']
    write_entry_to_base('real_name', real_name, target_user_id)
    update.message.reply_text(f'Пользователь {real_name} добавлен')
    return ConversationHandler.END


def pass_get_real_name(update, context):
    target_user_id = context.user_data['target_user_id']
    if 'real_name' in context.user_data:
        real_name = context.user_data['real_name']
    else:
        real_name = get_data_cell('real_name', target_user_id)
    query = update.callback_query
    query.message.reply_text(f'Пользователь {real_name} добавлен')
    return ConversationHandler.END



def admin_notification(update, context):
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    context.bot.send_message(
        chat_id=TG_ADMIN_ID, 
        text=f'Пользователь {user_name} (id {user_id}) хочет подписаться на бот. Одобрить?',
        reply_markup=get_inline_keyboard(update, context)
    )



    







if __name__ == "__main__":
    pass