# covert-chess-bot
Telegram bot to convert between chess positions and a unique emoji encoding. Primary instance of this bot is available via @CovertChessBot on Telegram. (please note that it may take several seconds to reply to the first command as it is running on a free heroku account)

To run this code yourself you need to complete the following steps:

1. create a telegram bot by contacting @BotFather on Telegram

2. enter the API token for your bot in to credentials.py (by filling in and renaming credentials_template.py)    
   optional: create a webhook, fill in relevant details for this in credentials.py (including setting webhook_active = True)

3. install dependencies by running 'pip install -r requirements.txt'

4. from the root folder of this repository run the command 'python3 -m covert-chess-bot'
