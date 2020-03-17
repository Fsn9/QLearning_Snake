from enum import Enum

NUM_DIRECTIONS = 3

LEFT = 0
FORWARD = 1
RIGHT = 2


def toString(action):
	if action == 0:
		return 'LEFT'
	elif action == 1:
		return 'FORWARD'
	else:
		return 'RIGHT'

