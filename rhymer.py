# -*- coding: utf-8 -*-
#
#
# бот рифмовальщик

# вау, чтобы работало автодополнение по нажатию Tab
# надо только поискать вопрос на SO: How do i add tab completion to python shell
#
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")
# конец автодополненния

import sys
sys.path.append('../elektrybalt/')

import wd

import config
import telebot


bot = telebot.TeleBot(config.token)

@bot.message_handler(func=lambda message:True, content_types=["text"])
def reverse_all_messages(message): 
   last_word = wd.tokenize(message.text)[-1]
   accented = wd.p.setAccent(last_word)
   if len(accented) > 0 :
      rhymes = wd.p.simpleRhyme(accented[0])
   
   if len(rhymes) > 0 :
      ans = "Find rhymes for " + accented[0] + ":\n"
      ans += '\n'.join(rhymes)
   else :
      ans = 'Cannot find a rhyme for ' + accented[0] + ":("
   bot.send_message(message.chat.id, ans)
   

if __name__ == '__main__':
   print 'Bot running'
   bot.polling(none_stop=True)

