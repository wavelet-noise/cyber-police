from dataclasses import fields
from common import *
import sys
import argparse

kick_parserer = argparse.ArgumentParser(description='cyber-police command line interface')

kick_parserer.add_argument(
    '--kick',
    type = int,
    help = 'user id',
    required = False
)

kick_parserer.add_argument(
    '--chat_info',
    help = 'show chat info',
    required = False
)

kick_parserer.add_argument(
    'chat_id',
    type = int,
    help = 'chat id'
)

args = kick_parserer.parse_args()

if args.chat_info: 
    result = vk.messages.getConversationMembers(peer_id = 2000000000 + args.chat_id, count=1000, extended=1)
    print(json.dumps(result, indent=4))

if args.kick:
    print('kick ' + str(args.kick) + ' from ' + str(args.chat_id))
    vk.messages.removeChatUser(chat_id = args.chat_id, user_id = args.kick)