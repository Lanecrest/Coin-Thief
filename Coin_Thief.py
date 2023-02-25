# Import the needed libraries and set the title
import msvcrt, os, sys, random, configparser, winsound
os.system("title Coin Thief")

# Create or load the high score config file
config_file = 'high_score.ini'
config = configparser.ConfigParser()
if os.path.exists(config_file):
    try:     
        config.read(config_file)
    except (configparser.Error, ValueError) as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)
else:
    config.add_section('Score')
    config.set('Score', 'Easy_Small', '0')
    config.set('Score', 'Easy_Medium', '0')
    config.set('Score', 'Easy_Large', '0')
    config.set('Score', 'Normal_Small', '0')
    config.set('Score', 'Normal_Medium', '0')
    config.set('Score', 'Normal_Large', '0')
    config.set('Score', 'Hard_Small', '0')
    config.set('Score', 'Hard_Medium', '0')
    config.set('Score', 'Hard_Large', '0')
    config.set('Score', 'Endless_Endless', '0')
    with open('high_score.ini', 'w') as f:
        config.write(f)
    
# Define the play_sound function
notes = {'C': 262, 'D': 294, 'E': 330, 'F': 349, 'G': 392, 'A': 440, 'B': 494}
theme = ['A', 'D', 'A', 'D', 'G', 'F', 'E']
win = ['B', 'A', 'G']
lose = ['E', 'G']
def play_sound(sound):
    if sound == theme:
        for note in theme:
            frequency = notes[note]
            duration = 100  # In milliseconds
            winsound.Beep(frequency, duration)
    if sound == win:
        for note in win:
            frequency = notes[note]
            duration = 100  # In milliseconds
            winsound.Beep(frequency, duration)
    if sound == lose:
        for note in lose:
            frequency = notes[note]
            duration = 100  # In milliseconds
            winsound.Beep(frequency, duration)
    """
    This uses winsound to to play a series of notes in the theme dictionary.
    The different themes are stored in the variables and called in the for loops. The function calls the sound effect.
    """
        
# Set values for the in-game characters
THIEF_CHAR = "\033[32m@\033[0m"    # Thief symbol in green
GUARD_CHAR = "\033[31m&\033[0m" # Guard symbol in red
STAIR_CHAR = "\033[36m%\033[0m"  # Stairs symbol in cyan
COIN_CHAR = "\033[33m*\033[0m"  # Coin symbol in yellow
CRATE_CHAR = "\033[35m#\033[0m"  # Crate symbol in magenta
WALL_CHAR = "\033[90m+\033[0m" # Wall symbol in grey
EMPTY_CHAR = " " # Empty space symbol (it's empty)

# Show the instructions and credits
print("   ___ \033[33m___\033[0m ___ _  _\n"
    "  / __\033[33m/ _ \\\033[0m_ _| \| |\n"
    " | (_\033[33m| (_) |\033[0m || .` |\n"
    "  \___\033[33m\___/\033[0m___|_|\_| ___     v1.41 \u00A9 2023 Lanecrest Tech\n"
    " |_   _| || |_ _| __| __|\n"
    "   | | | __ || || _|| _|\n"
    "   |_| |_||_|___|___|_|\n\n"
    "INSTRUCTIONS:\n"
    f"You are the {THIEF_CHAR} thief. Move with the arrow keys.\n"
    f"Collect {COIN_CHAR} coins to increase your score!\n"
    f"Move around {CRATE_CHAR} crates which block you and the guard.\n"
    f"Reach the {STAIR_CHAR} stairs to move up to the next floor.\n"
    f"Getting caught by the {GUARD_CHAR} guard ends the game!\n\n"
    f"You do not need to collect every {COIN_CHAR} on each floor.\n"
    "If you do collect every coin on a floor, you receive a bonus.\n"
    f"You must reach the {STAIR_CHAR} on the fifth floor to escape!\n"
    "Your score is only saved if you escape to the roof.\n\n"
    "You can choose the difficulty and floor sizes on the next screens.\n"
    "Your high scores are saved separately for each mode.\n")
play_sound(theme)
input("Press Enter to continue.")

