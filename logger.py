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

CHAT_ID = 0

with open('chats.txt') as f:
    CHAT_ID = int(f.readline())

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
            if event.type == VkEventType.MESSAGE_NEW and (event.chat_id == CHAT_ID or event.chat_id == CHAT_ID):
                fullname = get_user_name(event)

                message_tuple = (fullname, event.user_id, event.text)
                print(message_tuple)
                with open(str(CHAT_ID)+'-log.txt', 'a+') as f:
                    f.write(str(message_tuple))
                    f.write('\n')
        except Exception as err:
            print(err)

if __name__ == '__main__':
    main()
