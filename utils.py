import datetime
import locale
import logging
import random
import requests
import sqlite3
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import time

import config
from messages import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'tgbot.log'
                    )


def get_inline_keyboard():
    inlinekeyboard = [
        [InlineKeyboardButton('Одобрить', callback_data='approve'),
         InlineKeyboardButton('Отказать', callback_data='refuse')]]
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup


def get_reply_kb():
    keyboard = [[]]


def handle_var_inside_text(dictionary, key):
    text_list = dictionary[key]
    text = random.choice(text_list)
    return text
  

def create_user_base():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                       user_id      TEXT PRIMARY KEY, 
                       username     TEXT, 
                       access       TEXT)''' 
                    )
    conn.commit()
    conn.close()

def get_initial_data(update):    
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    initial_user_data = (user_id, username)
    return initial_user_data

def write_initial_data_to_base(data):
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (chat_id, first_name) VALUES (?, ?)', data)
    conn.commit()
    conn.close()

def write_entry_to_base(stage, entry, id):
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET {stage}=? WHERE chat_id=?', (entry, id))
    conn.commit()
    conn.close()    

def list_from_base_column(column): # Возвращает список значений столбца
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users')
    column_list = cursor.fetchall()
    conn.commit()
    conn.close()    
    return column_list # [('-yGIB7rf?NKU0Dk',), (None,)]

def get_date_string(column, chat_id):
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users WHERE chat_id=?', (chat_id,))
    date_list = cursor.fetchone()
    conn.commit()
    conn.close()    
    date_list = date_list[0].split(', ') 
    print(date_list)   
    return date_list

def get_data_cell(column, chat_id):
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users WHERE chat_id=?', (chat_id,))
    date_list = cursor.fetchone()
    conn.commit()
    conn.close()               
    return date_list[0]


def is_subscriber(user_id):
    users_list = list_from_base_column('user_id')
    for user in users_list:
        if user_id == user[0]:
            return True
    return False



