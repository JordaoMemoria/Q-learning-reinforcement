from numpy import zeros
from numpy import array
from numpy import empty
from pandas import DataFrame
from random import randint
import World


def get_action_name_of_state(state, utilities):
    if state is None:
        return "X"
    if state.terminal:
        return state.reward
    for index, row in utilities.iterrows():
        if row.name == state.name:
            return row.Action


class Agent:
    Q = None
    Nsa = None
    s = None
    a = None
    states = None
    stock_names = None
    discount_mdp = None

    def __init__(self, states, stock_names, discount_mdp):
        self.discount_mdp = discount_mdp
        self.states = states
        self.stock_names = stock_names
        lines = len(states)
        columns = len(stock_names)
        m1 = zeros(shape=(lines, columns))
        m2 = zeros(shape=(lines, columns))
        columns_names = []
        rows_names = []
        for s in states:
            rows_names.append(s.name)
        for a in stock_names:
            columns_names.append(a)
        self.Q = DataFrame(m1, columns=columns_names, index=rows_names)
        self.Nsa = DataFrame(m2, columns=columns_names, index=rows_names)

    def get_state_by_name(self, name):
        for state in self.states:
            if state.name == name:
                return state

    def get_max_action_value(self, sl):
        value = self.Q.at[sl.name, self.stock_names[0]]
        for a in self.stock_names:
            if self.Q.at[sl.name, a] > value:
                value = self.Q.at[sl.name, a]
        return value

    def function_exploration(self, s, a, n):
        if self.Nsa.at[s.name, a] < n:
            return 1
        else:
            return self.Q.at[s.name, a]

    def get_action(self, sl, n):
        default_action = randint(0, 3)
        action = self.stock_names[default_action]
        action_value = self.function_exploration(sl, action, n)
        for a in self.stock_names:
            value = self.function_exploration(sl, a, n)
            if action_value < value:
                action_value = value
                action = a
        return action

    def get_action_exploration(self, sl):
        default_action = randint(0, 3)
        nsl = self.Nsa.loc[sl.name]
        action_name = nsl.index[default_action]
        min_value = nsl[default_action]
        for i in range(len(nsl)):
            if nsl[i] < min_value:
                min_value = nsl[i]
                action_name = nsl.index[i]
        return action_name

    def get_utilities(self):
        u_states = []
        u_actions = []
        u = []
        for index, row in self.Q.iterrows():
            value, action_name = self.get_max_action_value_q(index)
            u_states.append(index)
            u_actions.append(action_name)
            u.append(value)
        columns_names = ["Value", "Action"]
        u = [u, u_actions]
        m = array(u).transpose(1, 0)
        u = DataFrame(m, index=u_states, columns=columns_names)
        return u

    def show_politics(self, lines, columns):
        utilities = self.get_utilities()
        stock_names = []
        matrix = empty(shape=(lines, columns), dtype=object)
        for i in range(lines):
            for j in range(columns):
                state_name = "{0}{1}".format(i, j)
                state = self.get_state_by_name(state_name)
                action_name = get_action_name_of_state(state, utilities)
                stock_names.append(action_name)
        for i in range(lines):
            for j in range(columns):
                matrix[i, j] = stock_names.pop(0)

        matrix = DataFrame(matrix)
        for i in range(lines):
            for j in range(columns):
                if matrix.loc[j, i] == "Up":
                    matrix.loc[j, i] = "^"
                elif matrix.loc[j, i] == "Down":
                    matrix.loc[j, i] = "v"
                elif matrix.loc[j, i] == "Left":
                    matrix.loc[j, i] = "<"
                elif matrix.loc[j, i] == "Right":
                    matrix.loc[j, i] = ">"
 #       print(matrix)

    def get_max_action_value_q(self, sl):
        value = self.Q.at[sl, self.stock_names[0]]
        action_name = self.stock_names[0]
        for a in self.stock_names:
            if self.Q.at[sl, a] > value:
                value = self.Q.at[sl, a]
                action_name = a
        return value, action_name

    def getLearningRate(self):
        a = self.Nsa.at[self.s.name, self.a]
        if a > 35:
            return 0.3
        else:
            return 1 -0.02*a

    def get_cell_by_name(self, state_name):
        return int(state_name[0]), int(state_name[1])

# Based on AIMA Chapter 21 Q-Learning Agent
    def act(self, sl):
        if sl is not None and sl.terminal:
            self.Q.at[sl.name,"Right"] = sl.reward
            self.Q.at[sl.name,"Down"] = sl.reward
            self.Q.at[sl.name,"Left"] = sl.reward
            self.Q.at[sl.name,"Up"] = sl.reward
        if self.s is not None:
            self.Nsa.at[self.s.name, self.a] += 1
            #self.learning_rate()
#                      Q[s,a]              ← Q[s,a]+  α(Nsa[s,a]) (r +         γ           maxa′ Q[s′,a′]                     −          Q[s,a] )
            self.Q.at[self.s.name, self.a] += self.getLearningRate()*(self.s.reward + self.discount_mdp * self.get_max_action_value(sl) - self.Q.at[self.s.name, self.a])
#            self.Q.at[self.s.name, self.a] += self.s.reward + self.discount_mdp * self.get_max_action_value(sl) - self.Q.at[self.s.name, self.a]

        if sl is not None and sl.terminal:
            self.s = None
            self.a = None
            return None
        self.s = sl
        self.a = self.get_action(sl, 5)
        return self.a

