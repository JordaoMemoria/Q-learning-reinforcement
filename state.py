class State:
    name = None
    reward = None
    terminal = None

    def __init__(self, name, reward, terminal):
        self.name = name
        self.reward = reward
        self.terminal = terminal
