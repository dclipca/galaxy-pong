# Import the random library
import random

# Import the cs1lib library
from cs1lib import *

# Import images
space = load_image("./images/space.png")
stars = load_image("./images/stars.png")
ring_planet = load_image("./images/ring_planet.png")
ball = load_image("./images/ball.png")
big_planet = load_image("./images/big_planet.png")
far_planets = load_image("./images/far_planets.png")
paddle = load_image("./images/paddle.png")

# Declare initial scores for the players
left_player_score = 0
right_player_score = 0

# Declare window height and width
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Declare the paddle speed
PADDLE_INITIAL_SPEED = 10
PADDLE_MOVEMENT_INCREMENT = PADDLE_INITIAL_SPEED

# Declare the collision speed increment constant which responds for how fast the ball will move after collision
BALL_COLLISION_SPEED_INCREMENT_CONSTANT = 2.5

# Declare the collision speed decrement constant which responds for how fast the ball will lose velocity after collision
BALL_COLLISION_SPEED_DECREMENT_CONSTANT = 0.02


# Declare far planets animation speed
FAR_PLANETS_SPEED = 1/5

# Declare far planets coordinates
INITIAL_X_COORDINATE_FAR_PLANETS = 0
INITIAL_Y_COORDINATE_FAR_PLANETS = WINDOW_HEIGHT / 2.5
x_coordinate_far_planets = INITIAL_X_COORDINATE_FAR_PLANETS
y_coordinate_far_planets = INITIAL_Y_COORDINATE_FAR_PLANETS

# Declare stars animation speed
STARS_SPEED = 1/2

# Declare stars coordinates
INITIAL_X_COORDINATE_STARS = 0
INITIAL_Y_COORDINATE_STARS = WINDOW_HEIGHT / 1.8
x_coordinate_stars = INITIAL_X_COORDINATE_STARS
y_coordinate_stars = INITIAL_Y_COORDINATE_STARS

# Declare the ball speed
BALL_INITIAL_SPEED = 4

# Declare ball coordinates
x_coordinate_ball_speed = 0
y_coordinate_ball_speed = 0

# Declare the paddle dimensions
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120

# Declare the ball radius
BALL_RADIUS = 20

# Declare initial paddle coordinates

# Left paddle coordinates
x_coordinate_left_paddle = 0
y_coordinate_left_paddle = 0

# Right paddle coordinates
x_coordinate_right_paddle = WINDOW_WIDTH - PADDLE_WIDTH
y_coordinate_right_paddle = WINDOW_HEIGHT - PADDLE_HEIGHT

# Declare initial ball coordinates
x_coordinate_ball_center = WINDOW_WIDTH/2
y_coordinate_ball_center = WINDOW_HEIGHT/3

# Declare horizontal line points inside the ball
x_coordinate_ball_left_point = x_coordinate_ball_center - BALL_RADIUS
x_coordinate_ball_right_point = x_coordinate_ball_center + BALL_RADIUS

# Declare movement booleans
left_paddle_moving_up = False
left_paddle_moving_down = False
right_paddle_moving_up = False
right_paddle_moving_down = False

# Declare specific booleans
game_did_start = False

# Key bindings
LEFT_PADDLE_MOVE_UP_KEY = 'a'
LEFT_PADDLE_MOVE_DOWN_KEY = 'z'
RIGHT_PADDLE_MOVE_UP_KEY = 'k'
RIGHT_PADDLE_MOVE_DOWN_KEY = 'm'
START_GAME_KEY = ' '
QUIT_GAME_KEY = 'q'

