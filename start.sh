# Don't Remove Credit @
# Subscribe YouTube Channel For Amazing Bot @
# Ask Doubt on telegram @

if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/TheDarkSaiyan/XnxxWorkBot.git /XnxxWorkBot 
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /XnxxWorkBot 
fi
cd /XnxxWorkBot 
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py, bot.py
