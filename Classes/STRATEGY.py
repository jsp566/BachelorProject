



class Strategy():
    '''
    Takes state

    Gives action
    '''
    
    def __init__(self, params):
        self.params = params

    def initialize(self, state_space, action_space):
        '''
        Initializes strategy
        '''
        pass
        

    def get_action(self, state, t):
        '''
        Takes state
        Gives action
        '''
        pass

    def update_strategy(self, state, action, next_state, profit):
        '''
        Takes state, action, next state
        Updates strategy
        '''
        pass