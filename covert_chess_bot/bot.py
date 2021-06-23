# ------------------------------------------------------------------------------
# Covert Chess Bot
# @CovertChessBot on Telegram
# https://t.me/CovertChessBot
# ------------------------------------------------------------------------------
# Author: Paul Frisby
# Email: mail@paulfrisby.com
# Github: https://github.com/paulfrisby/
# ------------------------------------------------------------------------------

import logging
import emoji
from covert_chess_bot import credentials, covert_chess

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    '''Send a message when a user uses the bot for the first time or the command /start is issued.'''
    user = update.effective_user
    update.message.reply_text(f'Hi {user.name}, welcome to the Covert Chess telegram bot!\nUse /commands for a list of availble commands.')
    
def unknown(update, context):
    '''Catches when user tries to use an unimplemented or misspelled command.'''
    update.message.reply_text('This is not a valid command, please use /commands for a list of available commands.')

def commands_command(update, context):
    '''Send a message explaining possible commands when command /commands or /help is issued.'''
    update.message.reply_text('''The commands available in this bot are:

/startgame - gives emoji encoding and FEN of a chess board in its starting state 

/encode (fen) - convert given chess position to emoji encoding of it

/decode (emojiString or mixedString) - decodes back to fen

/mix (emojiString or fen) (message=message) - mix emoji encoding in to a given block of text, returns mixed message

/extract (mixedString) - remove embedded emoji encoding from mixed message

/move (emojiString or fen) - sends lichess link allowing a move to be made in given position

/edit [emojiString or fen] - sends lichess link to edit a given position freely

/commands - what you just used!
    
n.b. required / optionalparameters are shown inside () or [] style brackets, but these are not necessary when actually inputting a command
''')

def emoji_info(update, context):
    '''When a user sends a single emoji message, sends info about that emoji'''
    
    # gets list of emojis from message
    messageEmojis = emoji.emoji_lis(update.message.text)
    
    # checks if there is exactly 1 emoji in message
    if len(messageEmojis) == 1:

        # get index of emoji in message
        emojiIndex = covert_chess.emojiIndex(messageEmojis[0]["emoji"])

        # checks if message is just the fully qualified emoji
        if update.message.text == covert_chess.emojiList[emojiIndex]:
            
            # get the dictionary entry for this emoji 
            emojiInfo = covert_chess.emojiInfo(emojiIndex)

            # build response using info from dictionary
            message = f'Emoji {emojiIndex}: {emojiInfo["emoji"]}\n'
            message += f'Name: {emojiInfo["name"]}\n'
            message += f'Group: {emojiInfo["group"]}\n'
            message += f'Subgroup: {emojiInfo["subgroup"]}\n'
            message += f'Escape Sequence: {emojiInfo["escape"]}'

            update.message.reply_text(message)

        # checks if message is just the minimally qualified emoji
        elif update.message.text == covert_chess.emojiListLessQualified[emojiIndex]:
            
            # get the dictionary entry for this emoji 
            emojiInfo = covert_chess.emojiInfo(emojiIndex)

            # build response using info from dictionary
            message = f'Emoji {emojiIndex}: {emojiInfo["emoji"]}\n'
            message += f'Name: {emojiInfo["Name"]}\n'
            message += f'Group: {emojiInfo["group"]}\n'
            message += f'Subgroup: {emojiInfo["subgroup"]}\n'
            message += f'Escape Sequence: {emojiInfo["escape"]}'

            update.message.reply_text(message)

        # message contains more than just the 1 emoji in it
        else:
            pass    

def startgame_command(update, context):
    '''Supplies various encodings of / options for starting position'''
    startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    response = f'Please see below the various encodings of the chess starting position. Use the link to the analysis board if you wish to make a move, copy the resulting FEN position to use with the /encode command. Use the /mix command if you wish to embed this position in to a text message.'
    response += "\n\n"
    response += f'FEN:\n{startingFen}'
    response += "\n\n"
    response += f'Emoji encoding:\n{covert_chess.encode(startingFen)}'
    response += "\n\n"
    response += f'Analysis board:\n{covert_chess.makeMove(startingFen)}'

    update.message.reply_text(response, disable_web_page_preview=True)

