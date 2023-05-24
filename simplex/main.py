import parse_str
import input_gui


def main():
    input_str = r"""Min: +2 +3 +1
    +1 +1 +1 <= 40
    +2 +1 -1 >= 10
    +0 -1 +1 >= 10
    """
    input_str = input_gui.initial
    t = parse_str.tabulate(input_str)
    print(t.tableau)


if __name__ == "__main__":
    main()
