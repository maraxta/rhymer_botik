# -*- coding: utf-8 -*-
#
#
# бот рифмовальщик
#
# чтобы запустить его без привязки к терминалу, надо
#
# export PYTHONIOENCODING=utf-8
# nohup python rhumer_botik.py &
#
# все, можно выходить, вывод будет находится в файлу ./nohup.out

# вау, чтобы работало автодополнение по нажатию Tab
# надо только поискать вопрос на SO: How do i add tab completion to python shell
#
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")
# конец автодополненния

import sys
sys.path.append('../elektrybalt/')


from time import sleep

# verse detector
import wd

import telebot
# RhymerBot
token = '405098465:AAHfeF-kBFK0WWc5DAPY4qVLctxxv-Loxqs'
helloString = u"""
Привет,
я бот рифмоплет, могу найти рифму к любому русскому слову,
ну или почти к любому

Просто введите слово и я отвечу рифмой
"""

#документация к TelegramBotAPI
bot = telebot.TeleBot(token)

# обработка комманд боту
@bot.message_handler(commands=["help", "setup", "start", "uups"])  # это декоратор
def DoCommand(message) :
   if message.text == "/help" or message.text == "/start" :
      bot.send_message(message.chat.id, helloString)
   elif message.text == "/setup":
      bot.send_message(message.chat.id, "oooouups")
   else :
      print 'Undefined command ', message.text
      bot.send_message(message.chat.id, 'undefined command')


# обработка входящих слов
@bot.message_handler(func=lambda message:True, content_types=["text"])  # это декоратор, вызывается для любого текста кроме комманд
def getRhymes(message): 
   last_word = wd.tokenize(message.text)[-1]
   print u'Получено слово :', last_word
   accented = wd.p.setAccent(last_word)
   # так как setAccent возвращает слово неизменным, если не сумел проставить ударение, то
   # грубо проверяем есть ли знак ударения в слове
   if u"'" in accented[0] :
      rhymes = wd.p.simpleRhyme(accented[0])
   else :
      bot.send_message(message.chat.id, u'Не могу проставить ударение в слове ' + last_word + u":(\nПопробуйте передать слово с апострофом ' после ударной гласной")
      return
   
   # телеграм не берет сообщения длиной больше чем 4096 символов
   # поэтому, если у нас большой список рифм, то разбиваем его на части по 50 слов
   #
   if len(rhymes) > 0 :
      ans = u"Ищем рифму к слову (" + accented[0] + u"): Всего найдено " +unicode(len(rhymes)) + u" вариантов\n"
      print u"): Всего найдено " +unicode(len(rhymes)) + u" вариантов\n"
      c = 0
      while c < len(rhymes) :
         ans += '\n'.join(rhymes[c: c+50])
         bot.send_message(message.chat.id, ans)
         ans = ""
         c += 50
         # телеграм банит, если отправить много сообщений одновременно, 
         # добавим задержку на секунду между сообщениями
         sleep(1)
   else :
      bot.send_message(message.chat.id, u'Не могу найти рифму к слову ' + accented[0] + u":(")
      print u'Не могу найти рифму к слову ' + accented[0] + u":("
   
   

if __name__ == '__main__':
   print 'Bot running'
   bot.polling(none_stop=True)

