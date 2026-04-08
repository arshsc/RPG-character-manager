def validate_input(text, kind='int'):
    test_to_check = str(text).strip().capitalize()
    if kind == 'int':
        try:
            int(test_to_check)
            return True
        except ValueError:
            return False
    elif kind == 'float':
        try:
            float(test_to_check)
            return True
        except ValueError:
            return False
    elif kind == 'alpha':
        return test_to_check.isalpha()
    else:
        return False
def editcharacters(database):
    print("\nWhich character would you like to edit? ")
    count = 0
    for i, character in enumerate(database.keys()):
        count += 1
        print(f"{i+1}. {character}")
    choice = input("\nEnter the number of the character you want to edit, or type q to return to the main menu: ").strip()
    if not validate_input(choice, 'int'):
        return
    choice = int(choice)   
    if choice < 1 or choice > count:
        print("Invalid choice.")
        return
    choice -= 1
    character_name = list(database.keys())[choice]
    while True:
        print(f"\nEditing {character_name}")
        print("1. Edit Skills")
        print("2. Edit Inventory")
        print ("3. Edit Stats")
        print("4. Return to Main Menu")
        action = input("\nChoose an option: ").strip()
        if action == "1":
            EditSkills(database, character_name)
        elif action == "2":
            inventory_management(database, character_name, database[character_name]["simpleinfo"][1])
        elif action == "3":
            editing(database, character_name)
        elif action == "4":
            break
        else:
            print("Invalid option.")

def EditSkills(database, character_name):
        action = input("\nWould you like to: \n- Add\n- Remove\n\nWhich one would you like to choose? ").lower().strip()
        if action == "add":
            skillname = input("\nEnter the name of the skill you want to add: ").capitalize().strip()
            skilldesc = input("Enter a description for the skill: ").strip()
            database[character_name]["skills"].add((skillname, skilldesc))
            print(f"Skill '{skillname}' has been added.")
                
        elif action == "remove":
            print("\nSkills:")
            for i in database[character_name]["skills"]:
                print(f"   - {i[0]}")
            skillToRemove = input("\nEnter the name of the skill you want to remove: ").capitalize().strip()
            skill_to_remove = next((skill for skill in database[character_name]["skills"] if skill[0] == skillToRemove), None)
            if skill_to_remove:
                database[character_name]["skills"].remove(skill_to_remove)
                print(f"\nSkill '{skillToRemove}' has been removed.")
            else:
                print(f"\nSkill '{skillToRemove}' not found in your skills.")


def inventory_management(database, character_name, player_class):
    Items_Dictonaties = database[character_name]["Items_Dictionary"]
    print(f"\nCharacters Weapon: {Items_Dictonaties["Weapon"][0]}")
    print(f"Character Wearing: {Items_Dictonaties["Armor"][0]} ")
    print(f"\nCharacter Inventory:")
    val = 0
    for x in Items_Dictonaties["Inventory"]:
        val += 1
        if val == 1:
            print(x)
        if val == 3:
            val = 0
    Player_answer = input("\nWould you like to: \n1. Yes\n2. No\n\nWhich one would you like to choose (1 - 2)? ").capitalize().strip()
    if Player_answer == "1" or Player_answer == "Yes":
        asking = True
        while asking:
            players_selected_action = input("Would you like to (1.edit your inventory 2.Add a item to your inventory 3.To exit):").capitalize().strip()
            if players_selected_action == "1":
                answering = True
                while answering:
                    for x in Items_Dictonaties["Inventory"]:
                        val += 1
                        if val == 1:
                            print(x)
                        if val == 3:
                            val = 0
                    Edit_item = input("What item in your inventory do you want to edit:").capitalize().strip()
                    if Edit_item in Items_Dictonaties["Inventory"]:
                        Item_index = Items_Dictonaties["Inventory"].index(Edit_item)
                        Item_slot = Items_Dictonaties["Inventory"][Item_index + 1]
                        Item_class = Items_Dictonaties["Inventory"][Item_index + 2]
                        if Item_class == player_class or Item_class == "None":
                            for x in range(0,3):
                                    Items_Dictonaties["Inventory"].pop(Item_index) 
                            for x in range(0,3):
                                if Items_Dictonaties[Item_slot][0] != "None":
                                    Items_Dictonaties["Inventory"].append(Items_Dictonaties[Item_slot][x]) 
                            Items_Dictonaties[Item_slot] = [Edit_item,Item_slot,Item_class]
                            print(f"Your characters weapon is a {Items_Dictonaties["Weapon"][0]}")
                            print(f"Your characters is wearing {Items_Dictonaties["Armor"][0]} ")
                            print(f"This is your inventory:")
                            val = 0
                            for x in Items_Dictonaties["Inventory"]:
                                val += 1
                                if val == 1:
                                    print(f"- {x}")
                                if val == 3:
                                    val = 0
                            answering = False
                        else:
                            print(f"Your character class is incorect. you need to be a {Item_class}, but you are a {player_class}")
                    else:
                        print("that is not an item in your inventory")
            if players_selected_action == "2":
                player_item_name = input("What is the name of the item:").capitalize().strip()
                Items_Dictonaties["Inventory"].append(player_item_name)
                player_item_slot = input("What is the slot of the item(1.Inventory,2.Weapon,3.Armor):").capitalize().strip()
                if player_item_slot == "1":
                    player_item_slot = "Inventory"
                if player_item_slot == "2":
                    player_item_slot = "Weapon"
                if player_item_slot == "3":
                    player_item_slot = "Armor"
                Items_Dictonaties["Inventory"].append(player_item_slot)
                player_item_class = input("What is the required class of the item(If no required one then type None):").capitalize().strip()
                if player_item_class not in ["None","Warrior","Fighter","Rogue","Cleric","Sorcerer","Mage","Wizard","Paladin","Ranger","Druid","Bard","Monk","Barbarian"]:
                    print("That is not a valid class.")
                if player_item_class == "None":
                    player_item_class = "Any"
                Items_Dictonaties["Inventory"].append(player_item_class)
                for x in Items_Dictonaties["Inventory"]:
                        val += 1
                        if val == 1:
                            print(x)
                        if val == 3:
                            val = 0
            if players_selected_action == "3":
                asking = False


