from telegram.ext import ConversationHandler

from config import *
from google_utils import get_list_of_rows, search
from utils import *





# Человек находит бота в поисковике или переходит по ссылке. “Этот бот 
# делает то-то и то-то. Чтобы получить к нему доступ, нажмите кнопку СТАРТ внизу.”

# НАЖАЛ СТАРТ. 

# Ему сообщение: Чтобы получить доступ к базе, сперва пообщайтесь с админом. 

# ПИШЕТ АДМИНУ. Админ отвечает… после разговора -- хорошо, 
# чтобы получить доступ к боту нажмите /new_user

# НАЖАЛ. Админу приходит сообщение в котором он одобряет его… и тут же вносит 
# имя пользователя, по которому потом можно будет его вытягивать из базы для удаления. 
# Человеку приходит уведомление, что его одобрили и он теперь может искать в базе. 





def start(update, context):    
    data = get_initial_data(update)
    write_initial_data_to_base(data)
    update.message.reply_text(msg_start)


def send_all_user_messages_to_admin(update, context):        
    text = update.message.text        
    user_id = update.message.from_user.id    
    context.bot.send_message(
        chat_id=TG_ADMIN_ID,
        text=text
    )
    # context.user_data['target_user_id'] = user_id
        

def send_admin_message_to_user(update, context):    
    text_full = update.message.text
    target_user_id = text_full.split(';;; ')[-1]
    context.bot.send_message(
        chat_id=target_user_id, 
        text=update.message.text
    )



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

    name = get_kb_real_name(update, context)
    context.bot.send_message(
        chat_id=TG_ADMIN_ID, 
        text=f'Пользователь {name} (id {user_id}) хочет подписаться на бот. Одобрить?',
        reply_markup=get_inline_keyboard(update, context)
    )


def user_search(update, context):
    user_id = update.message.from_user.id
    if is_subscriber(user_id) == True:
        update.message.reply_text('Введите ФИО для поиска в базе')
        return '1'

    else:
        update.message.reply_text(
            'Вы не подписаны. Чтобы подписаться, обратитесь к админу',
            reply_markup=get_reply_kb(user_id))
        return ConversationHandler.END
    

def send_search_result(update, context):
    all_list = get_list_of_rows(SPREADSHEET_URL)
    result_list = search(all_list, update.message.text)
    if len(result_list) == 0:
        update.message.reply_text('Ничего не найдено. Попробуйте другой запрос или /cancel для отмены')
        return '1'    

    for result in result_list:
        text = msg_search_result(result)        
        update.message.reply_text(text)
    return ConversationHandler.END
    

def block_user_start(update, context):    
    user_id = update.message.from_user.id

    if user_id != TG_ADMIN_ID:
        update.message.reply_text('Функционал доступен только админу')
        return ConversationHandler.END

    update.message.reply_text(
        'Введите реальное имя пользователя, которого надо удалить (как в записной книжке)',
        reply_markup=get_reply_kb(user_id))
    return '1'


def send_matched_users(update, context):
    user_id = update.message.from_user.id
    real_name = update.message.text
    msg = msg_searched_users_to_block(real_name)
    if len(msg) == 0:
        update.message.reply_text('Не найдено совпадений. Задайте другие данные')
        return '1'

    else:
        update.message.reply_text(msg)
        update.message.reply_text(
            'Впишите id пользователя, которого нужно удалить или \
/cancel, чтобы выйти из режима поиска',
        reply_markup=get_reply_kb(user_id))
        return '2'


def block_user(update, context):
    user_id = update.message.from_user.id
    target_user_id = update.message.text
    write_entry_to_base('access', 'no', target_user_id)
    update.message.reply_text(
        f'Пользователь с id {target_user_id} больше не имеет доступа к боту',
        reply_markup=get_reply_kb(user_id))
    return ConversationHandler.END



def cancel_conv(update, context):
    update.message.reply_text('Режим диалога завершён')
    return ConversationHandler.END



def get_id_to_delete(update, context):
    pass





if __name__ == "__main__":
    pass
