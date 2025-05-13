from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
import asyncio

# Замените 'API_ID' и 'API_HASH' на ваши значения
api_id = '22004760'
api_hash = 'a63bffce97b09560a2d3e17584215368'

# Замените на ссылку-приглашение и username или ID канала, куда пересылать сообщения
invite_link = '+https://t.me/+UQNbdVUqZTswYjcy'
destination_channel = '@Nik_LoL_kik'

# Создаем клиента
client = TelegramClient('session_name', api_id, api_hash)





async def parse_and_forward_messages(invite_link, destination_channel):


    # Замените на @username или ID вашего закрытого канала
    source_channel = -1002442254549
    async for message in client.iter_messages(source_channel, limit=1):  # Измените limit по необходимости
        try:
            # Пересылка сообщения в другой канал
            await client.send_message(destination_channel, message)
            print(f'Forwarded message: {message.text}')
            print(f'Forwarded message: {message.username_id}')
        except Exception as e:
            print(f'Failed to forward message: {e}')


async def main():
    await client.start()
    await parse_and_forward_messages(invite_link, destination_channel)


asyncio.run(main())
