import telebot
from telebot import types
import logging
from config import *
from weather_api import *
from yandex_gpt import *
from database1 import *
from bs import *
from validators import *

users_city = {}

# настраиваем запись логов в файл
logging.basicConfig(filename=LOGS, level=logging.ERROR,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

bot = telebot.TeleBot(BOT_TOKEN)  # создаём объект бота


def menu_keyboard(options):
    """Создаёт клавиатуру с указанными кнопками."""  # создаём клавиатуру
    buttons = (types.KeyboardButton(text=option) for option in options)
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    keyboard.add(*buttons)
    return keyboard


# обрабатываем команду /start
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.from_user.id, "Привет! Я твой бот помощник в путешествиях, напиши мне свой город"
                                           "и я тебе расскажу о нём!", reply_markup=menu_keyboard(['/help', '/debug']))
    prepare_database()  # создаем базу для общения с GPT
    test = count_tokens_in_project(message)
    if test == True:
        bot.register_next_step_handler(message, what_doing)
    else:
        bot.send_message(message.chat.id, "Израсходован лимит токенов на проект!")


def what_doing(message: telebot.types.Message):
    users_city[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Выберите какую информацию вы хотите узнать!", reply_markup=menu_keyboard([
        '/description', "/weather", "/attractions", "/What_to_wear", "/about_attractions"]))


# обрабатываем команду /help
@bot.message_handler(commands=['help'])
def help_command(message: telebot.types.Message):
    bot.send_message(message.from_user.id, "Чтобы узнать больше о городе в который ты направляешься или находишься,"
                                           " то просто отправь мне название города :)")


