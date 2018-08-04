class MDP:
    states = []
    actions = []
    discount = None

    def __init__(self, states, actions, discount):
        self.states = states
        self.actions = actions
        self.discount = discount
