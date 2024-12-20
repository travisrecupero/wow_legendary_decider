# Legendary Item Priority Calculation

This script is designed to calculate and prioritize players based on their role, average performance (parse), and tenure in the guild. The program processes player data from a given JSON input and sorts them according to the weighted score, which factors in both average parse and the length of time the player has been with the guild.

## Overview

The program works in the following steps:

1. **Categorize Players**: Players are categorized into roles like `dps`, `healer`, `new dps`, and `new healer` based on their role in the guild.
2. **Parse Data**: The program then processes raid parse data to calculate each player's average performance across multiple raids.
3. **Weighting System**: A weighting system is applied to factor in the player's tenure in the guild. The longer the player's tenure, the higher the weight applied to their average parse, influencing their final ranking.
4. **Sorting**: Players are then sorted based on their weighted scores for each category (Priority DPS, Priority Healers, etc.).

## JSON Input Example

```json
{
  "members": [
    {"name": "Maege", "role": "dps", "tenure": "December 2023", "attendance": 100},
    {"name": "Bremmy", "role": "healer", "tenure": "February 2024", "attendance": 100},
    {"name": "Bombalabomba", "role": "healer", "tenure": "June 2024", "attendance": 100},
    {"name": "Holocene", "role": "healer", "tenure": "August 2024", "attendance": 100},
    {"name": "Darkagony", "role": "dps", "tenure": "October 2024", "attendance": 100},
    {"name": "Bboyboog", "role": "dps", "tenure": "August 2024", "attendance": 100},
    {"name": "Derithas", "role": "dps", "tenure": "May 2024", "attendance": 100},
    {"name": "Starlitmagi", "role": "new dps", "tenure": "November 2024", "attendance": 100},
    {"name": "Mysticke", "role": "new dps", "tenure": "December 2024", "attendance": 100},
    {"name": "Droplock", "role": "new dps", "tenure": "December 2024", "attendance": 100},
    {"name": "Asmondot", "role": "new dps", "tenure": "December 2024", "attendance": 100},
    {"name": "Poosocks", "role": "new healer", "tenure": "December 2024", "attendance": 100},
    {"name": "Gisun", "role": "new healer", "tenure": "December 2024", "attendance": 100}
  ],
  "parses": {
    "molten_core_heat_2": {
      "dps": [
        {"name": "Maege", "avg": 65.9},
        {"name": "Derithas", "avg": 48.6},
        {"name": "Holocene", "avg": 44.5},
        {"name": "Bboyboog", "avg": 22.9}
      ],
      "healers": [
        {"name": "Bremmy", "avg": 84.3},
        {"name": "Bombalabomba", "avg": 83.8},
        {"name": "Holocene", "avg": 65.5}
      ]
    },
    "blackwing_lair_mythic": {
      "dps": [
        {"name": "Darkagony", "avg": 95.2},
        {"name": "Maege", "avg": 83.7},
        {"name": "Bboyboog", "avg": 81.2},
        {"name": "Holocene", "avg": 71.6},
        {"name": "Derithas", "avg": 69.5}
      ],
      "healers": [
        {"name": "Holocene", "avg": 79.8},
        {"name": "Bremmy", "avg": 70.7},
        {"name": "Bombalabomba", "avg": 57.2}
      ]
    },
    "temple_of_ahnqiraj_heroic": {
      "dps": [
        {"name": "Asmondot", "avg": 89.0},
        {"name": "Darkagony", "avg": 86.9},
        {"name": "Maege", "avg": 81.8},
        {"name": "Droplock", "avg": 73.8},
        {"name": "Holocene", "avg": 71.4},
        {"name": "Bboyboog", "avg": 51.7},
        {"name": "Derithas", "avg": 49.6},
        {"name": "Mysticke", "avg": 27.8},
        {"name": "Starlitmagi", "avg": 23.6}
      ],
      "healers": [
        {"name": "Gisun", "avg": 83.4},
        {"name": "Bremmy", "avg": 82.3},
        {"name": "Bombalabomba", "avg": 82.0},
        {"name": "Holocene", "avg": 74.6},
        {"name": "Poosocks", "avg": 45.3}
      ]
    }
  }
}
```
## Example Output

When you run the script, you will get the following sorted output based on priority:
```text
Sorted Priority DPS:
1. Darkagony - Avg Parse: 91.05, Tenure: October 2024, Weighted Score: 94.05
2. Maege - Avg Parse: 77.13, Tenure: December 2023, Weighted Score: 84.86
3. Holocene - Avg Parse: 62.50, Tenure: August 2024, Weighted Score: 63.58
4. Derithas - Avg Parse: 55.90, Tenure: May 2024, Weighted Score: 56.61
5. Bboyboog - Avg Parse: 51.93, Tenure: August 2024, Weighted Score: 51.93

Sorted Priority Healers:
1. Bremmy - Avg Parse: 79.10, Tenure: February 2024, Weighted Score: 89.10
2. Bombalabomba - Avg Parse: 74.33, Tenure: June 2024, Weighted Score: 74.33
3. Holocene - Avg Parse: 73.30, Tenure: August 2024, Weighted Score: 73.30

Sorted Priority New DPS:
1. Asmondot - Avg Parse: 89.00, Tenure: December 2024, Weighted Score: 89.00
2. Droplock - Avg Parse: 73.80, Tenure: December 2024, Weighted Score: 73.80
3. Mysticke - Avg Parse: 27.80, Tenure: December 2024, Weighted Score: 27.80
4. Starlitmagi - Avg Parse: 23.60, Tenure: November 2024, Weighted Score: 23.60

Sorted Priority New Healers:
1. Gisun - Avg Parse: 83.40, Tenure: December 2024, Weighted Score: 83.40
2. Poosocks - Avg Parse: 45.30, Tenure: December 2024, Weighted Score: 45.30
```

## Math Behind the Weighted Score

The weighted score is calculated as follows:

1. **Average Parse**: This is the average performance (parse) for a player across multiple raids. It's calculated by averaging the "avg" value for each player's parses in all raids.

2. **Tenure Weighting**: The tenure weight is based on how long the player has been in the guild. Players with longer tenure receive a higher weight. The tenure weight is determined by a predefined mapping (e.g., 12 months for "December 2023" and so on). For new roles, tenure does not affect the weighting.

3. **Weighted Score Calculation**:
    - Normalize the average parse value to a range of 0 to 1 based on the min and max parses within the group.
    - Multiply the normalized average parse by the tenure weight to calculate the weighted score.

    Formula:
    `Weighted Score = Average Parse + (Normalized Avg Parse * Tenure Weight)`

4. **Sorting**: Players are then sorted based on their weighted score, with the highest weighted score ranking first.
