from pygame.locals import *
import tools
import time
import pygame

class Facade:
        
    def __init__(self, game = None):
        print "init intelligent learning framework"
        
        #assert game != None
        self.game = game
        self.interactionstore = InteractionStore(game)
        self.firstPattern = InteractionPattern(self.interactionstore, None, self)

        #actions_1 = [(1, 2)]
        #interaction_1 = Interaction(actions, start, stop)
        #register to all pygame events
        #for e in pygame.events.get():
        #    self._action_executed_cb(e)
        
    def handleEvents(self, event, tool):
        """
        call this method to inform the framework about new events
        """
        #print event

        #forward events to the interaction store
        self.interactionstore.handleEvent(event, tool)

    def _action_executed_cb(action):
        """
        This callback should be used to inform the framework about new
        actions that occured
        """
        print "new action", action.name
        #categorize action
        #prototype: only detect obvious interactions, drop the rest
        #store the interactions somewhere, notify the interactionpatternmatcher

    def _add_interaction(self, interaction):
        """
        adds a new interaction to the interaction store.
        """
        print "add_interaction", interaction
        self.interactionstore.addInteraction(interaction)

    def _triggerSupport(self, interaction):
        self.game.triggerSupport(interaction)

    def _stopSupport(self):
        self.game.stopSupport()

class InteractionPattern:

    def __init__(self, interStore, interactions, facade):
        #register as observer
        interStore.register(self)
        #self.interactions = interactions
        self.interactions = ["objectCreated", "objectDestroyed"]
        self.loop_count = 0
        self.state = 0

        #need the facade to give feedback, STUB
        self.facade = facade

    def notify(self, interaction):
        #new interaction occurred, change state machine
        print "notify callback"
        if interaction.name in self.interactions:
            if interaction.name == "objectCreated" and self.state == 0:
                self.state = 1
                self.facade._stopSupport()
            elif interaction.name == "objectDestroyed" and self.state == 1:
                self.state = 0
                self.loop_count = self.loop_count + 1
                if self.loop_count == 3:
                    #notify pedagogical agent
                    self.loop_count = 0
                    self.facade._triggerSupport(interaction)

class InteractionStore:

    subscribers = [];
    interactionList = [];

    def __init__(self, game):
        print "init InteractionStore"
        self.game = game

    def addInteraction(self, interaction):
        print "added interaction with name " + interaction.name
        #add to persistent store with timestamp
        self.interactionList.append((time.localtime(None), interaction))
        for observer in self.subscribers:
            observer.notify(interaction)
    
    def handleEvent(self, event, tool):
        #print "handle event in interaction store"

        if (not isinstance(tool, tools.JointTool)
            and not isinstance(tool, tools.GrabTool)
            and not isinstance(tool, tools.DestroyTool)
            and event.type == MOUSEBUTTONUP):
            print "object " + tool.name + " created"
            createInteraction = Interaction("objectCreated")
            self.addInteraction(createInteraction)

        #call stateChange on all interactions in the store
        if (isinstance(tool, tools.DestroyTool) and event.type == MOUSEBUTTONDOWN):
            print "object deleted"
            destroyInteraction = Interaction("objectDestroyed");
            bodies = self.game.world.get_bodies_at_pos(pygame.mouse.get_pos())
            if bodies != False:
                print bodies
                print dir(bodies[-1])
            self.addInteraction(destroyInteraction)

        #always return false
        return False

    def register(self, observer):
        print "register observer"
        #test if the observer has a member "notify"
        if 'notify' in dir(observer):
            self.subscribers.append(observer)
        else:
            print "not a valid observer, notify method missing"

class StateMachine:
    """
    not in use at the moment, this was just a quick implementation, needs a lot
    more work to be fully functional!
    """
    def __init__(self, states, start, stop):
        self.states = states
        """
        states should be a list of tupels, each tupel is a state
        which contains as first element a symbol which leads
        to a transition and as the second element an integer which is the
        next state the machine should transist to.
        """
        self.actualState = start
        self.startState = start
        self.stopState = stop

    def stateChange(self, symbol):
        """
        returns true if a final state has been reached
        """
        if (states[self.actualState][0] == symbol):
            self.actualState = states[self.actualState][1]
        else:
            self.actualState = self.startState

        if (self.actualState == self.stopState):
            self.actualState = self.startState
            return TRUE;
        else:
            return FALSE;


class Interaction:

    def __init__(self, name):
       self.name = name

