#!/usr/bin/env python3
import asyncio
import os
import sys
from telethon import TelegramClient
import re
import keyring
import json
from datetime import datetime
import pytz

channel = sys.argv[1]
cutoff_date = datetime.strptime(sys.argv[2], '%Y-%m-%d').replace(tzinfo=pytz.utc) if len(sys.argv) > 2 else datetime(2000,1,1, tzinfo=pytz.utc)
output = channel.split('/')[-1] + '.json'

def get_api_info(name, message, cast=str):
	if name in os.environ:
		return os.environ[name]

	keyring_value = keyring.get_password("tg_api", name)
	if keyring_value:
		return keyring_value

	while True:
		value = input(message)
		try:
			return cast(value)
		except ValueError as e:
			print(e, file=sys.stderr)
			time.sleep(1)

session = os.environ.get('TG_SESSION', 'session')
api_id = get_api_info('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_api_info('TG_API_HASH', 'Enter your API hash: ') 

def get_link(chat_id, message_id):
	return f"https://t.me/c/{chat_id}/{message_id}"

with open(output, "w") as f:
	async def main():
		async with TelegramClient(session, api_id, api_hash) as client:
			entity = await client.get_entity(channel)
			async for message in client.get_messages(entity=entity):
				if message.date < cutoff_date:
					break
				result = {
					"url": get_link(message.chat_id, message.id), 
					"date": message.date.isoformat(),
					"views": message.views if message.views else 0,
					"forwards": message.forwards if message.forwards else 0,
					"replies": message.replies.replies if message.replies else 0,
				}
				reactions = {}
				if (message.reactions is not None):	
					for reaction in message.reactions.results:
						reactions[reaction.reaction] = reaction.count
				result["reactions"] = reactions	
				f.write(json.dumps(result)+'\n')

	asyncio.run(main())


