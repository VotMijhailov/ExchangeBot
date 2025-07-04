import telebot
from config import keys, TOKEN
from extensions import ConversionException, ExchangeConverter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды /start или /help.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> \
<количество переводимой валюты>\n Показать список валют доступных для конвертации: /values')
    bot.reply_to(message, text)

# Обрабатывается команда /values - выводится список допустимых валют.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# Выводит ошибки пользователся в виде сообщения в чат.
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Параметров меньше или больше 3х!')

        quote, base, amount = values
        total_base = ExchangeConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользлвателя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()