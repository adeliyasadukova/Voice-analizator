import aiohttp
import asyncio
import io
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, Voice

#ключи
audio_key_id: str = "t2bOjiv3DcUCDW55"
audio_key_secret: str = "G9x3pPW6IxQ31WrA"
#id бота
bot = Bot(token="7136833015:AAHDZMFeUCjQ0mc2XlswXbG2FRDLXIo-DYQ")
dp = Dispatcher()
router: Router = Router()

async def recognize_audio(file_path):
    try:
        print("Start recognizing audio...")
        headers = {"keyId": audio_key_id, "keySecret": audio_key_secret}
        create_url = "https://api.speechflow.io/asr/file/v1/create?lang=ru"
        query_url_base = "https://api.speechflow.io/asr/file/v1/query?taskId={}&resultType=4"

        print("Reading audio file...")
        with open(file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        #url-запрос
        print("Sending audio file for recognition...")
        async with aiohttp.ClientSession() as session:
            async with session.post(create_url, headers=headers, data={'file': audio_content}) as response:
                if response.status == 200:
                    create_result = await response.json()
                    task_id = create_result.get("taskId")
                    if task_id:
                        print("Waiting for recognition results...")
                        query_url = query_url_base.format(task_id)
                        while True:
                            async with session.get(query_url, headers=headers) as query_response:
                                if query_response.status == 200:
                                    query_result = await query_response.json()
                                    if query_result.get("code") == 11000 and query_result.get("result"):
                                        result = query_result["result"].replace("\n\n", " ")
                                        print("Recognition successful!")
                                        return result
                                    elif query_result.get("code") == 11001:
                                        await asyncio.sleep(3)
                                        print("Retrying recognition...")
                                        continue
                                    else:
                                        print("Recognition failed.")
                                        return None
                                else:
                                    print("Failed to get recognition results.")
                                    return None
                    else:
                        print("Failed to create recognition task.")
                        return None
    except Exception as e:
        print(f"Error during audio recognition: {e}")
        return None

async def save_voice_for_speechflow(bot: Bot, voice: Voice) -> str:
    """Скачиваем голосовое сообщение и сохраняем в формате ogg."""
    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)
    voice_ogg.seek(0)

    # Создаем каталог для сохранения аудио, если он не существует
    directory = 'voice_files'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Создаем файл для сохранения аудио в формате ogg
    voice_ogg_path = f"{directory}/voice-{voice.file_unique_id}.ogg"
    with open(voice_ogg_path, "wb") as f:
        f.write(voice_ogg.read())

    print("Voice saved for Speechflow.")
    return voice_ogg_path


@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    """Принимаем все голосовые сообщения и транскрибируем их в текст."""
    print("Voice message received.")
    voice_path = await save_voice_for_speechflow(bot, message.voice)

    # Отправляем аудиофайл на распознавание с помощью Speechflow
    transcript = await recognize_audio(voice_path)

    if transcript:
        print("Transcription successful.")
        await message.reply(text=transcript)
    else:
        print("Transcription failed.")


async def main():
    dp.include_router(router)
    print("Bot started polling.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
