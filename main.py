from pygame import mixer
import soundfile as sf
import sounddevice as sd
from twitchio.ext import commands
from twitchio.ext import routines
import random
import configparser
from elevenlabslib import *
from art import *


tprint("Menace's twitch text to speech", "small")

twitchUsers = {'menaceirl': 'VFIf6PK3SZDyOyZBctyg', 'kiteit': 'DdQjjMSusdM74m7jB7kb'}

#import settings
config = configparser.ConfigParser()
config.read('voiceconfig.ini')


Elabs_api_key = config.get('VOICES', 'api_key')
voice_idGlobal = config.get('VOICES', 'voice_id')
wingvoice_id = config.get('VOICES', 'wingvoice_id')
wingvoice = config.getboolean('VOICES', 'wingvoice')
volume = config.get('VOICES', 'volume')
speakFrequency = config.get('VOICES', 'speakFrequency')
twitchToken = config.get('VOICES', 'twitchToken')
botName = config.get('VOICES', 'botName')

#Bot class using twitchio
class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=twitchToken, prefix='!',
                         initial_channels=['bustin', 'menaceirl'])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        botNick = str(self.nick)
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

#Function to play audio files from elevenlabs
def speak(text = None, voice_id = voice_idGlobal):

    user = ElevenLabsUser(Elabs_api_key)
    voice = user.get_voice_by_ID(voice_id)
    voice.generate_and_stream_audio(text, streamInBackground=True)


#Cog to listen for messages and send them to the speak function
class MessageLogging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message):
            
        config = configparser.ConfigParser()
        config.read('voiceconfig.ini')

        Elabs_api_key = config.get('VOICES', 'api_key')
        voice_idGlobal = config.get('VOICES', 'voice_id')
        wingvoice_id = config.get('VOICES', 'wingvoice_id')
        wingvoice = config.getboolean('VOICES', 'wingvoice')
        volume = config.get('VOICES', 'volume')
        speakFrequency = config.get('VOICES', 'speakFrequency')
        twitchToken = config.get('VOICES', 'twitchToken')
        botName = config.get('VOICES', 'botName')

        print(f"{message.author.name}: {message.content}")
        
        #checks if the message is from the bot or the user is not youngbustin or wingofchicken (youngbustin was the name of our bot, wing was a moderator/tester)
        if not (message.author.name.lower() == "youngbustin" or (message.author.name.lower() == "wingofchicken"and wingvoice == True)):
            print("return cause 1")
            return
        if "model" in message.content.lower():
            print("return cause 2")
            return
        if len(message.content) > 400 or len(message.content) < 10:
            print("return cause 3")
            return

        readChance = random.randint(1, int(speakFrequency))
        print(f"Message roll {readChance}: {message.content}")
        if readChance == 1:
            speak(message.content, voice_idGlobal)


#initialise the bot
bot = Bot()
bot.add_cog(MessageLogging(bot))
bot.run()