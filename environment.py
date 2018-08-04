from state import State
from mdp import MDP
from action import Action
from pandas import DataFrame
from random import uniform
from random import randint
from numpy import empty
from numpy import zeros
from math import trunc
import World


def create_environment(discount):
    states = create_states(-0.04)
    actions = create_actions(states)
    return MDP(states, actions, discount)


def create_environment_dynamic(n_lines, m_columns, n_walls, sr_plus, sr_less, s_initial, discount):
    World.x = m_columns
    World.y = n_lines

    amb = empty([n_lines, m_columns], dtype=object)
    s = sr_plus.split(sep=".")
    amb[int(s[0]), int(s[1])] = "+1"

    World.specials.append((int(s[0]), int(s[1]),"green",1))

    s = sr_less.split(sep=".")
    amb[int(s[0]), int(s[1])] = "-1"

    World.specials.append((int(s[0]), int(s[1]),"red",-1))

    s = s_initial.split(sep=".")
    amb[int(s[0]), int(s[1])] = "I"

    World.player = (int(s[0]), int(s[1]))
    World.initial_position = (int(s[0]), int(s[1]))

    while n_walls > 0:
        line = randint(0, n_lines-1)
        col = randint(0, m_columns-1)
        if amb[line, col] is None:
            amb[line, col] = "X"

            World.walls.append((line, col))

            n_walls -= 1
    for i in range(n_lines):
        for j in range(m_columns):
            if amb[i, j] is None or amb[i, j] == 'I':
                amb[i, j] = " "

    states = create_states_dynamic(amb, -0.04)
    print(amb)
    up = create_up(states)
    down = create_down(states)
    right = create_right(states)
    left = create_left(states)
    actions = [up, down, left, right]

    World.render_grid()
    World.create_player()
    # World.start_game()

    return MDP(states, actions, discount)


def get_names_states(states):
    names = []
    for i in range(len(states)):
        names.append(states[i].name)
    return names


def generate_m_prob(states):
    names = get_names_states(states)
    m_prob = zeros(shape=(len(states),len(states)))
    m_prob = DataFrame(m_prob, index=names, columns=names)
    return m_prob


def there_is(name, states):
    for s in states:
        if s.name == name:
            return True
    return False


def update_prob(m_prob, i, j, p, s_name, states):
    sl_name = "{0}{1}".format(i, j)
    if there_is(sl_name, states):
        m_prob.at[s_name, sl_name] += p
    else:
        m_prob.at[s_name, s_name] += p
    return m_prob


def create_up(states):
    m_prob = generate_m_prob(states)
    for s in states:
        if s.terminal:
            m_prob.at[s.name, s.name] = 1
        else:
            n = int(s.name)
            i = trunc(n/10)
            j = round((n/10 - i) * 10)
            update_prob(m_prob, i-1, j, 0.8, s.name, states)
            update_prob(m_prob, i, j+1, 0.1, s.name, states)
            update_prob(m_prob, i, j-1, 0.1, s.name, states)
    return Action("Up", m_prob)


def create_down(states):
    m_prob = generate_m_prob(states)
    for s in states:
        if s.terminal:
            m_prob.at[s.name, s.name] = 1
        else:
            n = int(s.name)
            i = trunc(n/10)
            j = round((n/10 - i) * 10)
            update_prob(m_prob, i+1, j, 0.8, s.name, states)
            update_prob(m_prob, i, j+1, 0.1, s.name, states)
            update_prob(m_prob, i, j-1, 0.1, s.name, states)
    return Action("Down", m_prob)


def create_left(states):
    m_prob = generate_m_prob(states)
    for s in states:
        if s.terminal:
            m_prob.at[s.name, s.name] = 1
        else:
            n = int(s.name)
            i = trunc(n/10)
            j = round((n/10 - i) * 10)
            update_prob(m_prob, i, j-1, 0.8, s.name, states)
            update_prob(m_prob, i+1, j, 0.1, s.name, states)
            update_prob(m_prob, i-1, j, 0.1, s.name, states)
    return Action("Left", m_prob)


def create_right(states):
    m_prob = generate_m_prob(states)
    for s in states:
        if s.terminal:
            m_prob.at[s.name, s.name] = 1
        else:
            n = int(s.name)
            i = trunc(n/10)
            j = round((n/10 - i) * 10)
            update_prob(m_prob, i, j+1, 0.8, s.name, states)
            update_prob(m_prob, i+1, j, 0.1, s.name, states)
            update_prob(m_prob, i-1, j, 0.1, s.name, states)
    return Action("Right", m_prob)


