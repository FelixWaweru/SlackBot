import os
import time
import smtplib
import random
from slackclient import SlackClient

BOT_ID = os.environ.get('BOT_ID')
slack_client = SlackClient(os.environ.get('BOT_TOKEN'))
AT_BOT = "<@" + BOT_ID + ">"
GREET = ("hi", "hello", "who are you?", "who are you")
HELP = "help"
SEND = "send"
JOKE = 'joke'
jokes = ["Why was the cat really fat? It was suffering from Obi-Kitty",
         "What did the bee say to the other bee? I'm sorry but bees can't talk",
         "Why did the monkey date the banana skin? Because he found it a peeling"]
ALL_COMMANDS = [HELP, SEND, JOKE, GREET]

#
# def firstInput():
#     firstResponse = "Hello. I am the Fast Efficient Live Instruction Xenter bot, or Felix2.0 for short. :) " \
#                    "If you are receiving this message it means that Felix is currently offline and " \
#                    "if you would like me to forward a message to him please type in *send" \
#                    "* followed by your message."
#     output_list = slack_client.rtm_read()
#     if output_list and len(output_list) > 0:
#         for output in output_list:
#             if output and 'text' in output and 'text' is not firstResponse:
#                 slack_client.api_call("chat.postMessage", channel=output['channel'], text=firstResponse, as_user=True)
#                 return output['text'], output['channel']
#                 del output
#                 break

#user='D5GA526UA'

def handle_command(command, channel):
    channel_list = []
    channel_list.append(channel)
    if command.startswith(GREET):
        responseA = "Hello. I am the Fast Efficient Live Instruction Xenter bot, or Felix2.0 for short. :) " \
                   "If you are receiving this message it means that Felix is currently offline and " \
                   "if you would like me to forward a message to him please type in *" + SEND + \
                   "* followed by your message."
        slack_client.api_call("chat.postMessage", channel=channel, text=responseA, as_user=True)
    elif command.startswith(HELP):
        responseB = "My name is Fast Efficient Live Instruction Xenter bot, or Felix2.0 for short. " \
                   ":) Type in my username followed by the following commands to carry out an action. \n" \
                   "eg @felix2.0 make eggs (I can't do that btw. Im too young to be around a stove unattended). \n" \
                   "Type in *" + SEND + "* followed by your message to send Felix an email containing the message. \n" \
                   "Type in *joke* to hear a joke my creator made. " \
                    "Type in *Hi*, *Hello* or *Who are you?* to learn " \
                    "about my secret origins and how in the billions of years of existence I ended up being here," \
                    " right now in the same time and universe as you."
        slack_client.api_call("chat.postMessage", channel=channel, text=responseB, as_user=True)
    elif command.startswith(SEND):
        fromaddr = 'felix@moringaschool.com'
        toaddr = 'felix@moringaschool.com'
        words = command.split(' ', 1)[1]
        #removes the command 'send' from the message
        subject = 'Moringa Slack Message! \n'
        msg = (subject + words)
        try:
            username = 'felix@moringaschool.com'
            password = os.environ.get('PASS')
            server = smtplib.SMTP(host='smtp.gmail.com', port='587')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            print("Connected.")
            server.sendmail(fromaddr, toaddr, msg)
            server.quit()
            responseC = "Email sent to Felix :simple_smile: . Anything else I can help you with?"
            slack_client.api_call("chat.postMessage", channel=channel, text=responseC, as_user=True)
        except:
            responseD = "Whoops. Something went wrong but try again in a bit and the odds may be in your favour. :pray:"
            slack_client.api_call("chat.postMessage", channel=channel, text=responseD, as_user=True)
    elif command.startswith(JOKE):
        randomizer = random.randint(0, 3)
        responseE = jokes[randomizer]
        slack_client.api_call("chat.postMessage", channel=channel, text=responseE, as_user=True)
    elif channel not in channel_list and slack_client.api_call("channels.join", channel= channel):
        responseG = "My name is Fast Efficient Live Instruction Xenter bot, or Felix2.0 for short. " \
                    ":) Type in my username followed by the following commands to carry out an action. \n" \
                    "eg @felix2.0 make eggs (I can't do that btw. Im too young to be around a stove unattended). \n" \
                    "Type in *" + SEND + "* followed by your message to send Felix an email containing the message. \n" \
                                         "Type in *joke* to hear a joke my creator made. " \
                                         "Type in *Hi*, *Hello* or *Who are you?* to learn " \
                                         "about my secret origins and how in the billions of years of existence I ended up being here," \
                                         " right now in the same time and universe as you."
        slack_client.api_call("chat.postMessage", channel=channel, text=responseG, as_user=True)
    else:
        responseF = "Not sure what you mean. Please type in *" + HELP + \
                    "* to figure out what I can do and how I can help you out."
        slack_client.api_call("chat.postMessage", channel=channel, text=responseF, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.api_call("users.getPresence", user='U5183G1U4', presence="active"):
        print("Online")
    elif slack_client.api_call("users.getPresence", user='U5183G1U4', presence="away"):
        print("Not")
    if slack_client.rtm_connect():
        print("StarterBot connected and running!\n Waiting for first input.")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            print(command,channel)
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