# Change a state variable for a key to a new value, if the key is one of the keys of interest
def change_key_state(key, state):
    global left_paddle_moving_up, left_paddle_moving_down, right_paddle_moving_up, right_paddle_moving_down, game_did_start, x_coordinate_ball_speed, y_coordinate_ball_speed, x_coordinate_ball_center, y_coordinate_ball_center, x_coordinate_left_paddle, y_coordinate_ball_speed, y_coordinate_left_paddle, x_coordinate_right_paddle, y_coordinate_right_paddle

    if key == LEFT_PADDLE_MOVE_UP_KEY and game_did_start:
        left_paddle_moving_up = state

    if key == LEFT_PADDLE_MOVE_DOWN_KEY and game_did_start:
        left_paddle_moving_down = state

    if key == RIGHT_PADDLE_MOVE_UP_KEY and game_did_start:
        right_paddle_moving_up = state

    if key == RIGHT_PADDLE_MOVE_DOWN_KEY and game_did_start:
        right_paddle_moving_down = state

    if key == START_GAME_KEY and game_did_start == False:
        # Mention that the game has started
        game_did_start = state

        # Move the ball to the center
        x_coordinate_ball_center = WINDOW_WIDTH/2
        y_coordinate_ball_center = WINDOW_WIDTH/4

        # Push the ball to south east
        x_coordinate_ball_speed = BALL_INITIAL_SPEED * random.choice([-1, 1])
        y_coordinate_ball_speed = BALL_INITIAL_SPEED * random.choice([-1, 1])

        # Reset left paddle coordinates
        x_coordinate_left_paddle = 0
        y_coordinate_left_paddle = 0

        # Reset right paddle coordinates
        x_coordinate_right_paddle = WINDOW_WIDTH - PADDLE_WIDTH
        y_coordinate_right_paddle = WINDOW_HEIGHT - PADDLE_HEIGHT


    if key == QUIT_GAME_KEY:
        cs1_quit()


# When a key is pressed, if it is one of the keys of interest, record that it was pressed
def process_key_press(key):
    change_key_state(key, True)

# When a key is released, if it is one of the keys of interest, record that it was released
def process_key_release(key):
    # Ignore the Space key
    if key != ' ':
        change_key_state(key, False)

# Draw a paddle
def draw_paddle(x, y):
    # Set color to white
    set_fill_color(1, 1, 1)
    draw_image(paddle, x, y)

# Draw a ball
def draw_ball(x_coordinate_ball_center, y_coordinate_ball_center):
    # Set color to white
    set_fill_color(1, 1, 1)
    draw_image(ball, x_coordinate_ball_center - BALL_RADIUS, y_coordinate_ball_center - BALL_RADIUS)

def check_if_two_lines_collide(x_coordinate_horizontal_line_left_point, x_coordinate_vertical_line, x_coordinate_horizontal_line_right_point, y_coordinate_vertical_line_upper_point, y_coordinate_horizontal_line, y_coordinate_vertical_line_lower_point):
    return x_coordinate_horizontal_line_left_point  < x_coordinate_vertical_line < x_coordinate_horizontal_line_right_point and y_coordinate_vertical_line_upper_point < y_coordinate_horizontal_line < y_coordinate_vertical_line_lower_point

