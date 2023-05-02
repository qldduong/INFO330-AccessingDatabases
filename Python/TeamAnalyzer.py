import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters


# Run CMD code: python TeamAnalyzer.py 1 2 3 4 5 6
# Extra credit test: python3 TeamAnalyzer.py Bulbasaur Ivysaur Venusaur 4 5 6
# C:\Users\renti\Documents\INFO330\INFO330-AccessingDatabases\Python


# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]


connection = sqlite3.connect("../pokemon.sqlite")
cursor = connection.cursor()



# Take six parameters on the command-line

# Code to accept user input:
# My added code: --------------------------------------------
"""
sys.argv = []
print("Please input 6 valid pokemon names and/or IDs")
pok_count = 0
while pok_count < 6:
    current_pokemon = input("ID or name of pokemon" + " " + str(pok_count+1) + ": ")
    sys.argv.append(current_pokemon)
    pok_count += 1
    print(sys.argv)
"""
# My added code: --------------------------------------------

if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []

# Not sure how to get names / types as just strings and not part of a list
# This method cleans list items up for readability
def cleaning(string_to_clean):
    string_to_clean = string_to_clean.replace("'", "")
    string_to_clean = string_to_clean.replace("(", "")
    string_to_clean = string_to_clean.replace(")", "")
    string_to_clean = string_to_clean.replace(",", "")
    return(string_to_clean)

 
for i, arg in enumerate(sys.argv):

    if i == 0:
        continue

    # EXTRA CREDIT
    # If the user input is composed of digits, then it's treated as an ID 
    # Otherwise, it's treated as a string of just the pokemon's name
    # Only works if the user capitalizes the first letter of the pokemon's name
    if arg.isdigit():
        # Getting the name of each pokemon 
        name_sql = "SELECT name FROM pokemon WHERE id = ?"
        name_results = cursor.execute(name_sql, [arg])
        pok_name = name_results.fetchall()
        pok_name = str(pok_name[0])
    
        # Cleaning up the name 
        pok_name = cleaning(pok_name)
    else:
        pok_name = arg
    
    # Getting the type(s) of the pokemon 
    type1_sql = "SELECT type1 FROM pokemon_types_view WHERE name = ?"
    type1_results = cursor.execute(type1_sql, [pok_name])
    type1 = type1_results.fetchall()
    type1 = str(type1[0])

    type2_sql = "SELECT type2 FROM pokemon_types_view WHERE name = ?"
    type2_results = cursor.execute(type2_sql, [pok_name])
    type2 = type2_results.fetchall()
    type2 = str(type2[0])

    type1 = cleaning(type1)
    type2 = cleaning(type2)


    # SQL for getting the list of against_x for the pokemon (based on its type(s))
    effectiveness_sql = """SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, 
    against_fight, against_fire, against_flying, against_ghost, 
    against_grass, against_ground, against_ice, against_normal, 
    against_poison, against_psychic, against_rock, against_steel, against_water 
    FROM pokemon_types_battle_view WHERE type1name = ? AND type2name = ?
    """
    # Passing parameters into the placeholders in the SQL statement
    type_parameters = [type1, type2]
    effect_results = cursor.execute(effectiveness_sql, type_parameters)
    effects_list = effect_results.fetchall()

    # Initializing the weak[] and strong[] lists for the pokemon
    strong = []
    weak = []

    # Assigns types to the weak / strong lists (val < 1 --> strong || val > 1 --> weak)
    type_counter = 0
    for ef_tup in effects_list:
        for ef_num in ef_tup:
            if float(ef_num) < 1.0:
                strong.append(types[type_counter])
            elif float(ef_num) > 1.0:
                weak.append(types[type_counter])
            type_counter += 1
    print()

    print(pok_name + " (" + str(type1) + " " + str(type2) + ") is strong against " + str(strong) + " but weak against " + str(weak))
    

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")
