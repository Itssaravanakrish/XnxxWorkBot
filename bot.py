from pyrogram.methods.utilities.idle import idle
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from bs4 import BeautifulSoup
from asyncio import sleep as asyncsleep
from aiohttp import ClientSession
from aiohttp import web
from shutil import rmtree
from os.path import exists
from requests import get
import re
from tools import download, extractImg, extractSeconds
import random
import os
import logging
import json
from os import environ,getenv
from moviepy.editor import VideoFileClip
from PIL import Image
from pyrogram import filters, Client, types
from scrappy import Porn


PORT = getenv("PORT", "8080")
NAME_APP = getenv("NAME_APP")
API_HASH = getenv("API_HASH", "00b7ca7f535e816590db39e76f85d0c7")
API_ID = getenv("API_ID", "28374181")
BOT_TOKEN = getenv("BOT_TOKEN", "8025985068:AAFaA-FmxgZpTZ1Rz0DIHr37faG-AwLu4zU")

CHANNEL_ID = -1002316696001

porn = Porn()

if exists('./Debug.py'):
    from Debug import BOT_TOKEN, PORT, API_HASH, API_ID
    print("MODO DEBUG")
    DEBUG = True
else:
    print("MODO ONLINE")
    DEBUG = False

app = Client(name='searchxxx', api_hash=API_HASH,
             api_id=API_ID, bot_token=BOT_TOKEN)

# =============================================================== RESPUESTAS
# @app.on_message()
# def fun(app, message):
#     print(message)


temp = {}


CHANNEL_BUTTON = types.InlineKeyboardMarkup(
  [[
    types.InlineKeyboardButton("🥵 Join My Channel", url="https://t.me/venuma"),
  ]]
)

SHARE_URL = "tg://share?text=@XnxxDown_Bot%20is%20your%20ultimate%20gateway%20to%20the%20hottest%20adult%20content%21%20%F0%9F%94%A5%F0%9F%92%8B%20Whether%20you%27re%20craving%20something%20wild%20or%20want%20to%20indulge%20your%20deepest%20desires%2C%20we%27ve%20got%20it%20all%21%20%F0%9F%98%88%F0%9F%92%A6%0A%20%0A%20Join%20now%20and%20dive%20into%20a%20world%20of%20passion%20and%20pleasure%21%20%F0%9F%94%9E%F0%9F%92%83%20Ready%20to%20spice%20up%20your%20fantasies%3F%20%F0%9F%8D%91%F0%9F%94%A5%0A%20%0A%20%F0%9F%91%89%20%40XnxxxWorkBot%0A%20&url=https://t.me/XnxxDown_Bot"
SHARE_BUTTON = types.InlineKeyboardMarkup(
  [[
    types.InlineKeyboardButton("🥵 Share Me", url=SHARE_URL),
    types.InlineKeyboardButton("🥵 My Dev", user_id=7045923188),
    
  ]]
)

def resize_image(path: str):
   img = Image.open(path)
   img.thumbnail((320, 240))  # Resize to 320x240
   img.save(path)

@app.on_message(filters.command("mydata"))
async def _mydata(_, message):
     user = message.from_user
     if user.id in temp:
         data = temp[user.id]
         path = f"{user.full_name}_data.json"
         with open(path, "w+") as file:
               file.write(json.dumps(data[1]))
         await message.reply_document(document=path, caption=f"**{user.full_name}'s search data**")
     else:
         return await message.reply("I don't have any of your data yet.")

@app.on_message(filters.private & ~filters.command(["search", "mydata"]), group=10)
async def _Reply(_, message):
     return await message.reply_text("/search hot sexy girl")

