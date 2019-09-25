
import sys

# to run the program: python cmtCount.py test.java

# implemented a finite state machine that jumps to different states as you parse every character the file input
# The default state is the Text State. Other states are slash state, single comment state, multiple comments state, star state and the end state (when EOF has been reached)

class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        
    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo, text):
        try:
            handler = self.handlers[self.startState]
        except:
            print("must call .set_start() before .run()")
        if not self.endStates:
            print("at least one state must be an end_state")

        total = 0
        single = 0
        block = 0
        numblock = 0
    
        while True:
            (newState, cargo, total, single, block, numblock) = handler(cargo, text, total, single, block, numblock)
            if newState.upper() in self.endStates:
                
                print "Total # of single line comments:  %d" % single
                print "Total # of comment lines within block comments:  %d" % block
                print "Total # of block line comments:  %d" % numblock
                print "Total # of comments lines:  %d" % (single + block)

                print "Total # of lines:  %d" % total

                print "Total # of TODOs: %d" % text.count("TODO")
                break 
            else:
                handler = self.handlers[newState.upper()] 





def textTransitions(ind, text, totalNoLines, singleCommentLines, blockComments, numBlockComments):

    if (ind < len(text)):
        ch = text[ind]
        if ch == "/":
            newState = "slash_state"
        else:
            newState = "text_state"
        if ch == "\n":
            totalNoLines+=1
    else:
        newState = "end_state"
    return (newState, ind + 1, totalNoLines, singleCommentLines, blockComments, numBlockComments)

def slashTransitions(ind, text, totalNoLines, singleCommentLines, blockComments, numBlockComments):
    ch = text[ind]
    if ch == "/":
        newState = "single_comment_state"
    elif ch == "*":
        newState = "multiple_comment_state"
    else:
        newState = "text_state"
    return (newState, ind + 1, totalNoLines, singleCommentLines, blockComments, numBlockComments)

def singleCommentTransitions(ind, text, totalNoLines, singleCommentLines, blockComments, numBlockComments):
    ch = text[ind]
    if ch == "\n":
        totalNoLines+=1
        singleCommentLines+=1
        newState = "text_state"
    else:
        newState = "single_comment_state"
    return (newState, ind + 1, totalNoLines, singleCommentLines, blockComments, numBlockComments)

def multipleCommentTransitions(ind, text, totalNoLines, singleCommentLines, blockComments, numBlockComments):
    ch = text[ind]
    if ch == "\n":
        totalNoLines+=1
        blockComments+=1
        newState = "multiple_comment_state"
    elif ch == "*":
        newState = "star_comment_state"
    else :
        newState = "multiple_comment_state"
    return (newState, ind + 1, totalNoLines, singleCommentLines, blockComments, numBlockComments)

def starTransitions(ind, text, totalNoLines, singleCommentLines, blockComments, numBlockComments):
    ch = text[ind]
    if ch == "/":
        newState = "text_state"
        blockComments+=1
        numBlockComments+=1
    elif ch == "*":
        newState = "star_comment_state"
    else: 
        newState = "multiple_comment_state"
    return (newState, ind + 1, totalNoLines, singleCommentLines, blockComments, numBlockComments)



inFile = sys.argv[1]


with open(inFile) as fileobj:
    text = fileobj.read()

    fsm = StateMachine()
    fsm.add_state("text_state", textTransitions)
    fsm.add_state("slash_state", slashTransitions)
    fsm.add_state("single_comment_state", singleCommentTransitions)
    fsm.add_state("multiple_comment_state", multipleCommentTransitions)
    fsm.add_state("star_comment_state", starTransitions)
    fsm.add_state("end_state", None, end_state=1)

    # choose the starting state
    if text[0] == "/":
        fsm.set_start("slash_state")
    else:
        fsm.set_start("text_state")
    
    #run the state machine with the text and the 2nd index so the 2nd charcter can be parsed
    fsm.run(1, text)
    



   


