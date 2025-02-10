

class State():
    '''
    State class
    list of products
    '''
    
    def __init__(self, state, t=0):
        self.t = 0
        self.state = state

    def update_state(self, state):
        '''
        Takes state
        Updates state
        '''
        self.state = state
        self.t += 1