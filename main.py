import os
from os import listdir
from os.path import isfile, join

menu_spaces = 5
curr_set = ""
cards = {}
kv_seperator = "###"
sets_path = "sets"
card_width = 20   # TODO: make variable based on longest combined KV length. Also cap kv length.


def set_menu():
    if curr_set == "":
        select_set()
        return

    choice = input("1] Add card" + " " * menu_spaces + "2] View cards" + " " * menu_spaces + "3] Study set" +
                   " " * menu_spaces + "4] Home\n")
    if choice == "1":
        add_card()
    elif choice == "2":
        view_cards()
    elif choice == "3":
        study_set()
    elif choice == "4":
        home_menu()
    else:
        print("Invalid choice, please enter a number 1-4.")
        set_menu()


def create_set():
    global curr_set
    set_name = input("Set name: ")  # TODO: sanitize name - only valid file name chars
    set_name = set_name.strip()
    f = open(sets_path + "/" + set_name + ".txt", "w")  # create file
    f.close()

    print("Set '" + set_name + "' created.")
    curr_set = set_name
    set_menu()
    return


def get_card_border() -> str:
    return "-" * card_width


def get_formatted_card(text: str) -> str:
    return get_card_border() + "\n\n" + text + "\n\n" + get_card_border()


def view_cards():
    for k, v in cards.items():
        print(get_formatted_card(k + ": " + v))
    return


def add_card():
    k = input("Term: ")  # TODO: strip delimiter from both
    v = input("Definition: ")
    f = open(sets_path + "/" + curr_set + ".txt", "a")
    f.write(k + kv_seperator + v + "\n")
    cards[k] = v
    return


def study_set():
    while True:
        for k, v in cards.items():
            showing_key = True
            print(get_formatted_card(k))
            while True:
                choice = input("1] Flip" + " " * menu_spaces + "2] Next" + " " * menu_spaces + "3] Back\n")
                if choice == "1":
                    showing_key = not showing_key
                    display = v
                    if showing_key:
                        display = k
                    print(get_formatted_card(display))
                elif choice == "2":
                    break
                elif choice == "3":
                    set_menu()
                    return
                else:
                    print("Invalid selection, please enter a number 1-3")


def quiz():
    # TODO
    # 1] multiple choice
    # 2] self-graded
    # 3] matching
    # 4] text entry
    return


def select_set():
    global curr_set

    set_files = [f for f in listdir(sets_path) if isfile(join(sets_path, f))]
    if len(set_files) == 0:
        print("No sets found. Please create one.")
        home_menu()
        return

    for i in range(len(set_files)):
        split = set_files[i].split(".")
        print(str(i+1) + "] " + split[0])

    choice_str = input("\n")
    try:
        choice = int(choice_str)
    except ValueError:
        print("Invalid selection. Please enter a number 1-" + str(len(set_files)) + ".")
        select_set()
        return

    split = set_files[choice-1].split(".")
    curr_set = split[0]
    populate_cards()


def populate_cards():
    f = open(sets_path + "/" + curr_set + ".txt", "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        split = line.split(kv_seperator)
        cards[split[0]] = split[1]


def home_menu():
    choice = input("1] Create set" + " " * menu_spaces + "2] Existing set" + " " * menu_spaces + "3] Quit\n")
    choice = choice.strip()
    if choice == "1":
        create_set()
    elif choice == "2":
        select_set()
    elif choice == "3":
        exit()
    else:
        print("Invalid choice, please enter a number 1-3")
        home_menu()


def init_sets_to_cards():
    # TODO
    return


def main():
    try:
        if not os.path.exists(sets_path):
            os.mkdir(sets_path)
        init_sets_to_cards()
        home_menu()
        while True:
            set_menu()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