# Render a frame of the animation
def draw_game():
    global y_coordinate_left_paddle, y_coordinate_right_paddle, x_coordinate_ball_center, y_coordinate_ball_center, y_coordinate_ball_speed, x_coordinate_ball_speed, game_did_start, x_coordinate_left_paddle, x_coordinate_right_paddle, x_coordinate_stars, left_player_score, right_player_score, x_coordinate_far_planets

    draw_image(space, -WINDOW_HEIGHT/1.7, 0)
    draw_image(stars, x_coordinate_stars - WINDOW_WIDTH, y_coordinate_stars)
    draw_image(stars, x_coordinate_stars - WINDOW_WIDTH, y_coordinate_stars - WINDOW_HEIGHT / 2)
    draw_image(stars, x_coordinate_stars, y_coordinate_stars)
    draw_image(stars, x_coordinate_stars, y_coordinate_stars - WINDOW_HEIGHT / 2)
    draw_image(far_planets, x_coordinate_far_planets, y_coordinate_far_planets)
    draw_image(far_planets, x_coordinate_far_planets - WINDOW_WIDTH, y_coordinate_far_planets)
    draw_image(ring_planet, WINDOW_WIDTH/12, WINDOW_HEIGHT/1.5)
    draw_image(big_planet, WINDOW_WIDTH/2, 0)

    if game_did_start == False:
        enable_stroke()
        set_stroke_color(1, 1, 1)
        draw_text("Press on Space in order to start the game!", WINDOW_WIDTH/3.5, WINDOW_HEIGHT/2)

    # Draw the paddles

    # Draw left paddle
    draw_paddle(x_coordinate_left_paddle, y_coordinate_left_paddle)
    # Draw right paddle
    draw_paddle(x_coordinate_right_paddle, y_coordinate_right_paddle)

    # Draw the ball
    draw_ball(x_coordinate_ball_center, y_coordinate_ball_center)

    # Move the paddles depending on moving states
    if left_paddle_moving_up:
        y_coordinate_left_paddle -= PADDLE_MOVEMENT_INCREMENT
    if left_paddle_moving_down:
        y_coordinate_left_paddle += PADDLE_MOVEMENT_INCREMENT
    if right_paddle_moving_up:
        y_coordinate_right_paddle -= PADDLE_MOVEMENT_INCREMENT
    if right_paddle_moving_down:
        y_coordinate_right_paddle += PADDLE_MOVEMENT_INCREMENT

    # Move the ball depending on speed for each coordinate
    x_coordinate_ball_center += x_coordinate_ball_speed
    y_coordinate_ball_center += y_coordinate_ball_speed

    # Check for the ball's speed and reverse the acceleration if necessary
    if x_coordinate_ball_speed > BALL_INITIAL_SPEED * (1 + BALL_COLLISION_SPEED_DECREMENT_CONSTANT * 2):
        x_coordinate_ball_speed *= (1 - BALL_COLLISION_SPEED_DECREMENT_CONSTANT)
    if x_coordinate_ball_speed < -BALL_INITIAL_SPEED * (1 - BALL_COLLISION_SPEED_DECREMENT_CONSTANT * 2):
        x_coordinate_ball_speed *= (1 - BALL_COLLISION_SPEED_DECREMENT_CONSTANT)
    if y_coordinate_ball_speed > BALL_INITIAL_SPEED * (1 + BALL_COLLISION_SPEED_DECREMENT_CONSTANT * 2):
        y_coordinate_ball_speed *= (1 - BALL_COLLISION_SPEED_DECREMENT_CONSTANT)
    if y_coordinate_ball_speed < -BALL_INITIAL_SPEED * (1 - BALL_COLLISION_SPEED_DECREMENT_CONSTANT * 2):
        y_coordinate_ball_speed *= (1 - BALL_COLLISION_SPEED_DECREMENT_CONSTANT)

    # Check if the paddles move out of the screen and restrict them accordingly
    if y_coordinate_left_paddle < 0:
        y_coordinate_left_paddle = 0
    if y_coordinate_left_paddle > WINDOW_HEIGHT - PADDLE_HEIGHT:
        y_coordinate_left_paddle = WINDOW_HEIGHT - PADDLE_HEIGHT
    if y_coordinate_right_paddle < 0:
        y_coordinate_right_paddle = 0
    if y_coordinate_right_paddle > WINDOW_HEIGHT - PADDLE_HEIGHT:
        y_coordinate_right_paddle = WINDOW_HEIGHT - PADDLE_HEIGHT

    # Check if the horizontal line inside the ball and the vertical left line of the right paddle intersect and act accordingly
    if check_if_two_lines_collide(x_coordinate_ball_center - BALL_RADIUS, x_coordinate_right_paddle ,x_coordinate_ball_center + BALL_RADIUS, y_coordinate_right_paddle, y_coordinate_ball_center, y_coordinate_right_paddle + PADDLE_HEIGHT):
        x_coordinate_ball_speed = -x_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
        x_coordinate_ball_center -= BALL_RADIUS/2

    # Check if the vertical line inside the ball and the horizontal upper line of the right paddle intersect and act accordingly
    if check_if_two_lines_collide(x_coordinate_right_paddle, x_coordinate_ball_center, x_coordinate_right_paddle + PADDLE_WIDTH, y_coordinate_ball_center - BALL_RADIUS, y_coordinate_right_paddle, y_coordinate_ball_center + BALL_RADIUS):
        y_coordinate_ball_speed = -y_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
        y_coordinate_ball_center -= BALL_RADIUS/2

    # Check if the vertical line inside the ball and the horizontal lower line of the right paddle intersect and act accordingly
    if check_if_two_lines_collide(x_coordinate_right_paddle, x_coordinate_ball_center, x_coordinate_right_paddle + PADDLE_WIDTH, y_coordinate_ball_center - BALL_RADIUS, y_coordinate_right_paddle + PADDLE_HEIGHT, y_coordinate_ball_center + BALL_RADIUS):
        y_coordinate_ball_speed = -y_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
        y_coordinate_ball_center += BALL_RADIUS/2

    # Check if the vertical line inside the ball and the horizontal upper line of the left paddle intersect and act accordingly
    if check_if_two_lines_collide(x_coordinate_left_paddle, x_coordinate_ball_center, x_coordinate_left_paddle + PADDLE_WIDTH, y_coordinate_ball_center - BALL_RADIUS, y_coordinate_left_paddle, y_coordinate_ball_center + BALL_RADIUS):
        y_coordinate_ball_speed = -y_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
        y_coordinate_ball_center -= BALL_RADIUS/2

    # Check if the vertical line inside the ball and the horizontal lower line of the left paddle intersect and act accordingly
    if check_if_two_lines_collide(x_coordinate_left_paddle, x_coordinate_ball_center, x_coordinate_left_paddle + PADDLE_WIDTH, y_coordinate_ball_center - BALL_RADIUS, y_coordinate_left_paddle + PADDLE_HEIGHT, y_coordinate_ball_center + BALL_RADIUS):
        y_coordinate_ball_speed = -y_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
        y_coordinate_ball_center += BALL_RADIUS/2

    # Check if the horizontal line inside the ball and the vertical right line of the left paddle intersect and act accordingly
    if check_if_two_lines_collide(x_coordinate_ball_center - BALL_RADIUS, x_coordinate_left_paddle + PADDLE_WIDTH , x_coordinate_ball_center + BALL_RADIUS, y_coordinate_left_paddle, y_coordinate_ball_center, y_coordinate_left_paddle + PADDLE_HEIGHT):
        x_coordinate_ball_speed = -x_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
        x_coordinate_ball_center += BALL_RADIUS/2

    # Check if the vertical line inside the ball intersects with the upper and lower horizontal line of the screen and act accordingly
    if check_if_two_lines_collide(0, x_coordinate_ball_center, WINDOW_WIDTH, y_coordinate_ball_center - BALL_RADIUS, 0, y_coordinate_ball_center + BALL_RADIUS):
        y_coordinate_ball_speed = -y_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT
    if check_if_two_lines_collide(0, x_coordinate_ball_center, WINDOW_WIDTH, y_coordinate_ball_center - BALL_RADIUS, WINDOW_WIDTH, y_coordinate_ball_center + BALL_RADIUS):
        y_coordinate_ball_speed = -y_coordinate_ball_speed * BALL_COLLISION_SPEED_INCREMENT_CONSTANT

    # Background animation
    x_coordinate_stars += STARS_SPEED
    if x_coordinate_stars > WINDOW_WIDTH:
        x_coordinate_stars = INITIAL_X_COORDINATE_STARS
    x_coordinate_far_planets += FAR_PLANETS_SPEED
    if x_coordinate_far_planets > WINDOW_WIDTH:
        x_coordinate_far_planets = INITIAL_X_COORDINATE_FAR_PLANETS

    # Check if the ball goes of the screen and act accordingly
    if x_coordinate_ball_center > WINDOW_WIDTH or x_coordinate_ball_center < 0:
        # Register the scores
        if x_coordinate_ball_center > WINDOW_WIDTH and game_did_start:
            left_player_score += 1
        if x_coordinate_ball_center < WINDOW_WIDTH and game_did_start:
            right_player_score += 1

        # Mention that the game did not start
        game_did_start = False

        # Stop the ball
        x_coordinate_ball_speed = 0
        y_coordinate_ball_speed = 0

    draw_text("Left Player Score: " + str(left_player_score), WINDOW_WIDTH / 10, WINDOW_HEIGHT - WINDOW_HEIGHT / 10)
    draw_text("Right Player Score: " + str(right_player_score),WINDOW_WIDTH - WINDOW_WIDTH/ 3, WINDOW_HEIGHT - WINDOW_HEIGHT / 10)

# Start the game.
start_graphics(draw_game, title = "Galaxy Pong", width = WINDOW_WIDTH, height = WINDOW_HEIGHT,
               framerate = 60, key_press = process_key_press, key_release = process_key_release)