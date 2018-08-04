# Q-learning reinforcement learning agent based on temporal differentiation applied to the grid world of NxN

# Abstract

This work develops an agent based on learning Q and applies it to a grid world with obstacles. As a way of modelling the world, a data structure based on Markovian Decision Processes is used for every possible action in the world. In addition, the world is dynamically created so that it is possible to choose the number of "n" lines, "m" columns, number of obstacles and positions of important states. The tests run in three different worlds: one of 4 columns by 3 rows, one of 6 rows by 6 columns and last one of 10 rows by 10 rows. Time measurements are made under the agent passing through the respective world 100 times. Also shown is a graph representing the umpteenth time the agent has passed the world by the number of actions required to reach a terminal state. The decreasing graphs demonstrate the agent's learning.

# How to run

The code is implemented in python and the only file to be edited is "main.py". Before you run the code, you need to import these libraries: pandas, matplotlib and numpy. The others libraries used are native of language. We recommend PyCharm like IDE because the code was created in it.

# Editing "main.py"

There are some lines that have to be changed in order to create the world like the tester want.

line 14 > "n lines" configure the number of lines of the world

line 15 > "n columns" configure the number of columns of the world

line 16 > "timeSleep" configure the time between the actions of agent

line 18 > configure the position of good terminal state, bad terminal state and initial position of player. It's important to note that is necessary a point between the coordinates.

line 19 > this is the last configuration needed. You should just to repeat the initial position of player without the point like in last line.

Now you run and see how the agent behave.
