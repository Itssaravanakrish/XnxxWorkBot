
import os
import uuid
import aiohttp
import urllib
import httpx
import string
import random

from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs

class Porn:
    """
    A class for interacting with the xnxxx.work website.
    """

    def __init__(self):
        """
        Initialize the Porn class with the base URL.
        """
        self.base_url = "https://xnxxx.work"

    @staticmethod
    def get_token(length: int = 6) -> str:
    	      """ Returns 6 unique characters """
    	      
    	      characters = string.ascii_letters
    	      token = "".join(random.choice(characters) for _ in range(length))
    	      return token
    	
    @staticmethod
    def quote(text: str) -> str:
    		     """ Convert the text to Url safe string """
    		         		     
    		     quote = urllib.parse.quote(text)
    		     return quote

    @staticmethod
    def get_header() -> dict:
        """
        Generate a random User-Agent header.

        Returns:
            dict: A dictionary containing the User-Agent header.
        """
   
         
        user_agent = UserAgent()
        headers = {"User-Agent": user_agent.random}
        return headers

    @staticmethod
    async def download(download_url: str, filename: str = None) -> dict:
        """
        Download a file using the wget module.

        Args:
            download_url (str): The URL of the file to download.

        Returns:
            dict: A dictionary containing the file path.
        """

        try:
            async with httpx.AsyncClient() as client:
                  response = await client.get(download_url)
                  if response.status_code != 200:
                      return {"error": f"cant download the video: {response.text}"}
                  content = response.read()

                  if filename is None:
                       filename = str(uuid.uuid4()) + ".mp4"
                  with open(filename, "wb+") as file:
                       file.write(content)
                  return {"path": os.path.abspath(filename) }
        except Exception as error:
              return {"error": f"❌ ERROR: {error}"}

    async def get_download_url(self, url: str) -> str:
        """
        Get the downloadable URL for a video.

        Args:
            url (str): The URL of the video page.

        Returns:
            str: The downloadable URL or an error message.
        """
        try:
            async with httpx.AsyncClient() as session:
                 response = await session.get(url, headers=self.get_header())
                 if response.status_code != 200:
                    return {"error":  f"❌ ERROR: {str(response.text)}"}
                 soup = bs(response.text, "html.parser")
                 try:
                    source = soup.find_all("div", class_="video")[0].find("source").get("src")
                 except Exception as error:
                     return {"error": f"❌ Cant fetch download url ERROR: {error}"}
                 return {"download_url": source}

        except Exception as error:
               return {"error": f"❌ Cant fetch download url ERROR: {error}"}           
               
    async def search(self, query: str) -> list:
        """
        Search for videos on the xnxxx.work website.

        Args:
            url (str): The URL of the search page.

        Returns:
            list: A list of video metadata dictionaries.
        """
        
        url = f"https://xnxxx.work/bigtits-fuck?query={self.quote(query)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.get_header()) as response:
                if response.status != 200:
                    return [{"error": f"can't fetch data from {url} reason: {response.reason}"}]
                soup = bs(await response.text(), "html.parser")
                video_data = soup.find(class_="thumbs").find_all('li')
                formatted_data = [
                    {
                        "thumb": video.img["data-src"],
                        "preview": video.find(class_="thumb-img").get("data-preview-url"),
                        "title": video.p.text,
                        "link": video.a.get("href"),
                        "duration": video.find(class_="th-time").text
                    } for video in video_data
                ]
                return formatted_data


async def main():
    """
    The main function for searching and downloading videos.
    """
    porn = Porn()
    query = urllib.parse.quote(input("Query: "))
    video = await porn.search(f"")
    print(video)
    video = video[0]
    url = porn.base_url + video['link']
    download_data = await porn.get_download_url(url)
    print(download_data)

