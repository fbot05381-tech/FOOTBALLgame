def get_player_position(username: str) -> tuple[int, int]:
    if not username:
        username = "default"

    x = sum(ord(c) for c in username) % 10  # X coordinate: 0-9
    y = len(username) % 6                   # Y coordinate: 0-5

    return x, y
