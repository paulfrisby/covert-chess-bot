# Library of functions to import emoji (and associated information) 
# from unicode supplied test files of various emoji standards, available at:
# https://unicode.org/Public/emoji/

# tested working from 4.0 to 14.0 emoji standards

# default file location / name of unicode emoji test file is set here
emojiTestFileLocation = "data/emoji-test.txt"

# creating global variable so a file doesn't need to be imported multiple times
# with multiple function calls
importedEmoji = None

# creating global variable which stores less fully qualified versios of emoji
# instead of fully-qualified version, when they exists
importedLessQualifiedEmoji = None

def setEmojiTestFileLocation(testFile = None):
    '''
    Overwrite the default test file location.
    '''
    # set new test file location
    emojiTestFileLocation = testFile

    # reset imported emoji
    importedEmoji = None

def getEmojiTestFileLocation():
    '''
    Get the current test file location.
    '''
    # return test file location
    return emojiTestFileLocation

def importEmoji(testFileOverride = None, lessQualified = False):
    '''
    Returns list of dicts (with each dict containing emoji information) for each 
    emoji in a given unicode testfile.
    '''

    # optionally setting new test file location
    if testFileOverride != None:
        setEmojiTestFileLocation(testFileOverride)

    # make sure we are working with global variables
    global importedEmoji
    global importedLessQualifiedEmoji

    # requested fully qualified emoji have already been set
    if (importedEmoji != None) and (lessQualified == False):
        return importedEmoji
    
    # requested less qualified emoji have already been set
    if (importedLessQualifiedEmoji != None) and (lessQualified == True):
        return importedLessQualifiedEmoji

    # Only need to import if global variable has not yet been set
    # i.e. an import has not already been done on fully qualified emoji
    if (importedEmoji == None) and (lessQualified == False):

        # open the test file
        emojiTestFile = open(emojiTestFileLocation, 'r', encoding='utf8')
        # store each line of file
        emojiTestFileLines = emojiTestFile.readlines()
        # close passed file
        emojiTestFile.close()

        # initialise to list to store imported emoji info in
        importedEmoji = []

        # iterate over each line to find relevant info
        for line in emojiTestFileLines:

            # check if the line defines the group of succedding emoji
            if (line[:9] == "# group: "):
                # GROUP
                group = line[9:].strip("\n")
                continue

            # check if the line defines the subgroup of succedding emoji
            if (line[:12] == "# subgroup: "):
                # SUBGROUP
                subgroup = line[12:].strip("\n")
                continue
            
            # ignore lines which do not contain relevant emoji info
            # i.e. lines starting with # or empty lines
            if (line[0] == "#") or (line[0] == "\n"):
                continue

            # unicode test files display emoji status in between 1st ; and 1st # within emoji line
            status = line.split(";", 1)[1].split("#", 1)[0].strip()

            # check if emoji in given line is fully qualified
            if status == "fully-qualified":

                # ESCAPE SEQUENCE
                # finds codepoints before the first ; of the line
                codePoints = line.split(";", 1)[0].split()
                # initialise escape sequence string
                escapeSequence = ""
                # iterate over each codepoint
                for codePoint in codePoints:
                    # pad each codepoint with preceeding 0s until it is 8 chars long
                    # and add needed escape string for python (\U)
                    escapedCodePoint = "\\U" + codePoint.zfill(8)
                    # append escaped codepoint to escape sequence
                    escapeSequence += escapedCodePoint

                # EMOJI
                # finds emoji in the first spot after the first # of line
                emoji = line.split("#", 1)[1].split()[0]

                # NAME
                # finds part of line after # (emoji + name)
                # then finds name by splitting it at first space
                # and removes any newline characters
                name = line.split("#", 1)[1].split(" ", 2)[2].strip("\n")

                # collate relevant info for emoji on this line in to dictionary
                emojiEntry = {
                    "emoji" : emoji,
                    "escape" : escapeSequence,
                    "name" : name,
                    "group" : group,
                    "subgroup" : subgroup
                }

                # append dictionary for this emoji on to the list
                importedEmoji.append(emojiEntry)

        return importedEmoji
    
    # Only need to import requested emoji if global variable has not yet been set
    # i.e. an import has not already been done on less qualified emoji
    if (importedLessQualifiedEmoji == None) and (lessQualified == True):

        # open the test file
        emojiTestFile = open(emojiTestFileLocation, 'r', encoding='utf8')
        # store each line of file
        emojiTestFileLines = emojiTestFile.readlines()
        # close passed file
        emojiTestFile.close()

        # initialise to list to store imported emoji info in
        importedLessQualifiedEmoji = []

        # iterate over each line to find relevant info
        for line in emojiTestFileLines:

            # check if the line defines the group of succedding emoji
            if (line[:9] == "# group: "):
                # GROUP
                group = line[9:].strip("\n")
                continue

            # check if the line defines the subgroup of succedding emoji
            if (line[:12] == "# subgroup: "):
                # SUBGROUP
                subgroup = line[12:].strip("\n")
                continue
            
            # ignore lines which do not contain relevant emoji info
            # i.e. lines starting with # or empty lines
            if (line[0] == "#") or (line[0] == "\n"):
                continue

            # unicode test files display emoji status in between 1st ; and 1st # within emoji line
            status = line.split(";", 1)[1].split("#", 1)[0].strip()

            # check if emoji in given line is fully qualified
            if status == "fully-qualified":

                # ESCAPE SEQUENCE
                # finds codepoints before the first ; of the line
                codePoints = line.split(";", 1)[0].split()
                # initialise escape sequence string
                escapeSequence = ""
                # iterate over each codepoint
                for codePoint in codePoints:
                    # pad each codepoint with preceeding 0s until it is 8 chars long
                    # and add needed escape string for python (\U)
                    escapedCodePoint = "\\U" + codePoint.zfill(8)
                    # append escaped codepoint to escape sequence
                    escapeSequence += escapedCodePoint

                # EMOJI
                # finds emoji in the first spot after the first # of line
                emoji = line.split("#", 1)[1].split()[0]

                # NAME
                # finds part of line after # (emoji + name)
                # then finds name by splitting it at first space
                # and removes any newline characters
                name = line.split("#", 1)[1].split(" ", 2)[2].strip("\n")

                # collate relevant info for emoji on this line in to dictionary
                emojiEntry = {
                    "emoji" : emoji,
                    "escape" : escapeSequence,
                    "name" : name,
                    "group" : group,
                    "subgroup" : subgroup
                }

                # append dictionary for this emoji on to the list
                importedLessQualifiedEmoji.append(emojiEntry)
            
            # checks if a less qualified version of emoji exists
            # i.e. last emoji entry needs to be overwritten 
            if (status == "minimally-qualified") or (status == "unqualified"):
                
                # ESCAPE SEQUENCE
                # finds codepoints before the first ; of the line
                codePoints = line.split(";", 1)[0].split()
                # initialise escape sequence string
                escapeSequence = ""
                # iterate over each codepoint
                for codePoint in codePoints:
                    # pad each codepoint with preceeding 0s until it is 8 chars long
                    # and add needed escape string for python (\U)
                    escapedCodePoint = "\\U" + codePoint.zfill(8)
                    # append escaped codepoint to escape sequence
                    escapeSequence += escapedCodePoint

                # EMOJI
                # finds less qualified emoji in the first spot after the first # of line
                emoji = line.split("#", 1)[1].split()[0]

                # overwrite last emoji dict
                # i.e. overwriting entry of fully qualified version imported on previous line
                importedLessQualifiedEmoji[-1] = {
                    "emoji" : emoji,
                    "escape" : escapeSequence,
                    "name" : name,
                    "group" : group,
                    "subgroup" : subgroup
                }
            
        return importedLessQualifiedEmoji

