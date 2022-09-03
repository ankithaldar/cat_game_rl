from ex1_checks import (
    check_exercise_1,
    check_exercise_2,
    check_exercise_3,
)

###---------------------------------------------------------###

### 6.1 - Game of Tetris ###

# One is a state, one is an action and one is a reward
right = "Whether to move the piece right, left or keep it where it is"
points = "The number of points you've scored"
player = "The player of the game, who tries to score as high as possible"
board = "The dimensions of the Tetris board pieces on the board, not including their locations"
spaces = "Spaces filled at the bottom of the board, current piece shape, current piece location"


# TODO: of the variables defined above, pass the state as 'state', action as 'action' and reward as 'reward'
check_exercise_1(state=..., action=..., reward=...)

###---------------------------------------------------------###


### 6.2 - Robot navigation task ###

# One is a state, one is an action and one is a reward
hardware = "All the robotic hardware the robot has - motors, cpu, wheels & sensors"
reached = "Whether it has reached the goal location"
acceleration = "Acceleration/deceleration and tyre angle change"
location = "Robot location & orientation, layout of the room it's in & the goal location it's aiming to reach"
room = "The room the robot is in, in full detail!"


# TODO: fill in the state as state, action as action and reward as reward
check_exercise_2(state=..., action=..., reward=...)

###---------------------------------------------------------###

### 6.3 - Personalised advertiser online ###

# One is a state, one is an action and one is a reward
click = (
    "Whether the user clicks the advert & whether the user buys the advertised product"
)
advert = "Advert that can be shown"
info = "All physical information about the user - their age, height & hair colour"
user = "All user information incl. physical information, online behaviour & website they're on"
product = "The product or service that the advert is advertising"


# TODO: you know what to do now!
check_exercise_3(state=..., action=..., reward=...)

###---------------------------------------------------------###