@app.on_callback_query()
async def _callback_query(bot, query: types.CallbackQuery):
    query_data = query.data
    user = query.from_user


    if query_data.startswith("show"):
        _, CQtoken, CQindex = query_data.split(":")
        if user.id not in temp:
            return await query.answer("You haven't registered any search though!", show_alert=True)
        
        token, results = temp[user.id]
        
        if CQtoken != token:
            return await query.answer("This Query is expired please search again..", show_alert=True)
        
        result = results[int(CQindex)]
        await query.message.reply_text(str(result))
  
    elif query_data.startswith("download"):
        _, CQtoken, CQindex = query_data.split(":")
        if user.id not in temp:
            return await query.answer("You haven't registered any search though!", show_alert=True)
        
        token, results = temp[user.id]
        
        if CQtoken != token:
            return await query.answer("This Query is expired please search again..", show_alert=True)
        
        result = results[int(CQindex)]
        await query.message.delete()
      
        msg = await query.message.reply("😍 **Don't Panic Your requested video started to downloading so please wait hony...**")
        
        url = porn.base_url + result["link"]
			
        video = await porn.get_download_url(url)
        if "error" in video:
        	    return await msg.edit_text(text=str(video['error']))
        
        await msg.edit("😍 👅 **Successfully downloadable link scrapped now trying to download the file** 😋 🍆 **Please wait processing....** 🥶")
        Qmsg = await msg.reply_photo(photo=result["thumb"], caption="```\n📩 Downloading Video...```")
        await msg.delete()
      
        logging.info('Trying to download video: {%s}' % video.get("download_url"))
        download_url = video["download_url"]
        filename = result["title"] + ".mp4"
      
        video_data = await porn.download(download_url, filename)
        if "error" in video_data:
            return await Qmsg.edit_caption(caption=str(video_data['error']))
					
        clip = VideoFileClip(video_data["path"])
        duration = int(clip.duration)
        video_title = result['title']

        image_group = []

        await Qmsg.edit_caption(caption="**💋 💋 Taking Screenshotsn.... **")
      
        for _ in range(1, 8):           
            path = f"{video_title}_screenshot_{_}.jpg"
            image_group.append(types.InputMediaPhoto(path))
            clip.save_frame(path, t=random.randint(10, duration))
            resize_image(path)
                           
        await Qmsg.edit_caption(caption="👅 **Successfully Screenshot Taken Now Trying To Upload.....** 😋")

        try:
            await Qmsg.reply_media_group(media=image_group, quote=True)
        except Exception as e:
             await Qmsg.reply_text("❌ **ERROR When Uploading Screenshots**: {error}".format(error=str(e)))

        
        await Qmsg.edit_caption(caption=f"👅 💋 **Uploading {video_title} Video please wait 🥴 🥵 🥴....**")
        caption = f"**Video: {video_title} Downloaded by {'@' + user.username if user.username else user.full_name} -** ( `{user.id}` ) **Video duration time {round(duration/60, 2)} Minutes**"
      
        video = await Qmsg.reply_video(
             video=video_data['path'],
             duration=duration, 
             thumb=open(random.choice(image_group).media, "rb"),
             caption=caption
        )
      
        if video:
             await video.copy(CHANNEL_ID, caption=caption)
      
        await Qmsg.reply("😜 🥵 **Join @Venuma Honey!** 😋 😍", reply_markup=SHARE_BUTTON)
        await Qmsg.delete()
        

        if os.path.exists(video_data["path"]):
             os.remove(video_data["path"])
    	    	
    elif query_data.startswith("preview"):
        _, CQtoken, CQindex = query_data.split(":")
        if user.id not in temp:
            return await query.answer("You haven't registered any search though!", show_alert=True)
        
        token, results = temp[user.id]
        
        if CQtoken != token:
            return await query.answer("This Query is expired please search again..", show_alert=True)
        
        result = results[int(CQindex)]
        video_url = result['preview']
        await query.message.reply_video(video_url, caption=result["title"])
        
        emoji = random.choice(["💋","🥒","😋", "😜","🍆"])
        await query.message.reply(emoji)
    
    elif query_data.startswith("back"):
        _, CQtoken, CQindex = query_data.split(":")
        if CQindex == "0":
            return await query.answer("You can't go further back...", show_alert=True)

        if user.id in temp:
            token, results = temp[user.id]
            if CQtoken == token:
                index = int(CQindex) - 1
                result = results[index]
                caption = (
                    f"😍 **Name**: 😜 {result['title']}"
                    f"\n⏳ **Total Duration**: 👄 {result['duration']}"
                    f"\n🗂️ **Index no**: {index}"
                )
                button = types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton("Next ⏩", callback_data=f"next:{token}:{index}"),
                            types.InlineKeyboardButton("Back ⏮️", callback_data=f"back:{token}:{index}"),
                        ],
                        [
                            types.InlineKeyboardButton("Preview 😋", callback_data=f"preview:{token}:{index}"),
			    types.InlineKeyboardButton("Data 📩", callback_data=f"show:{token}:{index}"),

                           ], [
                           types.InlineKeyboardButton("Download 👅", callback_data=f"download:{token}:0")       
	         	         
                        ]
                    ]
                )
                await query.edit_message_media(
                    media=types.InputMediaPhoto(media=result['thumb'], caption=caption),
                    reply_markup=button
                )
            else:
                return await query.answer("The token is expired please make new search", show_alert=True)
        else:
            return await query.answer("You haven't registered any query!", show_alert=True)

    elif query_data.startswith("next"):
        _, CQtoken, CQindex = query_data.split(":")
        if user.id in temp:
            token, results = temp[user.id]
            if int(CQindex) == len(results) - 1:
                return await query.answer("You can't go further")
              
            if CQtoken == token:
                index = int(CQindex) + 1
                result = results[index]
                caption = (
                    f"😍 **Name**: 😜 {result['title']}"
                    f"\n⏳ **Total Duration**: 👄 {result['duration']}"
                    f"\n🗂️ **Index no**: {index}"
                )
                button = types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton("Next ⏩", callback_data=f"next:{token}:{index}"),
                            types.InlineKeyboardButton("Back ⏮️", callback_data=f"back:{token}:{index}"),
                        ],
                        [
                            types.InlineKeyboardButton("Preview 😋", callback_data=f"preview:{token}:{index}"),
			    types.InlineKeyboardButton("Data 📩", callback_data=f"show:{token}:{index}"),
				
                          ], [
                           types.InlineKeyboardButton("Download 👅", callback_data=f"download:{token}:0")       
	         	         
                        ]
                    ]
                )
                await query.edit_message_media(
                    media=types.InputMediaPhoto(media=result['thumb'], caption=caption),
                    reply_markup=button
                )
            else:
                return await query.answer("The token is expired please make new search", show_alert=True)
        else:
            return await query.answer("You haven't registered any query!", show_alert=True)

	                   	             
	          


