EMOJI = {
    'target': '🎯',
    'money_bag': '💰',
    'money_with_wings': '💸',
    'calendar': '📅',
    'fire': '🔥',
    'wrapped_gift': '🎁',
    'megaphone': '📣',
    'sunglasses': '😎',
    'hand_right': '👉',
    'bar_chart': '📊',
    'ok_hand': '👌',
    'hand_pointing_down': '👇',
    'thumbs_up': '👍',
    'thinking_face': '🤔',
    'purse': '👛',
    'waving_hand': '👋',
    'money_mouth_face': '🤑',
    'trophy': '🏆',
    'winking_face': '😉',
    'foot': '👣',
    'double_exclamation_mark': '‼️',
    'shrug': '🤷<200d>♂️',
    'key': '🔑'
    
    }

def msg_search_result(row):    
    date, last_name, first_name, otchestvo, year_birthday, passport_num, \
    grazhdanstvo, adress_reg, adress_prozh, position, reason, who_add_entry, \
    dop_info = row

    text = f'''Дата: {date}
Фамилия: {last_name}
Имя: {first_name}	
Отчество: {otchestvo}
Год рождения: {year_birthday}
Номер паспорта: {passport_num}
Гражданство: {grazhdanstvo}
Адрес регистрации: {adress_reg}
Адрес проживания: {adress_prozh}
Позиция: {position}
Причина внесения: {reason}
Кто добавил запись: {who_add_entry}
Дополнительная информация: {dop_info}'''
    
    return text


msg_start = 'Чтобы получить доступ к базе, напишите админу (прямо здесь пишите). '


msg_send_invitation = 'Чтобы получить доступ к боту нажмите /new_user'


msg_no_result = '''Ничего не найдено. Попробуйте другой запрос. Вы можете указать \
общий запрос, например, Иванов. Также вы можете конкретизировать запрос, указав \
фамилию и имя, например, Иванов Александр'''


msg_user_id_to_delete = 'Впишите id пользователя, которого нужно удалить'


msg_approved_start_message = '''Админ одобрил ваш запрос. Теперь у вас есть доступ к \
базе. Доступны следующие команды:

/search — поиск по базе кандидатов'''





