# import needed libraries
from upgrade_rpg_character_manager.Editing_function import *
import random
import sys
from upgrade_rpg_character_manager.helper import (viewchars, createcharacters, visualization_menu, analysis_menu, random_gen_menu, portfolio_dashboard, comparison_tools, character_builder, save_load_menu, export_data, import_characters)
from arsh import intro

# database
database = {
    "Zarkon":{"simpleinfo":("Dragonborn", "Fighter"), "level": 8, "Items_Dictionary": {"Weapon": ["Shortsword", "Weapon", "any"], "Armor": ["any", "Armor", "any"], "Inventory": []}, "skills":{("Fireball","A bright streak flashes from the caster to a point within 150 feet, erupting into a 20-foot-radius sphere of fire!")}, "attributes": [["strength", "dexterity", "intelligence", "wisdom", "constitution", "health", "armor class", "charisma"], [random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 15), random.randint(10, 17), random.randint(8, 18)]]},
    "Gulnum":{"simpleinfo":("Gnome", "Sorcerer"), "level": 4, "Items_Dictionary": {"Weapon": ["Mace", "Weapon", "None"], "Armor": ["None", "Armor", "None"], "Inventory": []}, "skills":{("Magic missile","A missile of magical force springs from the caster's finger to strike a target within 120 feet")}, "attributes": [["strength", "dexterity", "intelligence", "wisdom", "constitution", "health", "armor class", "charisma"], [random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 15), random.randint(10, 17), random.randint(8, 18)]]},
    "Zylvina":{"simpleinfo":("Elf", "Cleric"), "level": 13,"Items_Dictionary": {"Weapon": ["Whip", "Weapon", "None"], "Armor": ["None", "Armor", "None"], "Inventory": []}, "skills":{("Heal","The character can heal wounds and restore health")}, "attributes": [["strength", "dexterity", "intelligence", "wisdom", "constitution", "health", "armor class", "charisma"], [random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 18), random.randint(8, 15), random.randint(10, 17), random.randint(8, 18)]]},
}

# main menu
def mainmenu(database):
    while True:
        print("\nMain Menu:")
        print("1. Character Visualization")
        print("2. Statistical Analysis")
        print("3. Character Portfolio Dashboard")
        print("4. Character Comparison Tools")
        print("5. Create Character")
        print("6. Character Management")
        print("7. Character Builder")
        print("8. Random Generator")
        print("9. Save/Load Database")
        print("10. Export Character Data")
        print("11. Import Characters")
        print("Q. Quit")
        choice = input("\nEnter your choice: ").strip().lower()
        if choice == "1":
            visualization_menu(database)
        elif choice == "2":
            analysis_menu(database)
        elif choice == "3":
            portfolio_dashboard(database)
        elif choice == "4":
            comparison_tools(database)
        elif choice == "5":
            createcharacters(database)
        elif choice == "6":
            viewchars(database)
        elif choice == "7":
            character_builder(database)
        elif choice == "8":
            random_gen_menu(database)
        elif choice == "9":
            save_load_menu(database)
        elif choice == "10":
            export_data(database)
        elif choice == "11":
            import_characters(database)
        elif choice == "q":
            print("\nExiting...")
            sys.exit()
        else:
            print("Invalid choice.")

# run the program
if __name__ == "__main__":
    intro()
    mainmenu(database)