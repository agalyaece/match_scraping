import pandas as pd

# Sample player data
df = pd.read_csv("PlayerData.csv")

# Convert DataFrame to a list of player dictionaries
players = df.to_dict('records')

# Constraints
MAX_CREDITS = 100
MAX_PLAYERS_PER_TEAM = 7
ROLE_LIMITS = {
    "wicketkeeper": (1, 4),
    "batsman": (3, 6),
    "allrounder": (1, 4),
    "bowler": (3, 6),
}


def is_valid_team(team):
    """Checks if a team satisfies all constraints."""
    credits = 0
    team_counts = {"CSK": 0, "MI": 0}
    role_counts = {role: 0 for role in ROLE_LIMITS}

    for player in team:
        credits += player["credits"]
        team_counts[player["team"]] += 1
        role_counts[player["role"]] += 1

    if credits > MAX_CREDITS:
        return False

    for team, count in team_counts.items():
        if count > MAX_PLAYERS_PER_TEAM:
            return False

    for role, (min_count, max_count) in ROLE_LIMITS.items():
        if not (min_count <= role_counts[role] <= max_count):
            return False

    return True



from itertools import combinations


def find_valid_teams(players):
    """Finds all valid teams from the given players."""
    valid_teams = []
    for team in combinations(players, 11):  # Generate all 11-player combinations
        if is_valid_team(team):
            valid_teams.append(team)
    return valid_teams


# Find valid teams
valid_teams = find_valid_teams(players)

print(valid_teams)
# Print the valid teams
for team in valid_teams:
    print([player["name"] for player in team])


def calculate_win_probability(team):
    """Calculates win probability based on average fan rating."""
    total_fan_rating = sum(player["credits"] for player in team)
    print(total_fan_rating)
    average_fan_rating = total_fan_rating / len(team)

    # Normalize fan rating (assuming ratings are between 0 and 10)
    normalized_rating = average_fan_rating / 10

    # Linearly map normalized rating to win probability
    win_probability = normalized_rating

    return win_probability


# Example usage:
selected_team = valid_teams  # List of player dictionaries
win_prob = calculate_win_probability(selected_team)
print("Win Probability:", win_prob)


def generate_valid_teams(players):
    def is_valid(team):
        # Check if the team satisfies constraints
        MAX_CREDITS = 100
        MAX_PLAYERS_PER_TEAM = 7
        ROLE_LIMITS = {
            "wicketkeeper": (1, 4),
            "batsman": (3, 6),
            "allrounder": (1, 4),
            "bowler": (3, 6),
        }
        fan_ratings = 0
        team_counts = {"CSK": 0, "MI": 0}
        role_counts = {role: 0 for role in ROLE_LIMITS}

        for player in team:
            fan_ratings += player["fan-ratings"]
            team_counts[player["team"]] += 1
            role_counts[player["role"]] += 1

        if fan_ratings > MAX_CREDITS:
            return False

        for team, count in team_counts.items():
            if count > MAX_PLAYERS_PER_TEAM:
                return False

        for role, (min_count, max_count) in ROLE_LIMITS.items():
            if not (min_count <= role_counts[role] <= max_count):
                return False
        return True

    for team in combinations(players, 11):
        if is_valid(team):
            yield team

# Use the generator function
for team in generate_valid_teams(players):
    print(team)