# Define the difficulty mode function
def difficulty_mode():
    global GUARD_DIFFICULTY, FLOOR_SIZE
    while True:
        os.system('cls')
        print("Choose the difficulty:\n"
            "1 - Easy\n2 - Normal\n3 - Hard\n4 - Endless\n\n"
            "The difficulty determines the starting speed of the guard.\n"
            "The guard gets faster every floor.\n\n"
            "Endless Mode:\n\n"
            "Endless Mode has special rules.\n"
            "You keep moving up floors until caught at which point your score is saved.\n"
            "The guard speed is random on every floor, ranging among the fastest speeds in the other modes.\n"
            "The floor size is random on every floor, ranging among the small, medium, and large modes.\n"
            "There is no bonus score for collecting all the coins on a floor.\n")
        difficulty_prompt = input("Enter your choice: ")
        if difficulty_prompt == "1":
            GUARD_DIFFICULTY = "Easy"
            break
        elif difficulty_prompt == "2":
            GUARD_DIFFICULTY = "Normal"
            break
        elif difficulty_prompt == "3":
            GUARD_DIFFICULTY = "Hard"
            break
        elif difficulty_prompt == "4":
            GUARD_DIFFICULTY = "Endless"
            FLOOR_SIZE = "Endless"
            break
    """
    This prompts the user to select the difficulty. It stores the value as a string so it can be read in other functions.
    The functions are separated so the player only needs to enter 1, 2, or 3.
    """

# Define the floor_mode function
def floor_mode():
    global FLOOR_SIZE
    if GUARD_DIFFICULTY != "Endless":
        while True:
            os.system('cls')
            print("Choose the floor size:\n"
            "1 - Small\n2 - Medium\n3 - Large\n\n"
            "The floor size determines the width and height as well as how many coins and crates spawn.\n"
            "Each floor layout is randomly generated but all five will have the same dimensions.\n")
            size_prompt = input("Enter your choice: ")
            if size_prompt == "1":
                FLOOR_SIZE = "Small"
                break
            elif size_prompt == "2":
                FLOOR_SIZE = "Medium"
                break
            elif size_prompt == "3":
                FLOOR_SIZE = "Large"
                break
    """
    This prompts the user to select the floor size. It stores the value as a string so it can be read in other functions.
    The functions are separated so the player only needs to enter 1, 2, or 3.
    This should only prompt if the player did not select Endless difficulty.
    """

# Define the end_game function
def end_game():
    global FLOOR_NO, SCORE
    FLOOR_NO = 0
    SCORE = 0
    while True:
        print("Continue?\n"
        "1 - Restart\n2 - Change Settings\n3 - Quit\n")
        end_prompt = input("Enter your choice: ")
        if end_prompt == "1":
            game_defaults()
            break
        elif end_prompt == "2":
            difficulty_mode()
            floor_mode()
            game_defaults()
            break
        elif end_prompt == "3":
            sys.exit(0)
        else:
            os.system('cls')
    """
    This prompts the user to to restart the game with the same settings, new setting, or gives them the option to quit.
    """

# Prompt for difficulty and floor size.
difficulty_mode()
floor_mode()

# Define the set_difficulty function
def set_difficulty(difficulty):
    if difficulty == "Easy":
        return 9    # The "Speed" or frequency of movement for the guard
    elif difficulty == "Normal":
        return 8
    elif difficulty == "Hard":
        return 7
    elif difficulty == "Endless":
        return random.choice([2, 3, 4])
    """
    Pulls the strings from the difficulty_mode function and sets them as values.
    Gets called in the game_defaults function.
    """

# Define the set_size function
def set_size(size):
    if size == "Small":
        return 20, 10, 20, 10   # Width, Height, Crates, Coins
    elif size == "Medium":
        return 30, 15, 30, 15
    elif size == "Large":
        return 40, 20, 40, 20
    elif size == "Endless":
        return random.choice([
            (20, 10, 20, 10),
            (30, 15, 30, 15),
            (40, 20, 40, 20)
        ])
    """
    Pulls the strings from the floor_mode function and sets them as values.
    Gets called in the game_defaults functions.
    """

# Define the game_defaults function
def game_defaults():
    global GUARD_SPEED, FLOOR_WIDTH, FLOOR_HEIGHT, CRATE_NUM, COIN_NUM, NEW_THIEF_POS, GAME_MODE, HIGH_SCORE
    GUARD_SPEED = set_difficulty(GUARD_DIFFICULTY)
    FLOOR_WIDTH, FLOOR_HEIGHT, CRATE_NUM, COIN_NUM = set_size(FLOOR_SIZE)
    NEW_THIEF_POS = None
    GAME_MODE = GUARD_DIFFICULTY + "_" + FLOOR_SIZE
    HIGH_SCORE = int(config.get('Score', GAME_MODE))
    """
    This takes the settings defined in the difficulty and floor mode functions and pulls high score data as well as sets some other needed variables.
    This allows the game to be restarted with new settings between rounds.
    """

