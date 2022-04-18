import random
from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message

@loader.tds
class FarmIrisMod(loader.Module):
	"""Для автоматического фарминга коинов в ирисботе"""
	strings = {
		'name': 'FrogKorm',
		'frkoon': '<i>✅Отложенка создана, автофарминг запущен, всё начнётся через 20 секунд...</i>',
		'frkoon_already': '<i>Уже запущено</i>',
		'frkooff': '<i>❌Автофарминг остановлен.\n🐞Надюпано буках:</i> <b>%coins% i¢</b>',
		'buk': '<i>🐞Надюпано буках:</i> <b>%coins% i¢</b>',
	}
	
	def __init__(self):
		self.name = self.strings['name']
		
	async def client_ready(self, client, db):
		self.client = client
		self.db = db
		self.myid = (await client.get_me()).id
		self.honey = 1276392130
		
	async def frkooncmd(self, message):
		"""Запустить автофарминг"""
		status = self.db.get(self.name, "status", False)
		if status: return await message.edit(self.strings['frkoon_already'])
		self.db.set(self.name, "status", True)
		await self.client.send_message(self.honey, "Покормить жабу", schedule=timedelta(seconds=20))
		await message.edit(self.strings['frkoon'])
		
	async def frkooffcmd(self, message):
		"""Остановить автофарминг"""
		self.db.set(self.name, 'status', False)
		coins = self.db.get(self.name, 'coins', 0)
		if coins: self.db.set(self.name, 'coins', 0)
		await message.edit(self.strings['frkooff'].replace("%coins%", str(coins)))
		
	async def bukcmd(self, message):
		"""Вывод кол-ва коинов, добытых этим модулем"""
		coins = self.db.get(self.name, "coins", 0)
		await message.edit(self.strings['buk'].replace("%coins%", str(coins)))
	
	async def watcher(self, event):
		if not isinstance(event, Message): return
		chat = utils.get_chat_id(event)
		if chat != self.honey: return
		status = self.db.get(self.name, 'status', False)
		if not status: return
		if event.raw_text == "Покормить жабу":
			return await self.client.send_message(self.honey, "Покормить жабу", schedule=timedelta(minutes=random.randint(1, 20)))
		if event.sender_id != self.honey: return
		if "Дружище," in event.raw_text:
			args = [int(x) for x in event.raw_text.split() if x.isnumeric()]
			randelta = random.randint(20, 60)
			if len(args) == 4: delta = timedelta(hours=args[1], minutes=args[2])
			elif len(args) == 2: delta = timedelta(seconds=args[1]+randelta)
			else: return
			sch = (await self.client(functions.messages.GetScheduledHistoryRequest(self.honey, 1488))).messages
			await self.client(functions.messages.DeleteScheduledMessagesRequest(self.honey, id=[x.id for x in sch]))
			return await self.client.send_message(self.honey, 'Покормить жабу', schedule=delta)
		if "Вы успешно покормили жабу!" in event.raw_text:
			args = event.raw_text.split()
			for x in args:
				if x[0] == '+': 
					return self.db.set(self.name, 'coins', self.db.get(self.name, 'coins', 0) + int(x[1:]))
