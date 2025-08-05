import random

# Football GIFs for animation
GIFS = [
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",
    # Aap chahein to aur GIFs yahan add kar sakte hain
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
    return "https://i.imgur.com/jySqKyz.jpg"  # You can change to your own

def organiser_image() -> str:
    """
    Returns the organiser image URL.
    """
    return "https://i.imgur.com/zL3Tb7T.jpg"  # You can change to your own
