import GUI as gui
import RLearning as rl
import graphics

NUM_OBSTACLES = 0
WALLS_THICKNESS = 1

# grid WxH
GRID_WIDTH = 12
GRID_HEIGHT = 12

# BIG SIDE (WIDTH OR HEIGHT) in pixels
BIG_SIDE = 400

# compute parameters to set in the objects rl and gui below
PIXEL_SIZE, WIDTH, HEIGHT = graphics.computePixelSize(GRID_WIDTH+2*WALLS_THICKNESS, GRID_HEIGHT+2*WALLS_THICKNESS, BIG_SIDE)

# objects rl (AI algorithm) and gui (graphical window object)
rl = rl.RLearning(GRID_WIDTH, GRID_HEIGHT, NUM_OBSTACLES)
gui = gui.GUI(rl, WIDTH, HEIGHT, GRID_WIDTH + 2*WALLS_THICKNESS, GRID_HEIGHT + 2*WALLS_THICKNESS, PIXEL_SIZE)

# start loop of GUI events
gui.mainloop()
