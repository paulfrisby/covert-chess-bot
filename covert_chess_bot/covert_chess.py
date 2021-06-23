# ------------------------------------------------------------------------------
# Covert Chess
# ------------------------------------------------------------------------------
# Author: Paul Frisby
# Email: mail@paulfrisby.com
# Github: https://github.com/paulfrisby/
# ------------------------------------------------------------------------------
# Program to convert between a FEN chess position and a custom emoji encoding.
# https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
# Mixes emoji encoding in to given text block to steganographically hide the
# chess position.
#
# n.b. Given that the custom emoji encoding is based on FEN, a complete list of
# moves is not stored. Therefore, threefold repitition can not be automatically
# calculated. This allows for a more compact encoding, storing every move would
# very quickly make the length of the encoding unreasonably long to include 
# within a short message.
# ------------------------------------------------------------------------------

import emoji
from covert_chess_bot import emoji_importer

# import dictionary with info of all 3,178 fully qualified emoji from unicode's 12.1 standard
emojiDict = emoji_importer.importEmoji()

# import all 3,178 fully qualified emoji from unicode's 12.1 standard 
emojiList = emoji_importer.getEmoji()

# importing all 3,178 emojis from unicode's standard
# preferring less qualified emojis when they exist
# needed for situations where an emoji library function returns less qualified
# emoji with a fully qualified emoji as input 
emojiListLessQualified = emoji_importer.getEmoji(lessQualified=True)

def emojiIndex(emoji):
    '''
    Returns index of given emoji
    '''

    # try on both lists so that fully and minimally qualified emoji both return a correct index value
    try:
        index = emojiList.index(emoji)
    except:
        index = emojiListLessQualified.index(emoji)
    
    return index

def emojiInfo(index):
    '''
    Returns the dictionary of info for emoji at a given index
    '''
    return emojiDict[index]

def encode(fenPosition):
    '''
    Takes a chess position in FEN and returns emoji encoding of position.
    '''

    def getSquareValues(fenPosition):
        pieceValues = {
            "P": 1,
            "N": 2,
            "B": 3,
            "R": 4,
            "Q": 5,
            "K": 6,
            "p": 7,
            "n": 8,
            "b": 9,
            "r": 10,
            "q": 11,
            "k": 12
        }
        
        # initialise list to store value of each square
        squaresValues = []

        # iterate over part of fen detailing pieces
        for char in fenPosition.split()[0]:
            
            # ignore line separators 
            if char == "/":
                pass
           
            # add values for empty squares
            elif char in "12345678":
                for i in range(int(char)):
                    squaresValues.append(0)

            # add value of square from dictionary 
            else:
                squaresValues.append(pieceValues[char])
        
        return squaresValues
    
    def getNextToMove(fenPosition):
        # white to move
        if fenPosition.split()[1] == "w":
            return 0
        # black to move
        else:
            return 1
    
    def getCastleRights(fenPosition):
        # initialise variable to store values
        castleRights = [0] * 4

        # extract castling rights section of fen
        fenCastleRights = fenPosition.split()[2]

        # white kingside castle
        if "K" in fenCastleRights:
            castleRights[0] = 1
        # white queenside castle
        if "Q" in fenCastleRights:
            castleRights[1] = 1
        # black kingside castle
        if "k" in fenCastleRights:
            castleRights[2] = 1
        # black queenside castle
        if "q" in fenCastleRights:
            castleRights[3] = 1
        
        return castleRights

    def getEnPassantValue(fenPosition):
        enPassantSquare = fenPosition.split()[3]

        # no en passant capture possible
        if enPassantSquare == "-":
            return 0

        # how far away from 'a' file
        fileValue = ord(enPassantSquare[0]) - ord("a") + 1

        # how far away from 8th rank
        rankValue = 8 - int(enPassantSquare[1])

        return (8 * rankValue) + fileValue
    
    def getHalfMoves(fenPosition):
        return int(fenPosition.split()[4])
        
    def getFullMoves(fenPosition):
        return int(fenPosition.split()[5])

    def firstSquareEmoji(squareValue):
        return emojiList[2441 + squareValue]

    def threeSquaresEmoji(squareValues, offset):
        
        # initialise index to offset
        index = offset

        # 1st square
        index += squareValues[0] * (13*13)

        # 2nd square
        index += squareValues[1] * (13)

        # 3rd square
        index += squareValues[2]

        # make sure index is still in range
        index = index % 3178

        return emojiList[index]

    def legalMovesEmoji(nextToMove, castleRights, enPassant):
        
        # initialise index
        index = 0

        # next to move
        index += nextToMove * 1040

        # white kingside castle
        if castleRights[0] == 1:
            index += 520
        # white queenside castle
        if castleRights[1] == 1:
            index += 260
        # black kingside castle
        if castleRights[2] == 1:
            index += 130
        # black queenside castle
        if castleRights[3] == 1:
            index += 65

        # en passant square
        index += enPassant
        
        return emojiList[index] 
    
    def moveCountEmojis(halfMoves, fullMoves):
        movesValue = halfMoves + (fullMoves * 101)
        emoji1 = emojiList[int(movesValue / 3178)]
        emoji2 = emojiList[movesValue % 3178]

        return emoji1 + emoji2
    
    # initialise variable to store emoji encoding of position
    emojiPosition = ""

    squareValues = getSquareValues(fenPosition)

    emojiPosition += firstSquareEmoji(squareValues[0])

    for i in range(21):
        firstSquareIndex = 3*i + 1
        threeSquares = squareValues[firstSquareIndex : firstSquareIndex + 3]
        emojiPosition += threeSquaresEmoji(threeSquares, i * 1111)

    nextToMove = getNextToMove(fenPosition)
    castleRights = getCastleRights(fenPosition)
    enPassant = getEnPassantValue(fenPosition)

    emojiPosition += legalMovesEmoji(nextToMove, castleRights , enPassant)

    halfMoves = getHalfMoves(fenPosition)
    fullMoves = getFullMoves(fenPosition)
    
    emojiPosition += moveCountEmojis(halfMoves, fullMoves)

    return emojiPosition

