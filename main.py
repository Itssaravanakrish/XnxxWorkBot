


import random
import logging

from moviepy.editor import VideoFileClip
from PIL import Image
from pyrogram import filters, Client, types
from scrappy import Porn


logging.basicConfig(level=logging.INFO)




porn = Porn()
app = Client(
   name="xnxxwork",
   api_id=28374181,
   api_hash="00b7ca7f535e816590db39e76f85d0c7",
   bot_token="7673638763:AAGuJ0XJ6oZ6E1b63Hjoqcvsl8ovYnDoVjk"
   
)


temp = {}



def resize_image(path: str):
   img = Image.open(path)
   img.thumbnail((320, 240))  # Resize to 320x240
   img.save(path)


@app.on_callback_query()
async def _callback_query(bot, query: types.CallbackQuery):
    query_data = query.data
    user = query.from_user


    if query_data.startswith("download"):
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
        await msg.edit("😍 **Successfully downloadable link scrapped now trying to download the file** 😋 🍆 ⚡ **Please wait processing....**")
        
        print(video)
        if "error" in video:
        	    return await msg.edit(f"❌ **Error: {video['error']}**")
        download_url = video["download_url"]
        
        filename = result["title"] + ".mp4"

        
        try:
           video_data = await porn.download(download_url, filename)
        except Exception as e:
        	    return await msg.edit(f"😓 **Sorry the wget module got a error while downloading....** `{e}`")

        clip = VideoFileClip(video_data["path"])
        duration = int(clip.duration)
        video_title = result['title']

        image_group = []

        await msg.edit("**💋 Taking Screenshotsn.... **")
        for _ in range(1, 6):           
            path = f"{video_title}_screenshot_{_}.jpg"
            image_group.append(types.InputMediaPhoto(path))
            clip.save_frame(path, t=random.randint(30, duration))
            resize_image(path)
                           
        await msg.edit("👅 **Successfully Screenshot taken now trying to upload.....**")

        try:
            await msg.reply_media_group(media=image_group, quote=True)
        except Exception as e:
             await msg.reply_text("❌ ERROR When Uploading Screenshots: {e}".format(e))

        
        await msg.edit("🥒 **Uploading Video please A wait ....**")
        caption = f"**Video: {video_title} Successfully downloaded by @{bot.me.username}**"
      
        await query.message.reply_video(
             video=video_data['path'],
             duration=duration, 
             thumb=open(random.choice(image_group), "rb"),
             caption=caption
        )
        await msg.edit("**Join @NandhaBots Dude! XD**")

    	    	
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
                )
                button = types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton("Next ⏩", callback_data=f"next:{token}:{index}"),
                            types.InlineKeyboardButton("Back ⏮️", callback_data=f"back:{token}:{index}"),
                        ],
                        [
                            types.InlineKeyboardButton("Get Preview 😋", callback_data=f"preview:{token}:{index}"),
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
                )
                button = types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton("Next ⏩", callback_data=f"next:{token}:{index}"),
                            types.InlineKeyboardButton("Back ⏮️", callback_data=f"back:{token}:{index}"),
                        ],
                        [
                            types.InlineKeyboardButton("Get Preview 😋", callback_data=f"preview:{token}:{index}"),
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
	         
	         if len(msg_txt.split()) < 2:
	         	     return await message.reply("```\n/search query```\n**Use this format to search though!**")
	         else:
	         	     
	         	     query = message.text.split(maxsplit=1)[1]
	         	     results = await porn.search(query)
	         	     token = porn.get_token()
	         	     
	         	     if 'error' in results:
	         	      	    return await message.reply(results['error'])
	         	     if user.id in temp:
	         	      	     await message.reply("**Cleared your previous query search data...**", quote=True)
	         	      	     
	         	     temp[user.id] = token, results
	         	     query, results = temp[user.id]
	         	     
	         	     result = results[0]
	         	     caption = (
	         	         f"😍 **Name**: 😜 {result['title']}"
	         	         f"\n⏳ **Total Duration**: 👄 {result['duration']}"
	         	     )
	         	     
	         	     button = types.InlineKeyboardMarkup(
	         	         [[ 
	         	             types.InlineKeyboardButton("Next ⏭️", callback_data=f"next:{token}:0"),
	         	              ], [
                           types.InlineKeyboardButton("Get Preview 😋", callback_data=f"preview:{token}:0"),
                        ], [
                           types.InlineKeyboardButton("Download 👅", callback_data=f"download:{token}:0")       
	         	         ]]
	         	     )
	         	     await message.reply_photo(
	         	           photo=result['thumb'],
	         	           caption=caption,
	         	           reply_markup=button,
	         	           quote=True
	         	     )
	         	           
	         	           
app.run()
                                
	         	      	   
	         	   
	         
	         