def editing(database, character_name):

    def displaystat(num, stat_name):
        oldstat = database[character_name]["attributes"][1][num]
        try:
            database[character_name]["attributes"][1][num] = int(newStatValue)
        except ValueError:
            database[character_name]["attributes"][1][num] = newStatValue
        print(f"\n{stat_name.capitalize()} has been updated from {oldstat} to {database[character_name]['attributes'][1][num]}")

    while True:
        changableStats = database[character_name]["attributes"][0]
        print("\nAttributes: ")
        ii = 1
        for x in changableStats:
            print (f"{ii}. {x.title()}")
            ii += 1
        statToEdit = input("\nWhich attribute would you like to edit? ").lower().strip()
        stat_is_valid = statToEdit in changableStats or statToEdit in [s[:3] for s in changableStats] or statToEdit in ["ac", "hel"]
        try:
            stat_num = int(statToEdit)
            stat_is_valid = stat_is_valid or (1 <= stat_num <= len(changableStats))
        except ValueError:
            pass

        
        if stat_is_valid:
            # Map input to actual stat name. dont get confused team
            stat_name_map = {
                "strength": "strength", "str": "strength", "1": "strength",
                "dexterity": "dexterity", "dex": "dexterity", "2": "dexterity",
                "intelligence": "intelligence", "int": "intelligence", "3": "intelligence",
                "wisdom": "wisdom", "wis": "wisdom", "4": "wisdom",
                "constitution": "constitution", "con": "constitution", "5": "constitution",
                "charisma": "charisma", "cha": "charisma", "8": "charisma",
                "health": "health", "hel": "health", "6": "health",
                "armor class": "armor class", "ac": "armor class", "7": "armor class"
            }
            actual_stat_name = stat_name_map.get(statToEdit, statToEdit)
            while True:
                newStatValue = input(f"What would you like to change {actual_stat_name} to? ").strip()
                if not validate_input(newStatValue, 'int'):
                    print("Please enter a numeric value.")
                    continue
                break

                    
            match statToEdit:
                case "strength" | "str" | "1":
                        displaystat(0, "strength")
                case "dexterity" | "dex" | "2":
                        displaystat(1, "dexterity")
                case "intelligence" | "int" | "3":
                        displaystat(2, "intelligence")
                case "wisdom" | "wis" | "4":
                        displaystat(3, "wisdom")
                case "constitution" | "con" | "5":
                        displaystat(4, "constitution")
                case "charisma" | "cha" | "8":
                        displaystat(5, "charisma")
                case "health" | "hel" | "6":
                        displaystat(6, "health")
                case "armor class" | "ac" | "7":
                        displaystat(7, "armor class")
                case _:
                        print("Could not match stat. Please try again.")
            continue_editing = input("\nWould you like to update another attribute: \n- Yes\n- No\n\nWhich one would you like to choose? ").lower().strip()
            if continue_editing != "yes":
                break

        else:
                print("Invalid stat name. Please try again.")