def encode_command(update, context):
    '''Sends emoji encoding of passed FEN position when /encode is issued.'''
    try:
        # checks an argument was passed
        if len(update.message.text.split(" ", 1)) > 1:

            # get passed FEN
            fen = update.message.text.split(" ", 1)[1].strip()

            response = f'Please see below the emoji encoding of the passed chess position. Use the /mix command if you wish to embed this position in to a text message.'
            
            response += "\n\n"
            
            response += f'Input FEN:\n{fen}'

            response += "\n\n"

            response += f'Emoji encoding:\n{covert_chess.encode(fen)}'

            response += "\n\n"

            response += f'Analysis board:\n{covert_chess.makeMove(fen)}'

            update.message.reply_text(response, disable_web_page_preview=True)

        # no argument passed
        else:
            update.message.reply_text('please input a valid FEN chess position after the /encode command')
    
    # try block failed, likely because of invalid FEN
    except:
        update.message.reply_text('please input a valid FEN chess position after the /encode command')

def decode_command(update, context):
    '''Sends emoji encoding of passed FEN position when /encode is issued.'''
    try:
        # checks an argument was passed
        if len(update.message.text.split(" ", 1)) > 1:

            # get passed string
            emojiEncoding = update.message.text.split(" ", 1)[1].strip()

            # unmix string in case user didn;t run /extract first
            emojiEncoding = covert_chess.unmix(update.message.text.split(" ", 1)[1])

            response = f'Please see below the FEN of the passed emoji encoding. Use the link to the analysis board if you wish to make a move, copy the resulting FEN position to use with the /encode command.'
            response += "\n\n"
            response += f'Input emoji encoding:\n{emojiEncoding}'
            response += "\n\n"

            # decode passed emoji string
            fen = covert_chess.decode(emojiEncoding)

            response += f'Decoded FEN position:\n{fen}'
            response += "\n\n"
            response += f'Analysis board:\n{covert_chess.makeMove(fen)}'

            update.message.reply_text(response, disable_web_page_preview=True)

        # no argument passed
        else:
            update.message.reply_text('Please input a valid emoji chess position after the /decode command.')
    
    # try block failed, likely because of invalid emoji encoded chess position
    except:
        update.message.reply_text('Please input a valid emoji chess position after the /decode command.')

def mix_command(update, context):
    '''Send emoji encoding mixed in to passed message when the command /mix is issued.'''

    helpMessage = "To use the /mix command properly, make sure to pass it a chess position, and then a message after the string \"message=\"\n\n"
    helpMessage += "e.g.\n/mix ♟️👯‍♂️🧚🏽‍♀️🧑🏻‍🔧👩🏾‍🦽🎥☄️👐🏿👩🏼‍🦼📟🚴🏼‍♂️🚣🏼‍♂️🛒💁🏿🤾🏾‍♀️🅰️👩🏿‍🏫🥔👩🏾‍🔧👼🏾📂🧑🏾‍🦲😀😀👐 message=The quick brown fox jumps over the lazy dog."
    
    try:
        # get passed arguments
        arguments = update.message.text.split(" ", 1)[1].strip()

        position = arguments.split("message=")[0].strip()
        premixedMessage = arguments.split("message=")[1].strip()

        message = f'Passed position:\n{position}\n\n'

        # position already encoded to emoji
        if len(emoji.emoji_lis(position)) > 0:
            message += f'Mixed message:\n{covert_chess.mix(position, premixedMessage)}'
            message += "\n\n"
            message += "Congratulations, you have now covertly hidden this chess position! Paste this message wherever you wish, ready to be decoded by your opponent later."
            update.message.reply_text(message, disable_web_page_preview=True)
        # FEN position
        else:
            message += f'Mixed message:\n{covert_chess.mix(covert_chess.encode(position), premixedMessage)}'
            message += "\n\n"
            message += "Congratulations, you have now covertly hidden this chess position! Paste this message wherever you wish, ready to be decoded by your opponent later."
            update.message.reply_text(message, disable_web_page_preview=True)

    except:
        update.message.reply_text(helpMessage)

def extract_command(update, context):
    '''Extracts and displays emoji from passed mixed message'''
    # checks an argument was passed
    if len(update.message.text.split(" ", 1)) > 1:

        # get passed string
        mixedMessage = update.message.text.split(" ", 1)[1].strip()

        # unmix string in case user didn;t run /extract first
        emojiOnly = covert_chess.unmix(update.message.text.split(" ", 1)[1])

        response = f'Input message:\n{mixedMessage}'
        response += "\n\n"

        if len(emojiOnly) == 0:
            response += f'No emoji found in passed massage.'
        else:
            response += f'Extracted emoji:\n{emojiOnly}'

        update.message.reply_text(response)

    # no argument passed
    else:
        update.message.reply_text('Please input a message with embedded emoji after the /extract command.')