# Define the print_floor function
def print_floor():
    WALL = WALL_CHAR * (FLOOR_WIDTH + 2)
    level_string = WALL + "\n"
    for y in range(FLOOR_HEIGHT):
        row = ""
        for x in range(FLOOR_WIDTH):
            row += (THIEF_CHAR if (x, y) == THIEF_POS else
                GUARD_CHAR if (x, y) == GUARD_POS else
                STAIR_CHAR if (x, y) == STAIR_POS else
                COIN_CHAR if (x, y) in COIN_POS else
                CRATE_CHAR if (x, y) in CRATE_POS else
                EMPTY_CHAR)
        level_string += WALL_CHAR + row + WALL_CHAR + "\n"
    level_string += WALL
    print(level_string)
    """
    Draws the floor.
    The characters are displayed in their corresponding positions and the empty space is filled out.
    Every time the function is called it should have updated positions for everything.
    """

# Define the no_softlock function
def no_softlock(pos, walls, crates):
    x, y = pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    walls = list(walls)
    num_crates = 0
    num_walls = 0
    for adj_pos in adjacent_positions:
        if adj_pos in walls:
            num_walls += 1
        elif adj_pos in crates:
            num_crates += 1
    return num_crates > 3 or (num_crates > 1 and num_walls > 1)
    """
    This checks that the number of crates or walls will not exceed a certain threshold causing them to generate a softlock.
    """

# Define the game_hud function
def game_hud():
    if GUARD_DIFFICULTY == "Endless":
        print(f"Level: {FLOOR_NO} of \u221E\n"
              f"Coins: {SCORE}\n\n"
              f"High Score: {HIGH_SCORE}")
    else:
        print(f"Level: {FLOOR_NO} of 5\n"
            f"Coins: {SCORE}\n\n"
            f"Difficulty: {GUARD_DIFFICULTY}\n"
            f"Level Size: {FLOOR_SIZE}\n"
            f"High Score: {HIGH_SCORE}")
    """
    Draws the game hud.
    It displays basic info about the game such as level info, difficulty, and score
    """

# Start the main game loop. The first sections only run when a new floor (or game start) is loaded
FLOOR_NO = 0
SCORE = 0
game_defaults()

