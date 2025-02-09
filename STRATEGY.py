



class Strategy():
    '''
    Takes state

    Gives action
    '''
    
    def __init__(self, state):
        self.state = state

    def get_action(self, state):
        '''
        Takes state
        Gives action
        '''
        pass

    def update_strategy(self, state, action, next_state):
        '''
        Takes state, action, next state
        Updates strategy
        '''
        pass