def create_states_dynamic(amb, r):
    states = []
    for i in range(amb.shape[0]):
        for j in range(amb.shape[1]):
            if amb[i, j] != "X":
                if amb[i, j] == " ":
                    s = State("{0}{1}".format(i, j), r, False)
                else:
                    s = State("{0}{1}".format(i, j), int(amb[i, j]), True)
                states.append(s)
    return states


def create_states(r):
    e11 = State("11", r, False)
    e12 = State("12", r, False)
    e13 = State("13", r, False)
    e21 = State("21", r, False)
    e23 = State("23", r, False)
    e31 = State("31", r, False)
    e32 = State("32", r, False)
    e33 = State("33", r, False)
    e41 = State("41", r, False)
    e42 = State("42", -1, True)
    e43 = State("43", 1, True)
    return [e11, e12, e13, e21, e23, e31, e32, e33, e41, e42, e43]


def create_actions(states):
    matrix_up = [
        [0.1, 0.8, 0, 0.1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.2, 0.8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.9, 0, 0.1, 0, 0, 0, 0, 0, 0],
        [0.1, 0, 0, 0.8, 0, 0.1, 0, 0, 0, 0, 0],
        [0, 0, 0.1, 0, 0.8, 0, 0, 0.1, 0, 0, 0],
        [0, 0, 0, 0.1, 0, 0, 0.8, 0, 0.1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0.1, 0.8, 0, 0.1, 0],
        [0, 0, 0, 0, 0.1, 0, 0, 0.8, 0, 0, 0.1],
        [0, 0, 0, 0, 0, 0.1, 0, 0, 0.1, 0.8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]
    matrix_right = [
        [0.1, 0.1, 0, 0.8, 0, 0, 0, 0, 0, 0, 0],
        [0.1, 0.8, 0.1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.1, 0.1, 0, 0.8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.2, 0, 0.8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0.2, 0, 0, 0.8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.1, 0.1, 0, 0.8, 0, 0],
        [0, 0, 0, 0, 0, 0.1, 0, 0.1, 0, 0.8, 0],
        [0, 0, 0, 0, 0, 0, 0.1, 0.1, 0, 0, 0.8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0.9, 0.1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]
    matrix_left = [
        [0.9, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.1, 0.8, 0.1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.1, 0.9, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.8, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.8, 0, 0.2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0.8, 0, 0.1, 0.1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.1, 0.8, 0.1, 0, 0, 0],
        [0, 0, 0, 0, 0.8, 0, 0.1, 0.1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.8, 0, 0, 0.1, 0.1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]
    matrix_down = [
        [0.9, 0, 0, 0.1, 0, 0, 0, 0, 0, 0, 0],
        [0.8, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0.8, 0.1, 0, 0.1, 0, 0, 0, 0, 0, 0],
        [0.1, 0, 0, 0.8, 0, 0.1, 0, 0, 0, 0, 0],
        [0, 0, 0.1, 0, 0.8, 0, 0, 0.1, 0, 0, 0],
        [0, 0, 0, 0.1, 0, 0.8, 0, 0, 0.1, 0, 0],
        [0, 0, 0, 0, 0, 0.8, 0.1, 0, 0, 0.1, 0],
        [0, 0, 0, 0, 0.1, 0, 0.8, 0, 0, 0, 0.1],
        [0, 0, 0, 0, 0, 0.1, 0, 0, 0.9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]

    names = []
    for s in states:
        names.append(s.name)

    matrix_up = DataFrame(matrix_up, columns=names, index=names)
    matrix_right = DataFrame(matrix_right, columns=names, index=names)
    matrix_left = DataFrame(matrix_left, columns=names, index=names)
    matrix_down = DataFrame(matrix_down, columns=names, index=names)

    up = Action("Up", matrix_up)
    right = Action("Right", matrix_right)
    left = Action("Left", matrix_left)
    down = Action("Down", matrix_down)
    return [up, down, left, right]


def sort_state(state, action):
    accumulator = 0
    sorted_value = uniform(0, 1)
    m_line = action.matrix_prob.loc[state.name]
    for i in range(len(m_line)):
        if sorted_value <= m_line[i]+accumulator:
            return m_line.index[i]
        else:
            accumulator += m_line[i]


def get_stock_names(mdp):
    stock_names = []
    for action in mdp.actions:
        stock_names.append(action.name)
    return stock_names


def get_action_by_name(name, mdp):
    for action in mdp.actions:
        if action.name == name:
            return action


def get_state_by_name(name, mdp):
    for state in mdp.states:
        if state.name == name:
            return state


#create_environment_dynamic(3, 4, 1, "3.4", "2.4", "1.1", 0.999)