# обрабатываем команду /debug - отправляем файл с логами
@bot.message_handler(commands=['debug'])
def debug(message: telebot.types.Message):
    with open(LOGS, "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=['description'])
def description(message: telebot.types.Message):
    try:
        user_id = message.from_user.id
        try:
            status, pic = city_pic(users_city[user_id])
            if not status:
                bot.send_message(user_id, pic)
                return
            bot.send_photo(user_id, pic)  # отвечаем пользователю текстом
        except Exception as e:
            logging.error(e)
            bot.send_message(message.from_user.id, "Не получилось найти картинку или город написан неправильно")

        status_gpt, answer_gpt, tokens_in_answer, tokens_in_prompt, prompt = ask_gpt(
            [{'role': 'user', 'text': f"{users_city[user_id]}"}],
            prompt=DESCRIPTION_CITY)

        regestration_for_assistent(user_id=user_id, role="assistent",
                                   content=answer_gpt, tokens=tokens_in_answer, stt_blocks=0)
        regestration_for_people(user_id=user_id, role="user", content=str(prompt), tokens=tokens_in_prompt,
                                stt_blocks=0)

        # обрабатываем ответ от GPT
        if not status_gpt:
            answer = get_answer(user_id)
            # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
            bot.send_message(user_id, answer)
            return
        answer = get_answer(user_id)
        bot.send_message(user_id, text=answer)  # отвечаем пользователю текстом

    except Exception as e:
        logging.error(e)  # если ошибка — записываем её в логи
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")
        bot.send_photo(message.chat.id, open("C:\\Users\\USER\\Desktop\\Не так что-то пошло.jpg"))


@bot.message_handler(commands=['weather'])
def weather_2(message: telebot.types.Message):
    try:
        user_id = message.from_user.id
        status, description, temp, humidity = weather(users_city[user_id])
        # обрабатываем ответ от GPT
        if not status:
            # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
            bot.send_message(user_id, description)
            return

        bot.send_message(user_id, f"Погода в городе:\n{description}\n{temp}\n{humidity}")  # отвечаем пользователю текстом

    except Exception as e:
        logging.error(e)  # если ошибка — записываем её в логи
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")
        bot.send_photo(message.chat.id, open("C:\\Users\\USER\\Desktop\\Не так что-то пошло.jpg"))


@bot.message_handler(commands=["attractions"])
def attraction(message: telebot.types.Message):
    try:
        user_id = message.chat.id
        status_gpt, answer_gpt, tokens_in_answer, tokens_in_prompt, prompt = ask_gpt(
            [{'role': 'user', 'text': f"{users_city[user_id]}"}],
            prompt=IF_WHERE_GO_TO)

        regestration_for_assistent(user_id=user_id, role="assistent",
                                   content=answer_gpt, tokens=tokens_in_answer, stt_blocks=0)
        regestration_for_people(user_id=user_id, role="user", content=str(prompt), tokens=tokens_in_prompt,
                                stt_blocks=0)
        # обрабатываем ответ от GPT
        if not status_gpt:
            answer = get_answer(user_id)
            # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
            bot.send_message(user_id, answer)
            return
        answer = get_answer(user_id)
        bot.send_message(user_id, text=answer)  # отвечаем пользователю текстом

    except Exception as e:
        logging.error(e)  # если ошибка — записываем её в логи
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")
        bot.send_photo(message.chat.id, open("C:\\Users\\USER\\Desktop\\Не так что-то пошло.jpg"))


@bot.message_handler(commands=["What_to_wear"])
def wear(message: telebot.types.Message):
    try:
        user_id = message.chat.id
        temp = only_temp(users_city[message.chat.id])
        status_gpt, answer_gpt, tokens_in_answer, tokens_in_prompt, prompt = ask_gpt(
            [{'role': 'user', 'text': f"{temp}"}],
            prompt=IF_WEATHER_CLOTHES)

        regestration_for_assistent(user_id=user_id, role="assistent",
                                   content=answer_gpt, tokens=tokens_in_answer, stt_blocks=0)
        regestration_for_people(user_id=user_id, role="user", content=str(prompt), tokens=tokens_in_prompt,
                                stt_blocks=0)

        # обрабатываем ответ от GPT
        if not status_gpt:
            answer = get_answer(user_id)
            # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
            bot.send_message(user_id, answer)
            return
        answer = get_answer(user_id)
        bot.send_message(user_id, text=answer)

    except Exception as e:
        logging.error(e)  # если ошибка — записываем её в логи
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")
        bot.send_photo(message.chat.id, open("C:\\Users\\USER\\Desktop\\Не так что-то пошло.jpg"))


@bot.message_handler(commands=['about_attractions'])
def about(message):
    bot.send_message(message.chat.id, "Скажите, какая именно достопримечательность вас интересует?")
    bot.register_next_step_handler(message, say_about)


def say_about(message):
    try:
        user_id = message.chat.id
        try:
            status, pic = city_pic(message.text)
            if not status:
                bot.send_message(user_id, pic)
                return
            bot.send_photo(user_id, pic)  # отвечаем пользователю текстом
        except Exception as e:
            logging.error(e)
            bot.send_message(message.from_user.id, "Не получилось найти картинку или город написан неправильно")

        status_gpt, answer_gpt, tokens_in_answer, tokens_in_prompt, prompt = ask_gpt(
            [{'role': 'user', 'text': f"{message.text}"}],
            prompt=DESCRIPTION_ATTRACTION)

        regestration_for_assistent(user_id=user_id, role="assistent",
                                   content=answer_gpt, tokens=tokens_in_answer, stt_blocks=0)
        regestration_for_people(user_id=user_id, role="user", content=str(prompt), tokens=tokens_in_prompt,
                                stt_blocks=0)

        # обрабатываем ответ от GPT
        if not status_gpt:
            answer = get_answer(user_id)
            # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
            bot.send_message(user_id, answer)
            return
        answer = get_answer(user_id)
        bot.send_message(user_id, text=answer)  # отвечаем пользователю текстом

    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось найти картинку или город написан неправильно")


@bot.message_handler(content_types=['audio'])
def audio(message):
    bot.send_message(message.chat.id, "Бот не может воспринимать сообщения такого формата.")


@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, "Бот не может воспринимать сообщения такого формата.")


bot.polling()