def decode(emojiPosition):
    '''
    Takes a chess position in emoji and returns FEN encoding of position.
    '''

    def get1stSquareValue(emoji):

        # get index of emoji in this entry
        index = emojiIndex(emoji)
            
        return index - 2441

    def get3SquareValues(emoji, offset):
        
        # initialise list to store value of each square
        threeSquaresValues = []

        # get index of emoji in this entry
        index = emojiIndex(emoji)

        # remove offset
        withoutOffset = index - offset

        # make sure value is still in 0-3177 range
        inRangeValue = withoutOffset % 3178

        # work out and set piece 1 value
        piece1Value = int( inRangeValue / (13*13) )
        threeSquaresValues.append(piece1Value)

        # work out and set piece 2 value
        piece2Value = int( (inRangeValue % (13*13)) / 13 )
        threeSquaresValues.append(piece2Value)

        # work out and set piece 3 value
        piece3Value = inRangeValue % 13
        threeSquaresValues.append(piece3Value)
        
        return threeSquaresValues
        
    def getLegalMoveValues(emoji):
        
        # get index of emoji in this entry
        index = emojiIndex(emoji)
        
        # work out and set next to move value
        nextToMoveValue = int(index / 1040)

        # initialise list to hold castling rights values
        castleRightsValues = []

        # work out and set all 4 castling rights values
        for i in range(4):
            castleRightsValues.append( int((index % int(1040 / 2**i)) / (520 / 2**i)) )

        # work out and set en passant value
        enPassantValue = index % 65
        
        return nextToMoveValue, castleRightsValues, enPassantValue

    def getMoveCounts(emojiPair):
        
        # get index of emoji 1
        index1 = emojiIndex(emojiPair[0])

        # get index of emoji 2
        index2 = emojiIndex(emojiPair[1])

        # combine indexes of 2 emoji back in to originally computed total value
        totalValue = (index1 * 3178) + index2

        # work out and set half moves
        halfMoves = totalValue % 101

        # work out and set full moves
        fullMoves = int(totalValue / 101)

        return halfMoves, fullMoves

    def squaresFen(squareValues):
        
        pieceByValues = {
            0: "1",
            1: "P",
            2: "N",
            3: "B",
            4: "R",
            5: "Q",
            6: "K",
            7: "p",
            8: "n",
            9: "b",
            10: "r",
            11: "q",
            12: "k"
        }

        # list to hold strings for each rank
        rankSquareValues = []

        # build string for each rank
        for i in range(8):
            # initialising string to build one rank's square statuses in
            rankString = ""

            # build string with "1" representing an empty square
            for value in squareValues[ i*8 : (i+1)*8 ]:
                rankString += pieceByValues[value]

            # replace series of empty squares with single number
            # e.g. "111" -> "3"
            for emptyLine in ["11111111", "1111111", "111111", "11111", "1111", "111", "11", "1", ]:
                rankString = rankString.replace(emptyLine, str(len(emptyLine)))
            
            # add completed rank string to list
            rankSquareValues.append(rankString)
        
        # connect strings for each rank with forward slashes
        return "/".join(rankSquareValues)

    def nextToMoveFen(nextToMoveValue):
        # white to move
        if nextToMoveValue == 0:
            return "w"
        # black to move
        else:
            return "b"

    def castleRightsFen(castleRightsValues):
        
        # checks if no castles are legal
        if castleRightsValues == [0, 0, 0, 0]:
            return "-"

        # initialise string to build this section of fen in 
        castleRightsString = ""
        
        # white kingside castle
        if castleRightsValues[0] == 1:
            castleRightsString += "K"
        # white queenside castle
        if castleRightsValues[1] == 1:
            castleRightsString += "Q"
        # black kingside castle
        if castleRightsValues[2] == 1:
            castleRightsString += "k"
        # black queenside castle
        if castleRightsValues[3] == 1:
            castleRightsString += "q"
        
        return castleRightsString

    def enPassantFen(enPassantValue):

        # no en passant capture possible
        if enPassantValue == 0:
            return "-"
        
        # chars for each file
        files = "abcdefgh"

        # file
        fileValue = (enPassantValue - 1) % 8
        enPassantString = files[fileValue]

        # rank
        rankValue = 8 - int( (enPassantValue - 1) / 8)
        enPassantString += str(rankValue)

        return enPassantString
    
    def halfMovesFen(halfMoves):
        return str(halfMoves)
    
    def fullMovesFen(fullMoves):
        return str(fullMoves)
    
    # initialise variable to store fen encoding of position
    fenPosition = ""

    # initialise variable to store value of each square on board
    squareValues = []
    
    # get 1st emoji and add its value to square values list
    emoji1stSquare = emoji.emoji_lis(emojiPosition)[0]["emoji"]
    squareValues.append(get1stSquareValue(emoji1stSquare))

    # get next 21 square emojis, adding their values to square values list
    for i in range(21):
        emoji3Squares = emoji.emoji_lis(emojiPosition)[i+1]["emoji"]
        offset = i * 1111
        squareValues += get3SquareValues(emoji3Squares, offset)

    # set squares in fen
    fenPosition += squaresFen(squareValues)
    # add space required by fen format
    fenPosition += " "
    
    # get 23rd emoji and extract relevant values
    emojiLegalMoves = emoji.emoji_lis(emojiPosition)[22]["emoji"]
    nextToMoveValue, castleRightsValues, enPassantValue = getLegalMoveValues(emojiLegalMoves)

    # set next to move in fen
    fenPosition += nextToMoveFen(nextToMoveValue)
    # add space required by fen format
    fenPosition += " "

    # set castle rights in fen
    fenPosition += castleRightsFen(castleRightsValues)
    # add space required by fen format
    fenPosition += " "

    # set en passant possibility in fen
    fenPosition += enPassantFen(enPassantValue)
    # add space required by fen format
    fenPosition += " "

    # get last 2 emoji and extract move values
    emojiMoves = []
    emojiMoves.append(emoji.emoji_lis(emojiPosition)[23]["emoji"])
    emojiMoves.append(emoji.emoji_lis(emojiPosition)[24]["emoji"])
    halfMoves, fullMoves = getMoveCounts(emojiMoves)
    
    # set half moves clock in fen
    fenPosition += halfMovesFen(halfMoves)
    # add space required by fen format
    fenPosition += " "

    # set full moves in fen
    fenPosition += fullMovesFen(fullMoves)

    return fenPosition

