


import random
import os
import logging
import json

from moviepy.editor import VideoFileClip
from PIL import Image
from pyrogram import filters, Client, types
from scrappy import Porn


logging.basicConfig(level=logging.INFO)


CHANNEL_ID = -1002495787792

porn = Porn()

app = Client(
   name="xnxxwork",
   api_id=28374181,
   api_hash="00b7ca7f535e816590db39e76f85d0c7",
   bot_token="7673638763:AAGuJ0XJ6oZ6E1b63Hjoqcvsl8ovYnDoVjk",
   max_concurrent_transmissions=5
   
)


temp = {}


CHANNEL_BUTTON = types.InlineKeyboardMarkup(
  [[
    types.InlineKeyboardButton("🥵 Join My Channel", url="https://t.me/NandhaBots"),
  ]]
)

SHARE_URL = "tg://share?text=@XnxxxWorkBot%20is%20your%20ultimate%20gateway%20to%20the%20hottest%20adult%20content%21%20%F0%9F%94%A5%F0%9F%92%8B%20Whether%20you%27re%20craving%20something%20wild%20or%20want%20to%20indulge%20your%20deepest%20desires%2C%20we%27ve%20got%20it%20all%21%20%F0%9F%98%88%F0%9F%92%A6%0A%20%0A%20Join%20now%20and%20dive%20into%20a%20world%20of%20passion%20and%20pleasure%21%20%F0%9F%94%9E%F0%9F%92%83%20Ready%20to%20spice%20up%20your%20fantasies%3F%20%F0%9F%8D%91%F0%9F%94%A5%0A%20%0A%20%F0%9F%91%89%20%40XnxxxWorkBot%0A%20&url=https://t.me/xnxxxworkbot"
SHARE_BUTTON = types.InlineKeyboardMarkup(
  [[
    types.InlineKeyboardButton("🥵 Share Me", url=SHARE_URL),
    types.InlineKeyboardButton("🥵 My Dev", user_id=7402274873),
    
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
      
        await Qmsg.reply("😜 🥵 **Join @NandhaBots Honey!** 😋 😍", reply_markup=SHARE_BUTTON)
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
        await app.get_chat_member("@NandhaBots", user.id)
    except Exception as e:
        return await message.reply_text("😜 **Join @NandhaBots to use /search baby** 👻\n```python\n{error}```".format(error=str(e)), reply_markup=CHANNEL_BUTTON)

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

app.run()
	         	      	   
	         	   
	         
	         

