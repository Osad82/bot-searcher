import datetime
import locale
import logging
import random
import requests
import sqlite3
from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, 
                      ParseMode, ReplyKeyboardMarkup)
import time

from config import *
from messages import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'tgbot.log'
                    )


def get_inline_keyboard(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    real_name = get_data_cell('real_name', user_id)
    access = get_data_cell('access', user_id)
    inlinekeyboard = [
        [InlineKeyboardButton(
            'Одобрить', callback_data=f'yes, {str(user_id)}, {username}, {real_name}, {access}'),
         InlineKeyboardButton(
             'Отказать', callback_data=f'no, {str(user_id)}, {username}, {real_name}, {access}')]]
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup


def get_pass_inline_keyboard():
    inlinekeyboard = [
        [InlineKeyboardButton('Пропустить шаг', callback_data='passs')]
         ]
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup


def get_reply_kb(user_id):
    if user_id == TG_ADMIN_ID:
        keyboard = [[]]
        kb = ReplyKeyboardMarkup(keyboard)        
    else:
        keyboard = [['Запросить доступ к боту']]
        kb = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)    
    return kb



def handle_var_inside_text(dictionary, key):
    text_list = dictionary[key]
    text = random.choice(text_list)
    return text
  

def create_user_base():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                       user_id      INTEGER PRIMARY KEY, 
                       username     TEXT, 
                       real_name    TEXT,
                       access       TEXT)''' 
                    )
    conn.commit()
    conn.close()


def get_initial_data(update):    
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    access = 'no'
    initial_user_data = (user_id, username, access)
    return initial_user_data


def write_initial_data_to_base(data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, access) VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()


def write_entry_to_base(column, entry, user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET {column}=? WHERE user_id=?', (entry, user_id))
    conn.commit()
    conn.close()    


def list_from_base_column(column): # Возвращает список значений столбца
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users')
    column_list = cursor.fetchall()
    conn.commit()
    conn.close()    
    return column_list # [('-yGIB7rf?NKU0Dk',), (None,)]

def get_data_string(column, user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users WHERE user_id=?', (user_id,))
    data_list = cursor.fetchone()
    conn.commit()
    conn.close()             
    return data_list

def get_data_cell(column, user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users WHERE user_id=?', (user_id,))
    date_list = cursor.fetchone()
    conn.commit()
    conn.close()               
    return date_list[0]


def is_subscriber(user_id):
    users_list = list_from_base_column('user_id, access')
    for user in users_list:
        check_user_id, access = user
        if check_user_id == user_id:
            if access == 'yes':                
                return True    
    return False


def save_target_user_data_to_context(update, context):
    query = update.callback_query
    _, target_user_id, target_username, real_name, access = (query.data).split(', ')
    context.user_data['target_user_id'] = target_user_id
    context.user_data['target_username'] = target_username
    context.user_data['real_name'] = real_name
    context.user_data['access'] = access
    





if __name__ == "__main__":
    # p = get_data_string('*', TG_ADMIN_ID)
    is_subscriber(TG_ADMIN_ID)
    # pass