def mix(emojiPosition, message):
    '''
    Mixes a given emoji chess poition in to a given message.
    '''

    def evenlyInterleaveLists(list1, list2):
        '''
        Takes 2 lists of varying sizes, and merges them in to 1 list such that the
        the elements of each list are evenly spaced among the entire resulting list.
        '''

        # initialise list to store list1 values + interval positions of each value
        list1Intervals = []
        # iterate over every list item
        for i in range(len(list1)):
            # calculates a value representing where this list item would
            # be if all list items are spread evenly between 0 and 1
            interval = (i + 1) / (len(list1) + 1)
            list1Intervals.append({"interval": interval, "value": list1[i]})

        # initialise list to store list2 values + interval positions of each value
        list2Intervals = []
        # iterate over every list item
        for i in range(len(list2)):
            # calculates a value representing where this list item would
            # be if all list items are spread evenly between 0 and 1
            interval = (i + 1) / (len(list2) + 1)
            list2Intervals.append({"interval": interval, "value": list2[i]})

        # initiating list to interleave other lists in to
        interleavedList = []

        # repeatedly find element with lowest interval value, and append it to list
        while (len(list1Intervals) + len(list2Intervals) > 0):
            
            # checks if list1 is exhausted
            if len(list1Intervals) == 0:
                # append value of 0th element in list2
                interleavedList.append(list2Intervals[0]["value"])
                # remove 0th element from list2
                del list2Intervals[0]

            # checks if list2 is exhausted
            elif len(list2Intervals) == 0:
                # append value of 0th element in list1
                interleavedList.append(list1Intervals[0]["value"])
                # remove 0th element from list1
                del list1Intervals[0]

            # checks if intial list1 item has a lower value than initial list2 item
            elif list1Intervals[0]["interval"] < list2Intervals[0]["interval"]:
                # append value of 0th element in list1
                interleavedList.append(list1Intervals[0]["value"])
                # remove 0th element from list1
                del list1Intervals[0]

            # intial list1 item has a higher value than initial list2 item
            else:
                # append value of 0th element in list2
                interleavedList.append(list2Intervals[0]["value"])
                # remove 0th element from list2
                del list2Intervals[0]

        # all items should now have been added to interleaved list
        return interleavedList

    # get list of all emoji in position
    splitEmoji = [x["emoji"] for x in emoji.emoji_lis(emojiPosition)]

    # get a list of all words in message
    splitMessage = message.split()

    # interleave these 2 lists
    mixedMessage = evenlyInterleaveLists(splitMessage, splitEmoji)

    return " ".join(mixedMessage)

def unmix(mixedMessage):
    '''
    Extracts emoji from a given mixed message including it.
    '''

    emojiString = ""

    extractedEmoji = emoji.emoji_lis(mixedMessage)

    # iterate through first 25 extracted emoji
    for entry in extractedEmoji:

        # get index of emoji in this entry
        index = emojiIndex(entry["emoji"])

        # append fully qualified emoji to string
        emojiString += emojiList[index]

    # return completed string
    return emojiString

def makeMove(fenPosition):
    '''
    Takes a given FEN position and returns link to an analysis board with the 
    given position. Such that a legal move can be made to find FEN position 
    after move without manual claulation.
    '''
    analysisBoardLink = "https://lichess.org/analysis/"

    return analysisBoardLink + fenPosition.replace(" ", "_")

def createPosition(fenPosition = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    '''
    Returns link to a board editor so a custom FEN position can be constructed. 
    Defaults to standard board layout after 0 moves.
    '''
    boardEditorLink = "https://lichess.org/editor/"

    return boardEditorLink + fenPosition.replace(" ", "_")