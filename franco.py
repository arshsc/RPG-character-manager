# FB 1st Character manager
import sys, random, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from faker import Faker
from Editing_function import editcharacters

fake = Faker()

class RandomGenerator:
    races = ["Human", "Elf", "Dwarf", "Gnome", "Halfling", "Dragonborn", "Tiefling", "Half-Orc"]
    classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
    quests = [
        "Retrieve the stolen artifact from the dungeon.",
        "Escort the merchant through Darkwood Forest.",
        "Investigate disappearances in the northern village.",
        "Defeat the dragon terrorizing the coast.",
        "Uncover the traitor in the king's court.",
    ]
    def generate_character(self):
        name = fake.name()
        race = random.choice(self.races)
        character_class = random.choice(self.classes)
        level = random.randint(1, 20)
        attribute_names = ["strength", "dexterity", "intelligence", "wisdom", "constitution", "health", "armor class", "charisma"]
        attribute_scores = [random.randint(8, 18) for _ in attribute_names]
        backstory = f"{name} is a {race} {character_class} from {fake.city()}. They used to work as a {fake.job()}. {fake.sentence()}"
        character = {
            "simpleinfo": (race, character_class),
            "level": level,
            "Items_Dictionary": {"Weapon": ["None", "Weapon", "None"], "Armor": ["None", "Armor", "None"], "Inventory": []},
            "skills": set(),
            "attributes": [attribute_names, attribute_scores],
            "backstory": backstory
        }
        return name, character
    def random_quest(self):
        return random.choice(self.quests)


class StatisticalAnalyzer:
    def __init__(self, database):
        rows = []
        for name, data in database.items():
            row = {"name": name, "race": data["simpleinfo"][0], "class": data["simpleinfo"][1], "level": data["level"]}
            for attribute, value in zip(data["attributes"][0], data["attributes"][1]):
                row[attribute] = value
            rows.append(row)
        self.dataframe = pd.DataFrame(rows)
    def print_report(self):
        print("\nRoster:")
        print(self.dataframe[["name", "race", "class", "level"]].to_string(index=False))
        stat_columns = [c for c in self.dataframe.columns if c not in ["name", "race", "class", "level"]]
        print("\nStat Summary:")
        print(self.dataframe[stat_columns].agg(["mean", "median", "max", "min"]).round(2).to_string())
    def top_by_stat(self, stat):
        if stat not in self.dataframe.columns:
            print("Stat not found.")
            return
        print(self.dataframe[["name", stat]].sort_values(stat, ascending=False).head(3).to_string(index=False))
    def filter_by_class(self, character_class):
        print(self.dataframe[self.dataframe["class"].str.lower() == character_class.lower()].to_string(index=False))
    def filter_by_race(self, race):
        print(self.dataframe[self.dataframe["race"].str.lower() == race.lower()].to_string(index=False))
    def export_csv(self):
        self.dataframe.to_csv("characters.csv", index=False)
        print("Exported to characters.csv")


