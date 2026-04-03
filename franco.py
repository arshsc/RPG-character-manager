# FB 1st Character manager
import sys
import pandas
import matplotlib

from Editing_function import editcharacters

class DataVisualization:
    pass

class Statisticalanalyzer:
    pass

class RandomGenerator:
    pass



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
                if choicevar in range(1, rangeofchoices+1):
                    break
                else:
                    print("That's not an option :(")
                    continue
            except:
                print("Please enter a valid integer number.")
                continue
            
    return choicevar

def viewchars(data):
    characterkeys = data.keys()
    characternameandlistnum = {}

    count = 1
    for character in characterkeys:
        characternameandlistnum[count] = character
        char_race = data[character]["simpleinfo"][0]
        char_class = data[character]["simpleinfo"][1]
        char_level = data[character]["level"]
        print(f"{count}. {character} : {char_race}, {char_class}, {char_level}")
        count += 1
        

    print("\nWould you like to:\n1. Select\n2. Sort\n3. Main Menu")

    choice = inputchecker(3)
    
    match choice:
        case 1:
            select(data,characternameandlistnum)
        case 2:
            sortchoice(data)
        case 3:
            mainmenu(data)

def select(data, selectionmenu):
    print("\nCharacters:")
    for num, character in selectionmenu.items():
        char_race = data[character]["simpleinfo"][0]
        char_class = data[character]["simpleinfo"][1]
        char_level = data[character]["level"]
        print(f"{num}. {character} : {char_race}, {char_class}, {char_level}")
    
    print("\nWhich character do you want to select? (Refer to the list of characters above)")

    characternum = inputchecker(len(selectionmenu))
    character = selectionmenu[characternum]

    char_race = data[character]["simpleinfo"][0]
    char_class = data[character]["simpleinfo"][1]
    char_level = data[character]["level"]
    print(f"{character} : {char_race}, {char_class}, {char_level}")

    print("\nInventory: ")
    for itemslot in data[character]["Items_Dictionary"].keys():
        item = data[character]["Items_Dictionary"][itemslot]

        try:
            print(f"   - {itemslot}: {item[0]} it is a {item[1]}, and {item[2]} can use it!")
        except:
            continue

    for skill in data[character]["skills"]:
        print(f"\nSkills:\n   - {skill[0]}: {skill[1]}")
    
    count = 0
    print("\nAttributes: ")
    for attribute in data[character]["attributes"][0]:
        attr_value = data[character]["attributes"][1][count]
        print(f"   - {attribute.title()}: {attr_value}")
        count += 1

    print("\nWould you like to:\n1. Edit\n2. Main Menu?")

    answer = inputchecker(2)

    match answer:
        case 1:
            editcharacters(data)
        case 2:
            mainmenu(data)

def sortoptions(data, *typeindex):
    characternames = data.keys()
    previoustypes = []
    typelist = {}

    count = 1
    for character in characternames:

        if data[character]["simpleinfo"][typeindex] not in previoustypes: 
            previoustypes.append(data[character]["simpleinfo"][typeindex])
            print(f"{count}. {data[character]['simpleinfo'][typeindex]}")
            typelist[count] = data[character]["simpleinfo"][typeindex]
            count += 1

    return typelist

def sorter(data, choice, types, *typeindex):
    characterkeys = data.keys()
    characternameandlistnum = {}

    count = 1
    print("\n")
    for character in characterkeys:
        if data[character]["simpleinfo"][typeindex] == types[choice]:
            characternameandlistnum[count] = character

            print(f"{count}. {character} : {data[character]["simpleinfo"][0]}, {data[character]["simpleinfo"][1]}, {data[character]["level"]}")
            count += 1

    print("\nWould you like to:\n1. Select\n2. Main menu")

    choice = inputchecker(2)

    match choice:
        case 1:
            select(data, characternameandlistnum)

def sortchoice(data):
    print("\nWill sort by:\n1. Race\n2. Class\n3. Level")

    sortchoice = inputchecker(3)

    match sortchoice:
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
    #list of dnd classes
    availableclasses = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard", "Artificer"]
    class_stat_increases = {"Barbarian": {"strength": 2, "constitution": 1}, "bard": {"charisma": 2, "dexterity": 1}, "cleric": {"wisdom": 2, "charisma": 1}, "druid": {"wisdom": 2, "constitution": 1}, "fighter": {"strength": 2, "constitution": 1}, "monk": {"dexterity": 2, "wisdom": 1}, "paladin": {"strength": 2, "charisma": 1}, "ranger": {"dexterity": 2, "wisdom": 1}, "rogue": {"dexterity": 2, "intelligence": 1}, "sorcerer": {"charisma": 2, "constitution": 1}, "warlock": {"charisma": 2, "wisdom": 1}, "wizard": {"intelligence": 2, "wisdom": 1}, "artificer": {"intelligence": 2, "constitution": 1}}
    characterclass = input("What is the class of this character? ").lower().capitalize().strip()
    def increasestatsbyclass():
        class_lower = characterclass.lower()
        normalized = {k.lower(): v for k, v in class_stat_increases.items()}
        if class_lower in normalized:
            increases = normalized[class_lower]
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
        characterlevel = input("What is the level of the characters? ")

        if not validate_input(characterlevel, 'int'):
            print("\nPlease enter a valid integer number.")
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
                continue
    
    # Apply class-based increases
    if applied_increases:
        for stat, inc in applied_increases.items():
            stat_lower = stat.lower()
            if stat_lower in attributeslist:
                idx = attributeslist.index(stat_lower)
                attributesscores[idx] += inc
    specificdata = {charactername:{
        "simpleinfo":(characterrace, characterclass),
        "level": int(characterlevel),
        "Items_Dictionary": {"Weapon": ["None", "Weapon", "None"], "Armor": ["None", "Armor", "None"], "Inventory": []},
        "skills": set(),
        "attributes": [attributeslist, attributesscores]
    }}

    data.update(specificdata)
    mainmenu(data)
    
def mainmenu(database):
    while True:
        print("\nYou may:\n1. View Characters\n2. Create Character\n3. Edit Characters\n4. Exit")
        functionchoice = inputchecker(4)
        if functionchoice == 1:
            print("\n")
            viewchars(database)
        elif functionchoice == 2:
            createcharacters(database)
        elif functionchoice == 3:
            editcharacters(database)
        else:
            print("\nExiting...")
            sys.exit()


if __name__ == "__main__":
    print("Hello! This is a simple character management software")
    from main import database
    mainmenu(database)
