#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import json
from time import sleep
from urllib import urlopen, urlencode

BOT_NAME = 'ToledosPalaceBot'
BOT_TOKEN = open('.BOT_TOKEN', 'r').read().strip()
BOT_COMMANDS = ['/help', '/emcasa', '/status', '/fechar', '/abrir']
BOT_LAST_UPDATE = open('.LAST_UPDATE', 'r').read().strip()

API_URL = 'https://api.telegram.org/bot%s/' % BOT_TOKEN

def help():
   return """Bot criado por @leandrotoledo para interagir com Toledo's Palace.
/emcasa Retorna lista de quem esta em Toledo's Palace.
/status Informa se Toledo's Palace esta aberto ou fechado para o publico no momento.
/fechar Fechar Toledo's Palace para o publico.
/abrir Abrir Toledo's Palace para o publico."""

def emcasa():
   return u'@leandrotoledo esta em Toledo\'s Palace.\n @brunamarquezine esta em Toledo\'s Palace.'

def status():
   return u'Toledo\'s Palace esta fechado no momento.'

def fechar():
   return u'Toledo\'s Palace foi fechada.'

def abrir():
   return u'Toledo\'s Palace foi aberta.'

def getCommand(message):
   command = dict()

   if message:
      try:
         key, value = str(message.split()[0]), ' '.join(message.split()[1:])

         if key in BOT_COMMANDS:
            command[key.replace('/', '')] = value
      except UnicodeEncodeError:
         pass

   return command

def sendMessage(chat_id, message):
   params = urlencode(dict(chat_id=chat_id, text=message))
   result = urlopen(API_URL + 'sendMessage', params).read()

   return json.loads(result)['result']

def getUpdates():
   params = urlencode(dict(offset=int(BOT_LAST_UPDATE)))
   result = urlopen(API_URL + 'getUpdates', params).read()

   return json.loads(result)['result']

def main():
   global BOT_LAST_UPDATE

   while True:
      for update in getUpdates():
         if int(BOT_LAST_UPDATE) < update['update_id']:
            message = update['message'].get('text', None)
            command = getCommand(message)

            result = eval(command.keys()[0] + '()')
            if result:
               sendMessage(update['message']['chat']['id'], result)

            BOT_LAST_UPDATE = int(update['update_id'])
      sleep(3)

if __name__ == '__main__':
   try:
      main()
   except KeyboardInterrupt:
      with open('.LAST_UPDATE', 'wb') as f:
         f.write(str(BOT_LAST_UPDATE))

      raise