def getEmoji(testFileOverride = None, lessQualified = False):
    '''
    Returns list of all emoji from given unicode testfile.
    '''

    # optionally setting new test file location
    if testFileOverride != None:
        setEmojiTestFileLocation(testFileOverride)

    # fully qualified emoji
    if lessQualified == False:
        return [emojiEntry["emoji"] for emojiEntry in importEmoji(lessQualified == False)]

    # less qualified emoji
    if lessQualified == True:
        return [emojiEntry["emoji"] for emojiEntry in importEmoji(lessQualified=True)]

def getEmojiEscapes(testFileOverride = None, lessQualified = False):
    '''
    Returns list of escape sequences for all emoji from given unicode testfile.
    '''

    # optionally setting new test file location
    if testFileOverride != None:
        setEmojiTestFileLocation(testFileOverride)

    # fully qualified emoji
    if lessQualified == False:
        return [emojiEntry["escape"] for emojiEntry in importEmoji()]

    # less qualified emoji
    if lessQualified == True:
        return [emojiEntry["escape"] for emojiEntry in importEmoji(lessQualified=True)]

def getEmojiNames(testFileOverride = None):
    '''
    Returns list of names of all emoji from given unicode testfile.
    '''

    # optionally setting new test file location
    if testFileOverride != None:
        setEmojiTestFileLocation(testFileOverride)

    return [emojiEntry["name"] for emojiEntry in importEmoji()]

def getEmojiGroups(testFileOverride = None):
    '''
    Returns list of groups of all emoji from given unicode testfile.
    '''

    # optionally setting new test file location
    if testFileOverride != None:
        setEmojiTestFileLocation(testFileOverride)

    return [emojiEntry["group"] for emojiEntry in importEmoji()]

def getEmojiSubgroups(testFileOverride = None):
    '''
    Returns list of subgroups of all emoji from given unicode testfile.
    '''

    # optionally setting new test file location
    if testFileOverride != None:
        setEmojiTestFileLocation(testFileOverride)

    return [emojiEntry["subgroup"] for emojiEntry in importEmoji()]