'''
WARNING:
this file must be renamed to credentials.py and a valid variable values added 
before it will work correctly with the rest of the code.
'''

# file to be used to store credentials
# e.g. API keys & passwords

# make sure Credentials.py is added to .gitignore if adding this code to git
# otherwise credentials will be leaked to anyone with access to it

# how to use variables from this file:
'''
import credentials
imported_variable = credentials.variablename
'''

# Telegram HTTP API token
# can be generated or changed by contacting @BotFather on telegram
bot_token = "exampletoken"

# webhook information 

# set to True if using a webhook, False if running bot use polling
webhook_active = None

# as defined by telegram, this can be 80, 88, 443, or 8443
# but if using an external service with a reverse proxy (e.g. heroku) this
# may not be the case, check with that service to find out what it should be
webhook_port = None

# needs to be set to the URL that your webhook is set up on
webhook_url = "https://example.com/"