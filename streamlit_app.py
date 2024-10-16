import streamlit as st
import numpy as np
import random
import time

# Game settings
GRID_SIZE = 10
INITIAL_SNAKE_LENGTH = 3

# Initialize the game state
def initialize_game():
    snake = [(0, i) for i in range(INITIAL_SNAKE_LENGTH)]
    direction = (0, 1)  # Start moving to the right
    food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while food in snake:
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    return snake, direction, food

# Draw the game grid
def draw_grid(snake, food):
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    for (x, y) in snake:
        grid[x, y] = 1  # Snake body
    grid[food] = 2  # Food
    return grid

# Update the snake position
def update_snake(snake, direction):
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    snake.insert(0, new_head)
    return snake

# Check for collisions
def check_collision(snake, food):
    return snake[0] == food

# Streamlit app
st.title("Snake Game")

# Initialize game state
if 'snake' not in st.session_state:
    st.session_state.snake, st.session_state.direction, st.session_state.food = initialize_game()
    st.session_state.score = 0

# User controls
if st.button("Up"):
    st.session_state.direction = (-1, 0)
if st.button("Down"):
    st.session_state.direction = (1, 0)
if st.button("Left"):
    st.session_state.direction = (0, -1)
if st.button("Right"):
    st.session_state.direction = (0, 1)

# Game loop
while True:
    time.sleep(0.2)  # Control the speed of the game

    # Update the snake
    st.session_state.snake = update_snake(st.session_state.snake, st.session_state.direction)

    # Check for collisions with food
    if check_collision(st.session_state.snake, st.session_state.food):
        st.session_state.score += 1
        st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        while st.session_state.food in st.session_state.snake:
            st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    else:
        st.session_state.snake.pop()  # Remove the tail if no food eaten

    # Check for collisions with walls or self
    head_x, head_y = st.session_state.snake[0]
    if (head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE or
            len(st.session_state.snake) != len(set(st.session_state.snake))):
        st.write("Game Over! Score: ", st.session_state.score)
        break

    # Draw the game grid
    grid = draw_grid(st.session_state.snake, st.session_state.food)
    st.write(grid)

    st.write("Score: ", st.session_state.score)
    st.experimental_rerun()
