from config import *
from utils import *



def start(update, context):
    user_id = update.message.from_user.id
    if is_subscriber(user_id):
        # Вытянуть из базы все его данные и сохранить в контекст
        pass
    else:
        get_initial_data(update)
    user_start_handler(update, context)
    admnin_notification(update, context)
    






def admnin_notification(update, context):
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    context.bot.send_message(
        chat_id=TG_ADMIN_ID, 
        text=f'Пользователь {user_name}(id {user_id}) хочет подписаться на бот. Одобрить?',
        reply_markup=get_inline_keyboard()
    )


def user_start_handler(update, context):
    pass







if __name__ == "__main__":
    pass