import json
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time
import re
import datetime

from common import *

def main():
    for event in longpoll.listen():
        try:
            if len(event.raw) >=6:
                meta6 = event.raw[6]
                chat_id = event.raw[3] - 2000000000
                print('meta6: ' + str(meta6))
                if 'source_act' in meta6 and 'source_mid' in meta6 and 'from' in meta6:
                    output = {}
                    output['source_act'] = meta6['source_act']
                    output['source_mid'] = int(meta6['source_mid'])
                    output['source_name'] = get_user_name(output['source_mid'])
                    output['from'] = int(meta6['from'])
                    output['from_name'] = get_user_name(output['from'])

                    log_and_output(chat_id, output, 'acts')
                    #chat_id = event.chat_id
                    #№print(str(chat_id) + ': chat_kick_user ' + str(event.action['member_id']))
                    #with open(str(chat_id)+'-kicked.txt', 'a+') as f:
                    #  f.write(event.action['member_id'])
                    #   f.write('\n')
            for chat_id in CHAT_ID:                
                if event.chat_id == chat_id:
                    if event.type == VkEventType.MESSAGE_NEW:
                        fullname = get_user_name(event.user_id)

                        message_dict = {}
                        message_dict['from_name'] = fullname
                        message_dict['from_id'] = event.user_id
                        message_dict['text'] = event.text
                        message_dict['type'] = 'message'

                        current_time = datetime.datetime.now()
                        message_dict['timestamp'] = str(current_time)

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

                        current_time = datetime.datetime.now()
                        message_dict['timestamp'] = str(current_time)

                        print(str(chat_id) + ': ' + str(message_dict))
                        with open(str(chat_id)+'-log.txt', 'a+') as f:
                            f.write(str(message_dict))
                            f.write('\n')
                    
        except Exception as err:
            print(err)

if __name__ == '__main__':
    main()
