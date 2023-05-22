import parse_str
import input_gui

input_str = input_gui.initial


def main(INITIAL):
    tableau, col_titles, two_stage = parse_str.input_to_tableau(INITIAL)
    print(col_titles)
    print(tableau)


if __name__ == "__main__":
    main(input_str)
