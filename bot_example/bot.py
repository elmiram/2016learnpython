# -*- coding: utf-8 -*-
import telebot
import conf
import random
import shelve
from telebot import types

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

with open('reviews.csv', 'r', encoding='utf-8') as f:
    reviews = {}
    for line in f:
        num, text = line.strip().split('\t')
        reviews[num] = text
review_keys = list(reviews.keys())

keyboard = types.ReplyKeyboardMarkup(row_width=3)
btn1 = types.KeyboardButton('+')
btn2 = types.KeyboardButton('-')
btn3 = types.KeyboardButton('=')
keyboard.add(btn1, btn2, btn3)

shelve_name = 'shelve.db'  # Файл с хранилищем


def set_user_review(chat_id, review):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить.
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = review


def finish_user_review(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_user_review(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            review = storage[str(chat_id)]
            return review
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None


# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте! Это бот для разметки отзывов на кинофильмы.\n Положительные отзывы отмечаются плюсом +, отрицательные минусом -, а нейтральные знаком равно =.")


@bot.message_handler(commands=['start'])
def send_first_review(message):
    review_num = random.choice(review_keys)
    bot.send_message(message.chat.id, reviews[review_num], reply_markup=keyboard)
    set_user_review(message.chat.id, review_num)


@bot.message_handler(regexp='[-+=]')  # этот обработчик реагирует на символы разметки
def get_answer(message):
    review_num = get_user_review(message.chat.id)
    if review_num:
        with open('results.csv', 'a', encoding='utf-8') as results:
            results.write(review_num + '\t' + message.text + '\n')
        review_num = random.choice(review_keys)
        bot.send_message(message.chat.id, reviews[review_num], reply_markup=keyboard)
        set_user_review(message.chat.id, review_num)
    else:
        bot.send_message(message.chat.id, 'Вы не разметили отзыв.')


if __name__ == '__main__':
    bot.polling(none_stop=True)