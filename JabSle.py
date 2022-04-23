import random
from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message

@loader.tds
class frogkormMod(loader.Module):
	strings = {
		'name': 'JabSle',
		'kon': '<i>✅Отложенка создана, кормеж в ханей запущен...</i>',
		'kon_already': '<i>Уже запущено</i>',
		'koff': '<i>❌Автофарминг в ханей остановлен.\n🐞Надюпано буках:</i>',
	}
	
	def __init__(self):
		self.name = self.strings['name']
		
	async def client_ready(self, client, db):
		self.client = client
		self.db = db
		self.myid = (await client.get_me()).id
		self.honey = 798765050
		
	async def koncmd(self, message):
		running = True
		while running:
			status = self.db.get(self.name, "status", False)
			if status: return await message.edit(self.strings['kon_already'])
			self.db.set(self.name, "status", True)
			await self.client.send_message(self.honey, "Покормить жабу", schedule=timedelta(seconds=20))
			await self.client.send_message(self.honey, "Завершить работу", schedule=timedelta(seconds=20))
			await self.client.send_message(self.honey, "Работа грабитель", schedule=timedelta(seconds=20))
			await message.edit(self.strings['kon'])
		
	async def koffcmd(self, message):
		self.db.set(self.name, 'status', False)
		await message.edit(self.strings['koff'])
		
	
