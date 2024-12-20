import json

# Categorize members based on their roles
def categorize_members(members):
    guild_master = []
    healers = []
    dps = []
    new_dps = []
    new_healers = []

    for member in members:
        if member["role"] == "guild master":
            guild_master.append(member)
        elif member["role"] == "healer":
            healers.append(member)
        elif member["role"] == "dps":
            dps.append(member)
        elif member["role"] == "new dps":
            new_dps.append(member)
        elif member["role"] == "new healer":
            new_healers.append(member)

    return guild_master, healers, dps, new_dps, new_healers

# Normalize the tenure to be used as a weight factor
def get_tenure_weight(tenure):
    # Number of months in the guild
    tenure_months = {
        "December 2023": 12, "February 2024": 10, "May 2024": 7,
        "August 2024": 4, "October 2024": 3, "November 2024": 2, "December 2024": 1
    }
    return tenure_months.get(tenure, 0)

# Get average parse across raids for each role and return a list of dictionaries
def get_average_parse_across_raids(parses, role_list, role):
    role_totals = {}

    # Iterate through the list of categorized members
    for member in role_list:
        player_name = member["name"]
        tenure = member["tenure"]
        
        # Search for the player's parse data across all raids
        for data in parses.values():
            if role in data:
                for parse in data[role]:
                    if parse["name"] == player_name:
                        avg_parse = parse["avg"]
                        if player_name in role_totals:
                            role_totals[player_name]["total_performance"] += avg_parse
                            role_totals[player_name]["raid_count"] += 1
                        else:
                            role_totals[player_name] = {
                                "total_performance": avg_parse,  # Accumulated performance
                                "raid_count": 1, 
                                "tenure": tenure
                            }

    # Convert the totals into a list of dictionaries with avg_parse and tenure
    role_averages = [
        {
            "name": name,
            "avg_parse": totals["total_performance"] / totals["raid_count"],
            "tenure": totals["tenure"]
        }
        for name, totals in role_totals.items()
    ]

    return role_averages


def apply_weighting_system(role_list, is_new_role=False):
    weighted_list = []

    # Calculate the max and min of avg_parse to use for scaling
    avg_parses = [member['avg_parse'] for member in role_list]
    max_avg_parse = max(avg_parses)
    min_avg_parse = min(avg_parses)

    for member in role_list:
        avg_parse = member['avg_parse']
        tenure = member['tenure']
        weight = get_tenure_weight(tenure) if not is_new_role else 0  # Ignore tenure for new roles
        
        # Normalize the tenure weight by avg_parse
        if avg_parse > 0:
            if max_avg_parse > min_avg_parse:  # To avoid division by zero
                normalized_avg_parse = (avg_parse - min_avg_parse) / (max_avg_parse - min_avg_parse)
            else:
                normalized_avg_parse = 0  # If all avg_parse values are the same

            # Apply tenure weighting based on normalized avg_parse
            tenure_weighted = weight * normalized_avg_parse
        else:
            tenure_weighted = 0
        
        # Calculate weighted score
        weighted_score = avg_parse + tenure_weighted
        weighted_list.append({
            'name': member['name'],
            'avg_parse': avg_parse,
            'tenure': tenure,
            'weighted_score': weighted_score
        })

    # Return sorted list based on weighted score
    return sorted(weighted_list, key=lambda x: x['weighted_score'], reverse=True)

# Print in readable format
def print_priorities(role_name, sorted_parses):
    print(f"\nSorted {role_name}:")
    for rank, player in enumerate(sorted_parses, start=1):
        print(f"{rank}. {player['name']} - Avg Parse: {player['avg_parse']:.2f}, "
              f"Tenure: {player['tenure']}, Weighted Score: {player['weighted_score']:.2f}")

def main():
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    parses = data.get('parses', {})
    members = data.get('members', [])

    # Categorize the members by their roles
    guild_master, healers, dps, new_dps, new_healers = categorize_members(members)

    # Sort each categorized group, by parse, and average them across all raids
    new_healer_parses_sorted = get_average_parse_across_raids(parses, new_healers, "healers")
    new_dps_parses_sorted = get_average_parse_across_raids(parses, new_dps, "dps")
    dps_parses_sorted = get_average_parse_across_raids(parses, dps, "dps")
    healer_parses_sorted = get_average_parse_across_raids(parses, healers, "healers")

    # Apply weighting system (tenure affects only DPS and Healers)
    priority_dps = apply_weighting_system(dps_parses_sorted)
    priority_healers = apply_weighting_system(healer_parses_sorted)

    # Apply weighting system without considering tenure (only for new guildies)
    priority_new_dps = apply_weighting_system(new_dps_parses_sorted, is_new_role=True)
    priority_new_healers = apply_weighting_system(new_healer_parses_sorted, is_new_role=True)

    # Output the priority lists
    print_priorities("Priority DPS", priority_dps)
    print_priorities("Priority Healers", priority_healers)
    print_priorities("Priority New DPS", priority_new_dps)
    print_priorities("Priority New Healers", priority_new_healers)

if __name__ == "__main__":
    main()