class DataVisualization:
    def bar_chart(self, name, data):
        figure, axis = plt.subplots(figsize=(10, 5))
        bars = axis.bar(data["attributes"][0], data["attributes"][1], color="steelblue", edgecolor="black")
        axis.bar_label(bars, padding=3)
        axis.set_title(f"{name} Stats")
        axis.set_ylabel("Score")
        axis.set_ylim(0, 25)
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(f"{name}_bar.png")
        print(f"Saved {name}_bar.png - open the file in the Explorer panel to view it.")
        plt.close()
    def radar_chart(self, name, data):
        labels = data["attributes"][0]
        values = data["attributes"][1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values_closed = values + [values[0]]
        angles_closed = angles + [angles[0]]
        figure, axis = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        axis.plot(angles_closed, values_closed, "o-", linewidth=2)
        axis.fill(angles_closed, values_closed, alpha=0.25)
        axis.set_thetagrids(np.degrees(angles), labels)
        axis.set_title(f"{name} Radar Chart", pad=15)
        axis.set_ylim(0, 20)
        plt.tight_layout()
        plt.savefig(f"{name}_radar.png")
        print(f"Saved {name}_radar.png - open the file in the Explorer panel to view it.")
        plt.close()
    def comparison_bar(self, database):
        stat_columns = ["strength", "dexterity", "intelligence", "wisdom", "constitution", "charisma"]
        character_names = list(database.keys())
        positions = np.arange(len(stat_columns))
        bar_width = 0.8 / len(character_names)
        figure, axis = plt.subplots(figsize=(12, 6))
        for index, name in enumerate(character_names):
            attribute_names = database[name]["attributes"][0]
            attribute_scores = database[name]["attributes"][1]
            values = [attribute_scores[attribute_names.index(stat)] if stat in attribute_names else 0 for stat in stat_columns]
            axis.bar(positions + index * bar_width, values, bar_width, label=name)
        axis.set_xticks(positions + bar_width * (len(character_names) - 1) / 2)
        axis.set_xticklabels(stat_columns, rotation=20, ha="right")
        axis.set_ylabel("Score")
        axis.set_title("Character Comparison")
        axis.legend()
        plt.tight_layout()
        plt.savefig("comparison_bar.png")
        print("Saved comparison_bar.png - open the file in the Explorer panel to view it.")
        plt.close()
    def class_distribution(self, database):
        classes = [database[name]["simpleinfo"][1] for name in database]
        figure, axis = plt.subplots(figsize=(8, 5))
        axis.bar(set(classes), [classes.count(c) for c in set(classes)], color="coral", edgecolor="black")
        axis.set_title("Class Distribution")
        axis.set_xlabel("Class")
        axis.set_ylabel("Number of Characters")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig("class_distribution.png")
        print("Saved class_distribution.png - open the file in the Explorer panel to view it.")
        plt.close()
    def level_progression(self, database):
        names = list(database.keys())
        levels = [database[name]["level"] for name in names]
        figure, axis = plt.subplots(figsize=(10, 5))
        axis.bar(names, levels, color="mediumseagreen", edgecolor="black")
        axis.set_title("Character Level Progression")
        axis.set_xlabel("Character")
        axis.set_ylabel("Level")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig("level_progression.png")
        print("Saved level_progression.png - open the file in the Explorer panel to view it.")
        plt.close()


def validate_input(text, kind='int'):
    s = str(text).strip().capitalize()
    if kind == 'int':
        try:
            int(s)
            return True
        except ValueError:
            return False
    elif kind == 'float':
        try:
            float(s)
            return True
        except ValueError:
            return False
    elif kind == 'alpha':
        return s.isalpha()
    else:
        return False

def inputchecker(rangeofchoices):
    while True:
        choicevar = input(f"\nWhich one would you like to choose? (1 - {rangeofchoices})\n").strip().capitalize()
        try:
            choicevar = int(choicevar)
            if choicevar in range(1, rangeofchoices + 1):
                break
            else:
                print("That's not an option :(")
        except:
            print("Please enter a valid integer number.")
    return choicevar

def letter_input(options):
    while True:
        choice = input("\nEnter your choice: ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice.")

def viewchars(data):
    characternameandlistnum = {}
    count = 1
    for character in data.keys():
        characternameandlistnum[count] = character
        print(f"{count}. {character} : {data[character]['simpleinfo'][0]}, {data[character]['simpleinfo'][1]}, Level {data[character]['level']}")
        count += 1
    print("\n1. Select\n2. Sort\n3. Main Menu")
    choice = inputchecker(3)
    match choice:
        case 1: select(data, characternameandlistnum)
        case 2: sortchoice(data)
        case 3: return

def select(data, selectionmenu):
    for num, character in selectionmenu.items():
        print(f"{num}. {character} : {data[character]['simpleinfo'][0]}, {data[character]['simpleinfo'][1]}, Level {data[character]['level']}")
    characternum = inputchecker(len(selectionmenu))
    character = selectionmenu[characternum]
    print(f"\n{character} : {data[character]['simpleinfo'][0]}, {data[character]['simpleinfo'][1]}, Level {data[character]['level']}")
    print("\nInventory:")
    for itemslot in data[character]["Items_Dictionary"].keys():
        item = data[character]["Items_Dictionary"][itemslot]
        try:
            print(f"   - {itemslot}: {item[0]}, it is a {item[1]}, and {item[2]} can use it!")
        except:
            continue
    print("\nSkills:")
    for skill in data[character]["skills"]:
        print(f"   - {skill[0]}: {skill[1]}")
    count = 0
    print("\nAttributes:")
    for attribute in data[character]["attributes"][0]:
        print(f"   - {attribute.title()}: {data[character]['attributes'][1][count]}")
        count += 1
    print("\n1. Edit\n2. Main Menu")
    answer = inputchecker(2)
    match answer:
        case 1: editcharacters(data)
        case 2: return

def sortoptions(data, *typeindex):
    previoustypes = []
    typelist = {}
    count = 1
    for character in data.keys():
        if data[character]["simpleinfo"][typeindex] not in previoustypes:
            previoustypes.append(data[character]["simpleinfo"][typeindex])
            print(f"{count}. {data[character]['simpleinfo'][typeindex]}")
            typelist[count] = data[character]["simpleinfo"][typeindex]
            count += 1
    return typelist

def sorter(data, choice, types, *typeindex):
    characternameandlistnum = {}
    count = 1
    for character in data.keys():
        if data[character]["simpleinfo"][typeindex] == types[choice]:
            characternameandlistnum[count] = character
            print(f"{count}. {character} : {data[character]['simpleinfo'][0]}, {data[character]['simpleinfo'][1]}, Level {data[character]['level']}")
            count += 1
    print("\n1. Select\n2. Main Menu")
    choice = inputchecker(2)
    match choice:
        case 1: select(data, characternameandlistnum)

def sortchoice(data):
    print("\n1. Race\n2. Class\n3. Level")
    sortby = inputchecker(3)
    match sortby:
        case 1:
            distinct = sortoptions(data, 0)
            choice = inputchecker(len(distinct))
            typeindex = 0
        case 2:
            distinct = sortoptions(data, 1)
            choice = inputchecker(len(distinct))
            typeindex = 1
        case 3:
            distinct = sortoptions(data, 2)
            choice = inputchecker(len(distinct))
    try:
        sorter(data, choice, distinct, typeindex)
    except:
        sorter(data, choice, distinct)

def createcharacters(data):
    while True:
        charactername = input("\nWhat is the name of this character? ")
        if charactername not in data.keys():
            break
    characterrace = input("What is the race of this character? ")
    availableclasses = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard", "Artificer"]
    class_stat_increases = {"Barbarian": {"strength": 2, "constitution": 1}, "Bard": {"charisma": 2, "dexterity": 1}, "Cleric": {"wisdom": 2, "charisma": 1}, "Druid": {"wisdom": 2, "constitution": 1}, "Fighter": {"strength": 2, "constitution": 1}, "Monk": {"dexterity": 2, "wisdom": 1}, "Paladin": {"strength": 2, "charisma": 1}, "Ranger": {"dexterity": 2, "wisdom": 1}, "Rogue": {"dexterity": 2, "intelligence": 1}, "Sorcerer": {"charisma": 2, "constitution": 1}, "Warlock": {"charisma": 2, "wisdom": 1}, "Wizard": {"intelligence": 2, "wisdom": 1}, "Artificer": {"intelligence": 2, "constitution": 1}}
    characterclass = input("What is the class of this character? ").lower().capitalize().strip()
    def increasestatsbyclass():
        if characterclass in class_stat_increases:
            increases = class_stat_increases[characterclass]
            print(f"As a {characterclass}, you get the following stat increases:")
            for stat, increase in increases.items():
                print(f"- {stat.title()}: +{increase}")
            return increases
        else:
            print(f"No stat increases found for class: {characterclass}")
            return {}
    while characterclass not in availableclasses:
        print("Please enter a valid class.")
        for i in availableclasses:
            print(f"- {i}")
        characterclass = input("What is the class of this character? ").strip().lower().capitalize()
    applied_increases = increasestatsbyclass()
    while True:
        characterlevel = input("What is the level of the character? ")
        if not validate_input(characterlevel, 'int'):
            print("Please enter a valid integer number.")
            continue
        break
    attributeslist = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "health", "armor class"]
    attributesscores = []
    for attribute in attributeslist:
        while True:
            attributepoint = input(f"What is the {attribute} score of this character? ")
            if validate_input(attributepoint, 'int'):
                attributesscores.append(int(attributepoint))
                break
            else:
                print("Please enter a valid integer value.")
    if applied_increases:
        for stat, inc in applied_increases.items():
            if stat.lower() in attributeslist:
                index = attributeslist.index(stat.lower())
                attributesscores[index] += inc
    data[charactername] = {
        "simpleinfo": (characterrace, characterclass),
        "level": int(characterlevel),
        "Items_Dictionary": {"Weapon": ["None", "Weapon", "None"], "Armor": ["None", "Armor", "None"], "Inventory": []},
        "skills": set(),
        "attributes": [attributeslist, attributesscores]
    }
    print(f"\n{charactername} has been created!")

