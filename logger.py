from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

ACCESS_TOKEN = ""

with open('token.txt') as f:
    ACCESS_TOKEN = f.readline()

CHAT_ID = []

with open('chats.txt') as f:
    for line in f.readlines():
        try:
            CHAT_ID.append(int(line))
        except Exception as err:
            print(err)


vk_session = VkApi(token=ACCESS_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

known_users = {}

def get_user_name(event):
    if event.user_id in known_users:
        return known_users[event.user_id]
    
    response = vk.users.get(user_ids = event.user_id)
    name = response[0]['first_name'] +  ' ' + response[0]['last_name']
    known_users[event.user_id] = name
    return name

def main():
    for event in longpoll.listen():
        try:
            for chat_id in CHAT_ID:
                if event.type == VkEventType.MESSAGE_NEW and event.chat_id == chat_id:
                    fullname = get_user_name(event)

                    message_tuple = (fullname, event.user_id, event.text)
                    print('chat ' + str(chat_id) + ': ' + str(message_tuple))
                    with open(str(chat_id)+'-log.txt', 'a+') as f:
                        f.write(str(message_tuple))
                        f.write('\n')
        except Exception as err:
            print(err)

if __name__ == '__main__':
    main()
