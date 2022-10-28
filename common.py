import json
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

ACCESS_TOKEN = ''

try:
    with open('token.txt') as f:
        ACCESS_TOKEN = f.readline()
except FileNotFoundError as err:
    print('create token.txt with access token, one line')

CHAT_ID = []

try:
    with open('chats.txt') as f:
        for line in f.readlines():
                CHAT_ID.append(int(line))
except FileNotFoundError as err:
    print('create chats.txt with chad ids, one id in one line')
except Exception as err:
    print(err)
    print('use one line for every chat id')

vk_session = VkApi(token=ACCESS_TOKEN,api_version='5.154')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

known_users = {}

def get_user_name(id):
    if id in known_users:
        return known_users[id]
    
    response = vk.users.get(user_ids = id)
    name = response[0]['first_name'] +  ' ' + response[0]['last_name']
    known_users[id] = name
    return name

def log_and_output(chat_id, output, name):
    print(str(chat_id) + ': ' + str(output))
    with open(str(chat_id) + '-' + name + '.txt', 'a+') as f:
        f.write(str(output))
        f.write('\n')

#conv_members = vk.messages.getConversationMembers(peer_id = 2000000000 + args.chat_id, count=1000, extended=1)