def analysis_board(update, context):
    '''Send link to analysis board of given position when the command /move or /show is issued.'''
    try:
        # get any argument entered after command
        argument = update.message.text.split(" ", 1)[1].strip()

        message = f'Passed position:\n{argument}\n\n'

        if len(emoji.emoji_lis(argument)) > 0:
            message += f'Analysis board for passed position:\n{covert_chess.makeMove(covert_chess.decode(argument))}'
            message += "\n\n"
            message += "If you wish to make a move, do so on the linked analysis board, then copy the resulting FEN position to use with the /encode or /mix command."
            update.message.reply_text(message, disable_web_page_preview=True)
        else:
            # check FEN is valid
            if covert_chess.decode(covert_chess.encode(argument)) == argument:
                message += f'Analysis board for passed position:\n{covert_chess.makeMove(argument)}'
                message += "\n\n"
                message += "If you wish to make a move, do so on the linked analysis board, then copy the resulting FEN position to use with the /encode or /mix command."
                update.message.reply_text(message, disable_web_page_preview=True)
            else: 
                update.message.reply_text('Please input a valid emoji or FEN chess position after the command.')

    except:
        update.message.reply_text('Please input a valid emoji or FEN chess position after the command.')

def board_editor(update, context):
    '''Send link to board editor (optionally of a given position) when the command /edit or /create is issued.'''
    try:
        # returns link to edit starting position if no arguments entered
        if len(update.message.text.split(" ", 1)) == 1:
            startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

            message = f'Board editor (from starting position):\n{covert_chess.createPosition(startingFen)}'
            message += "\n\n"
            message += "After creating desired position in linked board, copy the resulting FEN position to use with the /encode or /mix command."
            update.message.reply_text(message, disable_web_page_preview=True)
        
        else:
            # get any argument entered after command
            argument = update.message.text.split(" ", 1)[1].strip()

            message = f'Passed position:\n{argument}\n\n'
            
            if len(emoji.emoji_lis(argument)) > 0:
                message += f'Board editor for passed position:\n{covert_chess.createPosition(covert_chess.decode(argument))}'
                message += "\n\n"
                message += "After creating desired position in linked board, copy the resulting FEN position to use with the /encode or /mix command."
                update.message.reply_text(message, disable_web_page_preview=True)
            else:
                # check FEN is valid
                if covert_chess.decode(covert_chess.encode(argument)) == argument:
                    message += f'Board editor for passed position:\n{covert_chess.createPosition(argument)}'
                    message += "\n\n"
                    message += "After creating desired position in linked board, copy the resulting FEN position to use with the /encode or /mix command."
                    update.message.reply_text(message, disable_web_page_preview=True)
                else: 
                    update.message.reply_text('Invalid position, please enter a valid emoji or FEN chess position or no arguments for starting position.')
    except:
        update.message.reply_text('Invalid position, please enter a valid emoji or FEN chess position or no arguments for starting position.')

def enpassant_command(update, context):
    '''Send a message when the command /enpassant is issued.'''
    update.message.reply_text('Holy hell')

def main():
    '''Start bot.'''
    # Create the Updater and pass it your bot's token.
    updater = Updater(credentials.bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("commands", commands_command))
    dispatcher.add_handler(CommandHandler("help", commands_command)) # alias
    dispatcher.add_handler(CommandHandler("startgame", startgame_command))
    dispatcher.add_handler(CommandHandler("newgame", startgame_command)) # alias
    dispatcher.add_handler(CommandHandler("encode", encode_command))
    dispatcher.add_handler(CommandHandler("encrypt", encode_command)) # alias
    dispatcher.add_handler(CommandHandler("decode", decode_command))
    dispatcher.add_handler(CommandHandler("decrypt", decode_command)) # alias
    dispatcher.add_handler(CommandHandler("mix", mix_command))
    dispatcher.add_handler(CommandHandler("extract", extract_command))
    dispatcher.add_handler(CommandHandler("unmix", extract_command)) # alias
    dispatcher.add_handler(CommandHandler("move", analysis_board))
    dispatcher.add_handler(CommandHandler("show", analysis_board)) # alias
    dispatcher.add_handler(CommandHandler("edit", board_editor))
    dispatcher.add_handler(CommandHandler("create", board_editor)) # alias
    dispatcher.add_handler(CommandHandler("enpassant", enpassant_command))

    # default handler for a command that has not been defined
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # echos a single emoji message back to userr
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, emoji_info))

    # using a webhook is usually preferred for final deployment
    # but can also be deployed using polling if a webhook can not be set up
    # or for testing in the dev environment before deployment
    # make sure to set which method to use in credentials.py
    if credentials.webhook_active:
        # Start the bot (webhook)
        updater.start_webhook(listen="0.0.0.0",
                            port=credentials.webhook_port,
                            url_path=credentials.bot_token,
                            webhook_url=credentials.webhook_url + credentials.bot_token)
    else:
        # Start the Bot (polling)
        updater.start_polling()
    

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)