while True:
    os.system('cls')

    # Update the counters  or settings when a new floor loads
    if GUARD_DIFFICULTY == "Endless":
        game_defaults()
    else:
        GUARD_SPEED -= 1
    FLOOR_NO += 1
    MOVE_COUNTER = 0

    # Set the new character positions when a new floor loads
    THIEF_POS = NEW_THIEF_POS
    if NEW_THIEF_POS is None:
        THIEF_POS = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
    GUARD_POS = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
    STAIR_POS = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
    while GUARD_POS == STAIR_POS or GUARD_POS == THIEF_POS:
        GUARD_POS = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
    while STAIR_POS == GUARD_POS or STAIR_POS == THIEF_POS:
        STAIR_POS = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
    COIN_POS = []
    for _ in range(COIN_NUM):
        COIN = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
        while (COIN == THIEF_POS or COIN == GUARD_POS or COIN == STAIR_POS or COIN in COIN_POS):
            COIN = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
        COIN_POS.append(COIN)
    CRATE_POS = []
    for _ in range(CRATE_NUM):
        CRATE = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
        while (CRATE == THIEF_POS or CRATE == GUARD_POS or CRATE == STAIR_POS or CRATE in COIN_POS or CRATE in CRATE_POS or no_softlock(CRATE, WALL_CHAR, CRATE_POS)):
            CRATE = (random.randint(0, FLOOR_WIDTH - 1), random.randint(0, FLOOR_HEIGHT - 1))
        CRATE_POS.append(CRATE)

    # Sub loop that in order checks if won, next floor, lose, coin collected, thief move, guard move
    while True:

        # Check if the thief has finished the 5th floor (win). Also updates the high score for the mode if it's a new record
        if FLOOR_NO == 6 and GUARD_DIFFICULTY != "Endless":
            os.system('cls')
            if SCORE > HIGH_SCORE:
                config.set('Score', GAME_MODE, str(SCORE))
                with open('high_score.ini', 'w') as f:
                     config.write(f)
            HIGH_SCORE = int(config.get('Score', GAME_MODE))
            print(f"You escaped!\n\n"
                f"You reached the roof with {SCORE} coins.\n"
                f"Your high score is: {HIGH_SCORE}\n")
            play_sound(win)
            end_game()
            break

        # Check if the thief has reached the stairs (next floor)
        if THIEF_POS == STAIR_POS:
            if FLOOR_NO != 5:
                winsound.Beep(notes['D'], 25)
                winsound.Beep(notes['D'], 25)
            elif GUARD_DIFFICULTY == "Endless":
                winsound.Beep(notes['D'], 25)
                winsound.Beep(notes['D'], 25)
            break

        # Check if the thief has been caught by the guard (lose)
        if THIEF_POS == GUARD_POS and GUARD_DIFFICULTY != "Endless":
            os.system('cls')
            print(f"You were caught!\n\n"
                f"You were on floor {FLOOR_NO} and collected {SCORE} coins.\n"
                f"Your high score is: {HIGH_SCORE}\n")
            play_sound(lose)
            end_game()
            break
        elif THIEF_POS == GUARD_POS:   # Else statement if game is being played on Endless
            os.system('cls')
            if SCORE > HIGH_SCORE:
                config.set('Score', GAME_MODE, str(SCORE))
                with open('high_score.ini', 'w') as f:
                     config.write(f)
            HIGH_SCORE = int(config.get('Score', GAME_MODE))
            print(f"Game Over!\n\n"
                f"You were on floor {FLOOR_NO} and collected {SCORE} coins.\n"
                f"Your high score is: {HIGH_SCORE}\n")
            play_sound(win)
            end_game()
            break

        # Check if the thief has collected a coin
        if THIEF_POS in COIN_POS:
            winsound.Beep(notes['B'], 25)
            COIN_POS.remove(THIEF_POS)
            SCORE += 1
            if GUARD_DIFFICULTY != "Endless":
                if not COIN_POS:
                    SCORE += 10

        # Draw the floor. This is in the loop so character objects update whenever they move
        print_floor()
        game_hud()
        print("\033[H", end="")

        # Check for thief movement. The game stops updating until one of the move keys is pressed
        MOVE = msvcrt.getch()
        NEW_THIEF_POS = THIEF_POS
        if MOVE == b'M':    # Right key
            NEW_THIEF_POS = (THIEF_POS[0] + 1, THIEF_POS[1])
        if MOVE == b'K':    # Left key
            NEW_THIEF_POS = (THIEF_POS[0] - 1, THIEF_POS[1])
        if MOVE == b'P':    # Down key
            NEW_THIEF_POS = (THIEF_POS[0], THIEF_POS[1] + 1)
        if MOVE == b'H':    # Up key
            NEW_THIEF_POS = (THIEF_POS[0], THIEF_POS[1] - 1)
        if (0 <= NEW_THIEF_POS[0] < FLOOR_WIDTH and 0 <= NEW_THIEF_POS[1] < FLOOR_HEIGHT and NEW_THIEF_POS not in CRATE_POS):
            THIEF_POS = NEW_THIEF_POS
        else:
            winsound.Beep(notes['C'], 25)
        MOVE_COUNTER += 1
   
        # Check for guard movement. After the guard moves, the sub loop repeats
        if MOVE_COUNTER % GUARD_SPEED == 0:
            dx = abs(THIEF_POS[0] - GUARD_POS[0])
            dy = abs(THIEF_POS[1] - GUARD_POS[1])
            if dx > dy:
                if THIEF_POS[0] < GUARD_POS[0]:
                    NEW_GUARD_POS = (max(0, GUARD_POS[0] - 1), GUARD_POS[1])
                elif THIEF_POS[0] > GUARD_POS[0]:
                    NEW_GUARD_POS = (min(FLOOR_WIDTH - 1, GUARD_POS[0] + 1), GUARD_POS[1])
                else:
                    NEW_GUARD_POS = GUARD_POS
            else:
                if THIEF_POS[1] < GUARD_POS[1]:
                    NEW_GUARD_POS = (GUARD_POS[0], max(0, GUARD_POS[1] - 1))
                elif THIEF_POS[1] > GUARD_POS[1]:
                    NEW_GUARD_POS = (GUARD_POS[0], min(FLOOR_HEIGHT - 1, GUARD_POS[1] + 1))
                else:
                    NEW_GUARD_POS = GUARD_POS
            if NEW_GUARD_POS in CRATE_POS:
                if THIEF_POS[0] < GUARD_POS[0]:
                    NEW_GUARD_POS = (max(0, GUARD_POS[0] - 1), GUARD_POS[1])
                elif THIEF_POS[0] > GUARD_POS[0]:
                    NEW_GUARD_POS = (min(FLOOR_WIDTH - 1, GUARD_POS[0] + 1), GUARD_POS[1])
                if NEW_GUARD_POS in CRATE_POS:
                    if THIEF_POS[1] < GUARD_POS[1]:
                        NEW_GUARD_POS = (GUARD_POS[0], max(0, GUARD_POS[1] - 1))
                    elif THIEF_POS[1] > GUARD_POS[1]:
                        NEW_GUARD_POS = (GUARD_POS[0], min(FLOOR_HEIGHT - 1, GUARD_POS[1] + 1))
                if NEW_GUARD_POS in CRATE_POS:
                    NEW_GUARD_POS = GUARD_POS
            GUARD_POS = NEW_GUARD_POS