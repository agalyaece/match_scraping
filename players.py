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




import pandas as pd
from itertools import combinations

def change_role(role):
  if 'Allrounder' in role:
    return 'Allrounder'
  elif 'Batter' in role:
    return 'Batter'
  elif 'Wicketkeeper' in role:
    return 'Wicketkeeper'
  else:
    return role

def generate_valid_teams(players, country1, country2):
    def is_valid(team):


        # Check if the team satisfies constraints
        MAX_CREDITS = 100
        MAX_PLAYERS_PER_TEAM = 7
        ROLE_LIMITS = {
            "Wicketkeeper": (1, 4),
            "Batter": (2, 6),
            "Allrounder": (1, 4),
            "Bowler": (2, 6),
        }
        fan_ratings = 0
        # Use a case-insensitive dictionary for team counts
        team_counts = {country1.lower(): 0, country2.lower(): 0}
        role_counts = {role: 0 for role in ROLE_LIMITS}

        for player in team:
            fan_ratings += player["fan-ratings"]
            # Convert team name to lowercase for comparison
            team_counts[player["country"].lower()] += 1
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

    valid_teams = []
    for team in combinations(players, 11):  # Generate all 11-player combinations
        if is_valid_team(team):
            valid_teams.append(team)
    return valid_teams



# Load the players data
players_df = pd.read_csv("players_data.csv")

print(players_df['country'].unique())

# Replace roles
players_df['role'] = players_df['role'].apply(change_role)

# Get country names from user input
country1 = input("Enter the first country name: ")
country2 = input("Enter the second country name: ")

# Generate and print valid teams
for team in generate_valid_teams(players_df, country1, country2):
         print("Valid Team:")
         for i, player in enumerate(team):
             print(f"{i+1}. {player['player_name_x']} ({player['country']}) - {player['role']} - Fan Rating: {player['fan-ratings']}")
         print("-" * 20)

# Generate valid teams
valid_teams = generate_valid_teams(players_df, country1, country2)

# Create a list to store team data in a flattened format
team_data = []
for i, team in enumerate(valid_teams):
    for j, player in enumerate(team):
        team_data.append({
            'team_number': i + 1,
            'player_number': j + 1,
            'player_name': player['player_name_x'],
            'country': player['country'],
            'role': player['role'],
            'fan_ratings': player['fan-ratings']
        })
# print(team_data)
# Create a DataFrame from the team data
teams_df = pd.DataFrame(team_data)

# Save the DataFrame to a CSV file
teams_df.to_csv('valid_teams.csv', index=False)
print("Valid teams saved to 'valid_teams.csv'")