@app.on_message(filters.command("search") & filters.private)
async def _search(bot, message: types.Message):
    msg_txt = message.text
    user = message.from_user

    try:
        await app.get_chat_member("@Venuma", user.id)
    except Exception as e:
        return await message.reply_text("😜 **Join @Venuma to use /search baby** 👻\n```python\n{error}```".format(error=str(e)), reply_markup=CHANNEL_BUTTON)

    if len(msg_txt.split()) < 2:
        return await message.reply("```\n/search query```\n**Use this format to search though!**")

    else:
      
        query = message.text.split(maxsplit=1)[1]
        results = await porn.search(query)
        token = porn.get_token()

        if 'error' in results:
            return await message.reply(results['error'])

        if user.id in temp:
            await message.reply("**🗑️ Cleared your previous query search data results...**", quote=True)

        temp[user.id] = token, results
        query, results = temp[user.id]

        result = results[0]
        index = 0
        caption = (
            f"😍 **Name**: 😜 {result['title']}"
            f"\n⏳ **Total Duration**: 👄 {result['duration']}"
            f"\n🗂️ **Index no**: {index}"
        )

        button = types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("Next ⏭️", callback_data=f"next:{token}:{index}"),
                ],
                [
                    types.InlineKeyboardButton("Preview 😋", callback_data=f"preview:{token}:{index}"),
                    types.InlineKeyboardButton("Data 📩", callback_data=f"show:{token}:{index}"),
                ],
                [
                    types.InlineKeyboardButton("Download 👅", callback_data=f"download:{token}:{index}")
                ]
            ]
        )

        await message.reply_photo(
            photo=result['thumb'],
            caption=caption,
            reply_markup=button,
            quote=True
        )

