import json
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time
import re

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

ACCESS_TOKEN = ''

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

def get_user_name(id):
    if id in known_users:
        return known_users[id]
    
    response = vk.users.get(user_ids = id)
    name = response[0]['first_name'] +  ' ' + response[0]['last_name']
    known_users[id] = name
    return name

def main():
    for event in longpoll.listen():
        try:
            for chat_id in CHAT_ID:
                if event.chat_id == chat_id:
                    if event.type == VkEventType.MESSAGE_NEW:
                        fullname = get_user_name(event.user_id)

                        message_dict = {}
                        message_dict['from_name'] = fullname
                        message_dict['from_id'] = event.user_id
                        message_dict['text'] = event.text
                        message_dict['type'] = 'message'

                        meta_data = event.raw[7]
                        if 'reply' in meta_data:
                            if 'mentions' in event.raw[6] and len(event.raw[6]['mentions']) > 0:
                                mention_id = event.raw[6]['mentions'][0]
                                message_dict['mention_id'] = mention_id
                                message_dict['mention_name'] = get_user_name(mention_id) 
                            else:
                                message_dict['mention_id'] = event.user_id
                                message_dict['mention_name'] = fullname

                            reply_data = meta_data['reply']
                            parsed = json.loads(reply_data)
                            repy_id = parsed['conversation_message_id']

                            message_dict['type'] = 'reply'
                            reply_to = vk.messages.getByConversationMessageId(peer_id = event.peer_id, conversation_message_ids = str(repy_id))
                            
                            message_dict['conversation_message_id'] = repy_id
                            message_dict['conversation_message'] = reply_to['items'][0]['text']

                        print(str(chat_id) + ': ' + str(message_dict))
                        with open(str(chat_id)+'-log.txt', 'a+') as f:
                            f.write(str(message_dict))
                            f.write('\n')

                    if event.type == event.type == VkEventType.MESSAGE_EDIT:
                        fullname = get_user_name(event.user_id)

                        message_dict = {}
                        message_dict['from_name'] = fullname
                        message_dict['from_id'] = event.user_id
                        message_dict['text'] = event.text
                        message_dict['type'] = 'edit'

                        print(str(chat_id) + ': ' + str(message_dict))
                        with open(str(chat_id)+'-log.txt', 'a+') as f:
                            f.write(str(message_dict))
                            f.write('\n')
                    
        except Exception as err:
            print(err)

if __name__ == '__main__':
    main()
