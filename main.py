from environment import create_environment_dynamic
from environment import sort_state
from environment import get_state_by_name
from environment import get_action_by_name
from environment import get_stock_names
from agentRQ import Agent
import threading
import World
import time
from datetime import datetime



n_lines = 10
n_columns = 10
timeSleep = 0.5
#                                                        Good    Bad    Player
env = create_environment_dynamic(n_lines, n_columns, 20, "0.0", "0.6", "6.6", 0.9)
initialState = get_state_by_name("66", env)
stock_names = get_stock_names(env)
guy = Agent(env.states, stock_names, env.discount)


actions = World.actions
states = []


def haveWall(i, j):
    for w in World.walls:
        if (i, j) == w:
            return True
    return False


for i in range(World.y):
    for j in range(World.x):
        if not haveWall(i, j):
            states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0
        World.set_cell_score(state, action, temp[action])

for (i, j, c, w) in World.specials:
    for action in actions:
        World.set_cell_score((i, j), action, w)




def trial(agent, mdp):
    numberOfAction = 0
    global timeSleep
    state = initialState
    World.restart_game()
    time.sleep(timeSleep)
    World.update_triangles(agent.Q, states)
#    print(agent.Q)
    while True:
        next_action_name = agent.act(state)
        if next_action_name is None:
            break
        action = get_action_by_name(next_action_name, mdp)
        if action is not None:
            numberOfAction += 1
            state_name = sort_state(state, action)
            discoverActionDid(state.name, state_name)
            time.sleep(timeSleep)
            state = get_state_by_name(state_name, mdp)
    return numberOfAction

def discoverActionDid(oldStateName, newStateName):
#    print(oldStateName)
#    print(newStateName)
    if oldStateName == newStateName:
        return
    oldLine = int(oldStateName[0])
    oldColumn = int(oldStateName[1])
    newLine = int(newStateName[0])
    newColumn = int(newStateName[1])
    deltaLine = oldLine - newLine
    deltaColumn = oldColumn - newColumn
    if deltaLine == -1:
        do_action("Down")
    elif deltaLine == 1:
        do_action("Up")
    elif deltaColumn == -1:
        do_action("Right")
    elif deltaColumn == 1:
        do_action("Left")


def do_action(action):
    if action == "Up":
        World.try_move(-1, 0)
    elif action == "Down":
        World.try_move(1, 0)
    elif action == "Left":
        World.try_move(0, -1)
    elif action == "Right":
        World.try_move(0, 1)
    else:
        return

def run():
    a = datetime.now()
    Y = []
    X = []
    global guy
    global env
    global n_lines
    global n_columns
    for i in range(100):
        Y.append(i)
        print("Complete: ",i /99 * 100)
        X.append(trial(guy, env))
#    print(guy.Q)
#    print(guy.Nsa)
    #guy.show_politics(n_lines, n_columns)
    b = datetime.now()
    c = b - a
    print(c.seconds)
    print(c.microseconds)
    print(Y)
    print(X)
    World.showGraph(Y, X)

t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()