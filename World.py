from tkinter import *
import numpy as np
import matplotlib as mpl
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

master = Tk()

triangle_size = 0.1
cell_score_min = -1
cell_score_max = 1
Width = 80
(x, y) = (10, 10)
actions = ["Up", "Down", "Left", "Right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (int(x/2), y-1)
initial_position = None
score = 1
restart = False
walk_reward = -0.04

walls = []
specials = []
cell_scores = {}


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo

def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(y):
        for j in range(x):
            board.create_rectangle(j*Width, i*Width, (j+1)*Width, (i+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(j, i, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(j*Width, i*Width, (j+1)*Width, (i+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(j*Width, i*Width, (j+1)*Width, (i+1)*Width, fill="black", width=1)


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dy, dx):
    global player, x, y, score, walk_reward, me, restart
    if restart == True:
        restart_game()
    new_x = player[1] + dx
    new_y = player[0] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_y, new_x) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_y, new_x)
    for (i, j, c, w) in specials:
        if new_y == i and new_x == j:
            score -= walk_reward
            score += w
            if score > 0:
                pass
               # print("Success! score: ", score)
            else:
                pass
                #print("Fail! score: ", score)
            restart = True
            return
#    print("New player position: ",player)
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = initial_position
    score = 1
    restart = False
    board.coords(me, player[1]*Width+Width*2/10, player[0]*Width+Width*2/10, player[1]*Width+Width*8/10, player[0]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

def update_triangles(Q, states):
    i = 0
    for index, row in Q.iterrows():
        state = states[i]
#        print(state)
#        print(index)
        set_cell_score(state, "Up", row["Up"])
        set_cell_score(state, "Down", row["Down"])
        set_cell_score(state, "Left", row["Left"])
        set_cell_score(state, "Right", row["Right"])
        i += 1

def create_player():
    global me
    me = board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                                player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10, fill="orange",
                                width=1, tag="me")

board.grid(row=0, column=0)

def showGraph(X, Y):

    # Create the figure we desire to add to an existing canvas
    fig = mpl.figure.Figure(figsize=(4, 4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlabel("Teste")
    ax.plot(X, Y)

    # Keep this handle alive, or else figure will disappear
    fig_x, fig_y = 150, 150
    fig_photo = draw_figure(board, fig, loc=(fig_x, fig_y))
    fig_w, fig_h = fig_photo.width(), fig_photo.height()

    # Add more elements to the canvas, potentially on top of the figure
    board.create_text(350, 575, font="Times 20 italic bold", text="Trials", anchor="s")
    board.create_text(130, 450, font="Times 20 italic bold", text="\n".join("Actions"), anchor="s")



def start_game():
    master.mainloop()
