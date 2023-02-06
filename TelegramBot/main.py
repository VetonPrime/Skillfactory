import telebot

from config import TOKEN, money
from extensions import APIException, BankApi

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = '''Доброго времени суток!!
    Я круто конвертер валют, но надо правильно ввести запрос.
    Запрос долже выглядеть так: <имя валюты, цену которой хотите узнать> 
    <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.
    Доступные валюты пожно посмотреть в /values'''

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def send_values(message):
    text = 'Я могу конвертировать только следующие валюты:'
    for _ in money.keys():
        text += f'\n{_}'

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert_money(message):

    try:

        list_params = message.text.split()
        if len(list_params) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = list_params
        summa = BankApi.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Какая то непредвиденная ошибка \n{e}')
    else:
        bot.send_message(message.chat.id, f'В результате получаем {round(summa, 2)} в валюте {quote}')


bot.polling(none_stop=True)
