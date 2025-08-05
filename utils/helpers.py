import random

# ✅ Football GIFs for animation
GIFS = [
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",
    # ➕ Add more GIFs if needed
]

def random_football_gif() -> str:
    """
    Returns a random football-related GIF URL.
    """
    return random.choice(GIFS)

def referee_image() -> str:
    """
    Returns the referee image URL.
    """
    return "https://i.imgur.com/jySqKyz.jpg"  # Replace with your custom referee image if needed

def organiser_image() -> str:
    """
    Returns the organiser image URL.
    """
    return "https://i.imgur.com/zL3Tb7T.jpg"  # Replace with your custom organiser image if needed

def get_player_position(username: str) -> tuple[int, int]:
    """
    Generates a position (x, y) based on the player's username.
    This helps simulate positioning on a virtual football field.
    """
    if not username:
        username = "default"

    x = sum(ord(c) for c in username) % 10  # X coordinate: 0-9
    y = len(username) % 6                   # Y coordinate: 0-5

    return x, y
