class antBrain:
    def __init__(self):
        self.currentState = 'Idle'
    # Change anything below! (It might be easier to mess with the elevator
    #  brain, though
    states = ['Idle',
              'name1',
              'other name',
              'Whatever you want',
              'but',
              'shorter is',
              'better']
    #state outputs : Each state can return:
    # 'F' -- Go Forward
    # 'TR' -- Turn Right
    # 'TL' -- Turn Left
    # ''   -- do nothing (its an empty text string)
    outputs = {'Idle'             : ''  ,
               'name1'            : 'F' ,
               'other name'       : 'TR',
               'Whatever you want': 'F' ,
               'but'              : 'TL',
               'shorter is'       : 'F' ,
               'better'           : 'TL'}
    #NOTE:: the names of your states MUST MATACH EXACTLY with the
    # values in outputs the format is 'state name':'output'
    # Transition tables - Input is represented as FRL, meaning:
    #  F -- 1 for wall in front, 0 for no wall
    #  R -- 1 for wall to right, 0 for no wall
    #  L -- 1 for wall to left, 0 for no wall
    #  Format: Name your table whatever you want.
    #  I chose StateT (state name followed by a capital T for transition
    # These tables show what state the ant will transition to for the given input
    # Example: '010':'name1' Means:
    #   when the input is F=0, R=1, L=0, go to the state name1

    IdleT = {'000' : 'Whatever you want',
             '001' : 'but',
             '010' : 'Idle',
             '011' : 'shorter is',
             '100' : 'HitWall',
             '101' : 'HitWall',
             '110' : 'HitWall',
             '111' : 'HitWall'}
    shorter_isT = {'000' : 'PastWall',
                   '001' : 'PastWall',
                   '010' : 'shorter is',
                   '011' : 'shorter is',
                   '100' : 'PastWall',
                   '101' : 'PastWall',
                   '110' : 'HitWall',
                   '111' : 'HitWall'}
    # ...
    # include one transition for each state you have. Include all
    #  possibilities for inputs!
    # this table is the dispatch table and links the current state with
    #  the transition tables.
    
    dispatch = {'Idle'              : IdleT,
                'shorter is'        : shorter_isT,
                # ...
                'Whatever you want' : Whatever_you_wantT}
    # link all possible states with their transition tables you wrote

    ###### You shouldn't have to edit anything below this (Unless you name your default state something other than "Idle"
    def reset(self):
        self.currentState = 'Idle'

    ##### There is nothing to edit here
    def advance(self, Input):
        #print(Input + " -> " + self.dispatch[self.currentState][Input])
        self.currentState = self.dispatch[self.currentState][Input]
        return self.outputs[self.currentState]