def visualization_menu(database):
    character_names = list(database.keys())
    print(f"\nCharacter Visualization - Total characters: {len(database)}")
    print("A. Individual Character Radar Chart\nB. Multi-Character Stat Comparison\nC. Class Distribution Analysis\nD. Attribute Trends Over Time\nE. Character Level Progression\nM. Main Menu")
    choice = letter_input(["a", "b", "c", "d", "e", "m"])
    if choice == "m":
        return
    visualization = DataVisualization()
    if choice == "a" or choice == "d":
        for index, name in enumerate(character_names, 1):
            print(f"{index}. {name}")
        selected_name = character_names[inputchecker(len(character_names)) - 1]
        if choice == "a":
            visualization.radar_chart(selected_name, database[selected_name])
        else:
            visualization.bar_chart(selected_name, database[selected_name])
    elif choice == "b":
        visualization.comparison_bar(database)
    elif choice == "c":
        visualization.class_distribution(database)
    elif choice == "e":
        visualization.level_progression(database)

def analysis_menu(database):
    analyzer = StatisticalAnalyzer(database)
    print("\nStatistical Analysis\n1. Full stat report\n2. Top characters by stat\n3. Filter by class\n4. Filter by race\n5. Back")
    choice = inputchecker(5)
    if choice == 1:
        analyzer.print_report()
    elif choice == 2:
        analyzer.top_by_stat(input("Which stat? (example: strength): ").strip().lower())
    elif choice == 3:
        analyzer.filter_by_class(input("Enter class: ").strip())
    elif choice == 4:
        analyzer.filter_by_race(input("Enter race: ").strip())

