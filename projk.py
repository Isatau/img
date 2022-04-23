import random
from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message

@loader.tds
class frogkormMod(loader.Module):
	strings = {
		'name': 'FrogKorm',
		'frkoon': '<i>✅Отложенка создана, кормеж в ханей запущен, всё начнётся через 20 секунд...</i>',
		'frkoon_already': '<i>Уже запущено</i>',
		'frkooff': '<i>❌Автофарминг в ханей остановлен.\n🐞Надюпано буках:</i>',
	}
	
	def __init__(self):
		self.name = self.strings['name']
		
	async def client_ready(self, client, db):
		self.client = client
		self.db = db
		self.myid = (await client.get_me()).id
		self.honey = 1276392130
		
	async def frkooncmd(self, message):
		status = self.db.get(self.name, "status", False)
		if status: return await message.edit(self.strings['frkoon_already'])
		self.db.set(self.name, "status", True)
		await self.client.send_message(self.honey, "Покормить жабу", schedule=timedelta(hours=8))
		await message.edit(self.strings['frkoon'])
		
	async def frkooffcmd(self, message):
		self.db.set(self.name, 'status', False)
		await message.edit(self.strings['frkooff'])
		
	