@app.on_message(filters.regex('https://www.xnxxx.work.com') & filters.user('Sunnivenuma'))
def mostrar_info(app, message):
    """
    La función `mostrar_info` descarga un video, lo sube a un canal de Telegram, extrae imágenes del
    video, envía las imágenes a otro canal de Telegram y elimina los archivos temporales.
    
    :param app: El parámetro "app" es probablemente una instancia de un cliente de Telegram, como la
    clase `TelegramClient` de la biblioteca `Telethon`. Se utiliza para interactuar con la API de
    Telegram y realizar acciones como enviar mensajes, cargar medios, etc
    :param message: El parámetro `mensaje` es un objeto que representa el mensaje recibido por la
    aplicación. Contiene información como el texto del mensaje, el remitente y otros metadatos
    """
    
    if '/s/' or '/best/' in message.text:
        html = get(message.text).content
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.find_all("a")
        for element in elements:
            if 'href="/video' in str(element) and 'data-src=' in str(element):
                link = 'https://www.xnxx.work.com' + \
                    str(element).split('<a href="')[-1].split('"')[0]

                sms = message.reply('**Downloading video...**')
                file = download(link)
                
                sms.edit_text('Uploading video...')
                video = app.send_video(-1002316696001, file[0], duration=extractSeconds(file[0]), thumb=file[1])
                sms.edit_text('**Extracting images...**')
                list_img = extractImg(file[0], message)
                
                caption = show_metadata(link)
                caption += f"\n\n**🔥 [DOWNLOAD VIDEO](https://t.me/c/{2316696001}/{video.id}) 🔥**"
                
                sms.edit_text('**Sending images...**')
                media = app.send_media_group(-1002316696001, list_img)
                media[-1].edit_caption(caption)
                
        message.reply('**ALL TASK COMPLETED**')
        return 
    
    sms = message.reply('**Downloading video...**')
    file = download(message.text)
    
    sms.edit_text('Uploading video...')
    video = app.send_video(-1002316696001, file[0], duration=extractSeconds(file[0]), thumb=file[1])

    sms.edit_text('**Extracting images...**')
    list_img = extractImg(file[0], message)
    
    caption = show_metadata(message.text)
    caption += f"\n\n**🔥 [DOWNLOAD VIDEO](https://t.me/c/{1515779942}/{video.id}) 🔥**"
    
    sms.edit_text('**Sending images...**')
    media = app.send_media_group(-1002316696001, list_img)
    media[-1].edit_caption(caption)
    
    sms.delete()
    rmtree(message.from_user.username)

@app.on_inline_query()
async def handle_inline_query(client, query):
    """
    La función `handle_inline_query` toma una consulta de búsqueda, realiza web scraping para obtener
    enlaces y crea resultados de consultas en línea con los enlaces obtenidos.

    :param client: El parámetro `cliente` es una instancia de la clase de cliente que se utiliza para
    interactuar con la API de Telegram. Es responsable de enviar y recibir mensajes, realizar llamadas
    API y manejar otras interacciones con la plataforma Telegram
    :param query: El parámetro `query` es un objeto que representa la consulta en línea realizada por un
    usuario. Contiene información como el texto de la consulta, el usuario que realizó la consulta y
    otros detalles relevantes
    """
    results = []
    search_query = query.query.strip()

    # Verifica si la consulta no está vacía
    if search_query:
        # Realiza el web scraping y obtiene los enlaces
        enlaces = scrape_links(search_query)

        # Crea los resultados de la consulta inline con los enlaces obtenidos
        for i, data in enumerate(enlaces[0]):
            results.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=data[2],
                    description=f'Page: {enlaces[1]}',
                    input_message_content=InputTextMessageContent(data[0]),
                    thumb_url=data[1]
                )
            )
    try:
        await client.answer_inline_query(query.id, results)
    except:
        pass