def portfolio_dashboard(database):
    analyzer = StatisticalAnalyzer(database)
    print(f"\nCharacter Portfolio Dashboard - Total characters: {len(database)}")
    print("\nRoster:")
    for name, data in database.items():
        print(f"   - {name} : {data['simpleinfo'][0]}, {data['simpleinfo'][1]}, Level {data['level']}")
    stat_columns = [c for c in analyzer.dataframe.columns if c not in ["name", "race", "class", "level"]]
    print("\nStat Summary:")
    print(analyzer.dataframe[stat_columns].agg(["mean", "median", "max", "min"]).round(2).to_string())

def comparison_tools(database):
    analyzer = StatisticalAnalyzer(database)
    visualization = DataVisualization()
    print("\nCharacter Comparison Tools\n1. Compare all characters bar chart\n2. Top 3 by stat\n3. Back")
    choice = inputchecker(3)
    if choice == 1:
        visualization.comparison_bar(database)
    elif choice == 2:
        analyzer.top_by_stat(input("Which stat? (example: strength): ").strip().lower())

def character_builder(database):
    generator = RandomGenerator()
    print("\nCharacter Builder\n1. Build manually\n2. Generate random character\n3. Back")
    choice = inputchecker(3)
    if choice == 1:
        createcharacters(database)
    elif choice == 2:
        name, character = generator.generate_character()
        database[name] = character
        print(f"\nCreated: {name} | {character['simpleinfo'][0]} {character['simpleinfo'][1]} Level {character['level']}")
        print(f"Backstory: {character['backstory']}")

def random_gen_menu(database):
    generator = RandomGenerator()
    print("\nRandom Generator\n1. Generate random character\n2. Generate random quest\n3. Back")
    choice = inputchecker(3)
    if choice == 1:
        name, character = generator.generate_character()
        database[name] = character
        print(f"\nCreated: {name} | {character['simpleinfo'][0]} {character['simpleinfo'][1]} Level {character['level']}")
        print(f"Backstory: {character['backstory']}")
    elif choice == 2:
        print(f"\nQuest: {generator.random_quest()}")

def save_load_menu(database):
    print("\nSave/Load Database\n1. Save to file\n2. Load from file\n3. Back")
    choice = inputchecker(3)
    if choice == 1:
        save_database(database)
    elif choice == 2:
        load_database(database)

def save_database(database):
    saveable = {}
    for name, data in database.items():
        saveable[name] = {
            "simpleinfo": list(data["simpleinfo"]),
            "level": data["level"],
            "Items_Dictionary": data["Items_Dictionary"],
            "skills": list(data["skills"]),
            "attributes": data["attributes"]
        }
    with open("database.json", "w") as file:
        json.dump(saveable, file)
    print("Database saved to database.json")

def load_database(database):
    try:
        with open("database.json", "r") as file:
            loaded = json.load(file)
        for name, data in loaded.items():
            database[name] = {
                "simpleinfo": tuple(data["simpleinfo"]),
                "level": data["level"],
                "Items_Dictionary": data["Items_Dictionary"],
                "skills": set(tuple(skill) for skill in data["skills"]),
                "attributes": data["attributes"]
            }
        print("Database loaded from database.json")
    except FileNotFoundError:
        print("No save file found.")

def export_data(database):
    StatisticalAnalyzer(database).export_csv()

def import_characters(database):
    try:
        dataframe = pd.read_csv("characters.csv")
        print("\nImported characters from characters.csv:")
        print(dataframe[["name", "race", "class", "level"]].to_string(index=False))
    except FileNotFoundError:
        print("No characters.csv file found.")

if __name__ == "__main__":
    print("Hello! This is a simple character management software")
    from main import database
    mainmenu(database)