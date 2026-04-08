# import needed libraries
import sys, random, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from faker import Faker
from upgrade_rpg_character_manager.Editing_function import editcharacters

# setup faker
fake = Faker()

# csv path
csv_path = os.path.join("upgrade_rpg_character_manager", "documents", "characters.csv")

# class random generator for random character generation and quests
class RandomGenerator:
    # possible options for random generation
    races = ["Human", "Elf", "Dwarf", "Gnome", "Halfling", "Dragonborn", "Tiefling", "Half-Orc"]
    classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", 
               "Rogue", "Sorcerer", "Warlock", "Wizard"]
    quests = ["Do a quest", "Help someone with something", "Go to a place and fix a problem","Fight a thing", "Find an item", "Talk to an NPC", "Clear out enemies in area","Investigate something weird", "Escort someone somewhere", "Stop something bad from happening"]
    traits = ["kind of brave", "a little shady", "hard to read"]
    motivations = ["seeking revenge for their fallen family.", "searching for a legendary lost artifact.","trying to repay an old debt to a powerful figure.", "running from a dark past they can't escape.","driven by an unquenchable thirst for knowledge.", "hoping to earn enough gold to retire peacefully.","fulfilling a prophecy they never asked to be part of.", "proving themselves worthy of their mentor's legacy."]

    # generate a random character with name
    def generate_character(self):
        name = fake.name()
        race = random.choice(self.races)
        character_class = random.choice(self.classes)
        level = random.randint(1, 20)
        attribute_names = ["strength", "dexterity", "intelligence", "wisdom", "constitution", "health", "armor class", "charisma"]
        attribute_scores = [random.randint(8, 18) for _ in attribute_names]
        trait = random.choice(self.traits)
        motivation = random.choice(self.motivations)
        backstory = (f"{name} is a {trait} {race} {character_class} from {fake.city()}.\nBefore adventuring, they worked as a {fake.job()}.\nNow they travel the world, {motivation}")
        character = {
            "simpleinfo": (race, character_class),
            "level": level,
            "Items_Dictionary": {
                "Weapon": ["None", "Weapon", "None"],
                "Armor": ["None", "Armor", "None"],
                "Inventory": []
            },
            "skills": set(),
            "attributes": [attribute_names, attribute_scores],
            "backstory": backstory
        }
        return name, character

    # generate a random quest
    def random_quest(self):
        return random.choice(self.quests)

# class for statistical analysis of characters using pandas
class StatisticalAnalyzer: 
    # initialize with character data and create dataframe
    def __init__(self, database):
        rows = []
        for name, data in database.items():
            row = {
                "name": name,
                "race": data["simpleinfo"][0],
                "class": data["simpleinfo"][1],
                "level": data["level"]
            }
            for attribute, value in zip(data["attributes"][0], data["attributes"][1]):
                row[attribute] = value
            rows.append(row)
        self.dataframe = pd.DataFrame(rows)

    # print character list and stats summary
    def print_report(self):
        print("\nYour Characters")
        print(self.dataframe[["name", "race", "class", "level"]].to_string(index=False))
        stat_columns = [c for c in self.dataframe.columns if c not in ["name", "race", "class", "level"]]
        print("\n--- Stat Summary (mean, median, max, min) ---")
        print(self.dataframe[stat_columns].agg(["mean", "median", "max", "min"]).round(2).to_string())

    # top 3 characters by a specific stat
    def top_by_stat(self, stat):
        if stat not in self.dataframe.columns:
            print(f"\n'{stat}' isn't a valid stat.")
            return
        print(f"\nTop 3 Characters by {stat.title()} ---")
        print(self.dataframe[["name", stat]].sort_values(stat, ascending=False).head(3).to_string(index=False))

    # filter characters by class or race
    def filter_by_class(self, character_class):
        results = self.dataframe[self.dataframe["class"].str.lower() == character_class.lower()]
        if results.empty:
            print(f"\nNo characters found with the class '{character_class}'.")
        else:
            print(results.to_string(index=False))

    def filter_by_race(self, race):
        results = self.dataframe[self.dataframe["race"].str.lower() == race.lower()]
        if results.empty:
            print(f"\nNo characters found with the race '{race}'.")
        else:
            print(results.to_string(index=False))

# class for data visualization of characters using matplotlib
class DataVisualization:
    # bar chart for attributes
    def bar_chart(self, name, data):
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(data["attributes"][0], data["attributes"][1], color="steelblue", edgecolor="black")
        ax.bar_label(bars, padding=3)
        ax.set_title(f"{name}'s Attribute Scores")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 25)
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join("documents", f"{name}_bar.png"))
        print(f"Chart saved: '{name}_bar.png'")
        plt.close()

    # radar chart for attributes
    def radar_chart(self, name, data):
        labels = data["attributes"][0]
        values = data["attributes"][1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values_closed = values + [values[0]]
        angles_closed = angles + [angles[0]]
        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
        ax.plot(angles_closed, values_closed, "o-", linewidth=2)
        ax.fill(angles_closed, values_closed, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles), labels)
        ax.set_title(f"{name}'s Radar Chart", pad=15)
        ax.set_ylim(0, 20)
        plt.tight_layout()
        plt.savefig(os.path.join("documents", f"{name}_radar.png"))
        print(f"Chart saved: '{name}_radar.png'")
        plt.close()

# load from csv
def load_from_csv(database):
    if not os.path.exists(csv_path):
        print(f"No CSV file found at '{csv_path}'.")
        return
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        attributes = [[], []]
        for col in df.columns:
            if col not in ["name", "race", "class", "level"]:
                attributes[0].append(col)
                attributes[1].append(int(row[col]))
        database[row["name"]] = {
            "simpleinfo": (row["race"], row["class"]),
            "level": int(row["level"]),
            "Items_Dictionary": {"Weapon":["None","Weapon","None"],
                                 "Armor":["None","Armor","None"],
                                 "Inventory":[]},
            "skills": set(),
            "attributes": attributes
        }
    print(f"Loaded {len(database)} character(s) from CSV")

# import chartacters from csv (with duplicate name check) and add to database
def import_characters(database):
    if not os.path.exists(csv_path):
        print(f"No CSV file found at '{csv_path}'.")
        return
    df = pd.read_csv(csv_path)
    stat_columns = [c for c in df.columns if c not in ["name", "race", "class", "level"]]
    imported, skipped = 0, 0
    for _, row in df.iterrows():
        name = row["name"]
        if name in database:
            skipped += 1
            continue
        attributes_names = []
        attributes_scores = []
        for stat in stat_columns:
            if stat in row and pd.notna(row[stat]):
                attributes_names.append(stat)
                attributes_scores.append(int(row[stat]))
        database[name] = {
            "simpleinfo": (str(row["race"]), str(row["class"])),
            "level": int(row["level"]),
            "Items_Dictionary": {"Weapon":["None","Weapon","None"],
                                 "Armor":["None","Armor","None"],
                                 "Inventory":[]},
            "skills": set(),
            "attributes": [attributes_names, attributes_scores]
        }
        imported += 1
    print(f"Imported {imported} character(s), skipped {skipped} already existing.")

# characters database
characters_database = {}

# load from csv call
load_from_csv(characters_database)