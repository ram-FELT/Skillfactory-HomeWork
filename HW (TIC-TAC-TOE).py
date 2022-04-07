print(" Крестики нолики (итоговое задание) ")

playing_field = list(range(1, 10))


def draw_playing_field(playing_field):
    for i in (reversed(range(3))):
        print("(", playing_field[0 + i * 3], "][", playing_field[1 + i * 3], "][", playing_field[2 + i * 3], ")")


def take_input(player_character):
    valid = False
    while not valid:
        player_choice = input("Куда поставим " + player_character + "? ")
        try:
            player_choice = int(player_choice)
        except:
            print("Некорректный ввод. Вы уверены, что ввели число?")
            continue
        if player_choice >= 1 and player_choice <= 9:
            if (str(playing_field[player_choice - 1]) not in "XO"):
                playing_field[player_choice - 1] = player_character
                valid = True
            else:
                print("Эта клетка уже занята!")
        else:
            print("Некорректный ввод. Введите число от 1 до 9.")


def check_win(playing_field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if playing_field[each[0]] == playing_field[each[1]] == playing_field[each[2]]:
            return playing_field[each[0]]
    return False


def main(playing_field):
    counter = 0
    win = False
    while not win:
        draw_playing_field(playing_field)
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1
        if counter > 4:
            tmp = check_win(playing_field)
            if tmp:
                print("\(*^*)/", tmp, "выиграл!")
                win = True
                break
        if counter == 9:
            print("	╮(;*~*)╭ НИЧЬЯ ┐(*~*;)┌")
            break
    draw_playing_field(playing_field)


main(playing_field)

input("Нажмите Enter для выхода!")