def scrape_links(search_query):
    """
    La función `scrape_links` toma una consulta de búsqueda como entrada y extrae enlaces e imágenes de
    los resultados de búsqueda en xnxx.com.

    :param search_query: La consulta de búsqueda es el término o frase que desea buscar en el sitio web.
    Puede ser cualquier valor de cadena que desee utilizar como consulta de búsqueda
    :return: La función `scrape_links` devuelve una lista de tuplas. Cada tupla contiene tres elementos:
    el enlace a un video en xnxx.com, la imagen asociada con el video y el título del video.
    """
    pag = 0
    if search_query.split(' ')[-1].isdigit():
        pag = search_query.split(' ')[-1]
        url = f"https://www.xnxxx.work.com/search/{search_query.lower().split(' ')[0]}/{pag}"

    else:
        url = f"https://www.xnxx.work.com/search/{search_query.lower()}"

    html = get(url).content
    soup = BeautifulSoup(html, "html.parser")
    all = set()
    elements = soup.find_all("a")
    for element in elements:
        if 'href="/video' in str(element) and 'data-src=' in str(element):
            link = 'https://www.xnxxx.work.com' + \
                str(element).split('<a href="')[-1].split('"')[0]
            img = str(element).split('data-src="')[-1].split('"')[0]
            name = link.split('/')[-1].replace('_', ' ').capitalize()

            all.add((link, img, name))

    return all, pag


def show_metadata(url: str):
    """
    La función `show_metadata` toma una URL como entrada, recupera el contenido HTML de la URL, extrae
    información de metadatos como el título, la duración, la resolución y las vistas del HTML utilizando
    BeautifulSoup y devuelve una cadena formateada que contiene los metadatos extraídos.

    :param url: El parámetro `url` es la URL de una página web que contiene metadatos sobre un video
    :return: La función `show_metadata` devuelve una cadena que contiene los metadatos de una URL dada.
    Los metadatos incluyen el título, la duración, la resolución, las vistas y las etiquetas del video.
    """
    html = get(url).content
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find('div', class_='clear-infobar')
    txt = ''
    txt += '🎬 **Title: ' + f"`{info.find('strong').text}`**\n"

    patronmin = r'(\d+)\s*(min)'
    patronsec = r'(\d+)\s*(sec)'

    metadata = info.find('span', class_='metadata').text.replace(
        '\t', '').split('-')

    if metadata[0].replace('\n', '').endswith('min'):
        txt += '⏱️ **Duration: ' + '`' + \
            re.findall(patronmin, metadata[0])[0][0] + ' Min`**\n'
    elif metadata[0].replace('\n', '').endswith('sec'):
        txt += '⏱️ **Duration: ' + '`' + \
            re.findall(patronsec, metadata[0])[0][0] + ' Sec`**\n'

    txt += '**📺 Resolution: ' + '`' + metadata[1].replace(' ', '') + '`**\n'
    txt += '**🌎 Views: ' + '`' + metadata[2].replace(' ', '') + '`**\n\n'

    txt += '**🏷️ Tags: **'
    for i in soup.find_all('a', class_='is-keyword'):
        txt += '#' + i.text.replace(' ', '_') + ' '

    return txt


# =============================================================== SERVER
server = web.Application()
runner = web.AppRunner(server)


async def despertar(sleep_time=10 * 60):
    while True:
        await asyncsleep(sleep_time)
        async with ClientSession() as session:
            async with session.get(f'https://{NAME_APP}.onrender.com/' + "/Despiertate"):
                pass


async def run_server():
    await app.start()
    print('Bot Iniciado')
    # Iniciando User Bot
    await runner.setup()
    print('Iniciando Server')
    await web.TCPSite(runner, host='0.0.0.0', port=PORT).start()
    print('Server Iniciado')

if __name__ == '__main__':
    app.loop.run_until_complete(run_server())
    if not DEBUG:
        app.loop.run_until_complete(despertar())
    idle()
