from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio
import os

# Ganti dengan API ID dan Hash Anda
api_id = '25438898'
api_hash = '67abead22ca1ea5561e7a7f281291df5'
phone_number = '+62895423078394'

client = TelegramClient('my_session', api_id, api_hash)

async def send_message_to_groups(message_text):
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            try:
                await client.send_message(dialog, message_text)
                print(f"Pesan dikirim ke grup")
            except Exception as e:
                print(f"Gagal mengirim pesan ke grup")

async def main():
    async with client:
        await client.start()
        print("Client created")

        if await client.is_user_authorized():
            print("Logged in successfully!")

            # Membaca isi file teks.txt
            file_path = 'bahan.txt'
            if not os.path.exists(file_path):
                print("File teks.txt tidak ditemukan!")
                return

            with open(file_path, 'r', encoding='utf-8') as file:
                message_text = file.read().strip()

            if not message_text:
                print("Pesan tidak boleh kosong!")
                return

            while True:
                await send_message_to_groups(message_text)
                print("Menunggu 15 detik sebelum mengirim pesan ulang...")
                await asyncio.sleep(15)
        else:
            await client.send_code_request(phone_number)
            code = input('Masukkan kode: ')
            try:
                await client.sign_in(phone_number, code)
            except SessionPasswordNeededError:
                password = input('Masukkan kata sandi Anda: ')
                await client.sign_in(password=password)
            print("Logged in successfully!")

# Start the event loop
asyncio.run(main())
