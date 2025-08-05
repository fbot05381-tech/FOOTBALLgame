# Group-based game data
games = {}  # {chat_id: {
             #   "referee": user_id,
             #   "teamA": [user_ids],
             #   "teamB": [user_ids],
             #   "captains": {"A": user_id, "B": user_id},
             #   "goalkeepers": {"A": user_id, "B": user_id},
             #   "score": {"A": 0, "B": 0},
             #   "round": 0,
             #   "current_player": user_id,
             #   "ball_holder": user_id,
             #   "yellow_cards": {user_id: 1},
             #   "red_cards": [user_ids]
             # }}

# User to game mapping (useful to restrict multi-join)
user_game = {}  # {user_id: chat_id}

# Tournaments
tournaments = {}  # {chat_id: tournament_info}

# Game state control
game_states = {}  # {chat_id: "playing" / "paused" / "waiting"}

# Player-specific data
player_states = {}  # {user_id: {"game": chat_id, "team": "A" or "B"}}

# Referee vote logic
referee_votes = {}  # {chat_id: {user_id: True/False}}
