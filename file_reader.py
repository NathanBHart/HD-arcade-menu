from enum import Enum


NUMBER_OF_PARAMS_GAME_FILE = 9
ORIGINALS = "resources/originals/original_games.txt"

class Properties(Enum):

    # Order of properties
    title = 0
    description = 1
    background_image = 2
    music = 3
    color = 4
    game_file = 5
    hi_score_file = 6
    number_of_players = 7
    completion_time = 8

def read_file(file):

    temp = open(file, "r")

    f = temp.read().splitlines()

    list_item_count = 0

    i = 0

    for stuff in f:

        if str(f[i]) == "-li":
            list_item_count += 1

        i += 1


    x = [{} for j in range(list_item_count)]

    item = 0
    i = 0

    for stuff in f:

        if str(f[i]) == "-li":

            scan = True
            j = 1
            c_type: int = 0

            while c_type < NUMBER_OF_PARAMS_GAME_FILE:

                if str(f[i + j])[0] != "#" or str(f[i + j]) != "NONE":

                    x[item][Properties(c_type).name] = (f[i + j])

                    c_type += 1

                j += 1

            item += 1

        i += 1

    temp.close()

    return x