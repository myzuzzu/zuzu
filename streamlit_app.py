import streamlit as st
import numpy as np
import random

# Game settings
GRID_SIZE = 5
NUM_CATS = 3

# Initialize the game state
def initialize_game():
    cats = []
    for _ in range(NUM_CATS):
        cat_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        while cat_position in cats:
            cat_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        cats.append(cat_position)
    return cats

# Draw the game grid
def draw_grid(cats, score):
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=str)
    for (x, y) in cats:
        grid[x, y] = "🐱"  # Cat emoji
    grid_string = "\n".join(" ".join(row) for row in grid)
    return grid_string

# Streamlit app
st.title("Catch the Cats Game")

# Initialize game state
if 'cats' not in st.session_state:
    st.session_state.cats = initialize_game()
    st.session_state.score = 0

# Display the grid
grid_string = draw_grid(st.session_state.cats, st.session_state.score)
st.write(grid_string)

# User interaction
selected_cat = st.selectbox("Select a cat position to catch:", [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)])

if st.button("Catch Cat"):
    if selected_cat in st.session_state.cats:
        st.session_state.cats.remove(selected_cat)
        st.session_state.score += 1
        st.success("Cat caught! 🎉")
    else:
        st.error("No cat at that position! 😿")

# Check for game end
if len(st.session_state.cats) == 0:
    st.write("All cats caught! Your score: ", st.session_state.score)
    if st.button("Restart Game"):
        st.session_state.cats = initialize_game()
        st.session_state.score = 0

  
