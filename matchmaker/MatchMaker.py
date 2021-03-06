'''
Created on 25.02.2019

@author: Joshua Esselmann
@version: 1.2.2
'''

import json
import traceback
from discord.ext import commands
import logging
from logging.handlers import TimedRotatingFileHandler

class MatchMaker(commands.Bot):
    '''Wrapper for main Bot so Cogs can access logger and other features.
    '''

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.TimedRotatingFileHandler("SLBot.log",'midnight', 1, 5, 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    
    COMMANDS = ["1vs1","2vs2","mainChannel",
                "set","reset", "settings",
                "post", "commands", "help", "version",
                "restart", "roll", "reloadSettings",
                "debug", "testdebug"]
    
    def is_command(self, cmd):
        '''Return, if a command with this name exists.
        
        :param cmd: Command name
        '''
        if len(cmd.content) > 1 and cmd.content[0] == str(get_prefix(bot, cmd)):
                
            command = cmd.content[1:]
            
            mainCommand = command.split(" ", 1)[0]
            
            if mainCommand in self.COMMANDS:
                return True
        return False
    
    async def on_message(self, message):
        '''Gets called when messages are posted.
        
        Enables command processing, if valid command is used.
        '''
        if self.is_command(message):
            await self.process_commands(message)

  
SETTINGS_FILE = 'settings.json'
TOKEN_FILE = 'token.txt'
EXTENSIONS = ["Cogs.Controller", "Cogs.MatchMaking", "Cogs.Misc", "Cogs.CoinTournament", "Cogs.DiscordBotsOrgAPI"]

def get_prefix(bot, message):
    '''This method enables the use of custom Prefixes set by the user.
    
    returns ! as default.
    '''
    if message.guild is not None:
        serverid = str(message.guild.id)
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        
        if serverid in list(data) and 'PREFIX' in list(data[serverid]):
            prefix = data[serverid]['PREFIX']
        else:
            prefix = "!"
    else:
        prefix = "!"
    return prefix

bot = MatchMaker(command_prefix=get_prefix)
# using own implementation of the help command
bot.remove_command('help')

if __name__ == '__main__':      
    try:
        token = open(TOKEN_FILE,"r").readline()
        for ext in EXTENSIONS:
            bot.load_extension(ext)
        bot.run(token)
    except Exception as e:
        print(traceback.print_exc())
    
