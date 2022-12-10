from utils.stop_watch import time_me


def get_instructions(test: bool):
    filename = "test.txt" if test else "day_10.txt"
    with open(filename) as f:
        return [line.strip().split() for line in f.readlines()]


@time_me
def solution_provider(test: bool):
    instructions = get_instructions(test=test)

    register = 1
    ins_index = 0
    completion = False

    # Part One
    signal_strength = 0
    # Part Two
    screen = []

    for cycle in range(1, 241):
        instruction = instructions[ins_index]

        # Part One
        if (cycle + 20) % 40 == 0:
            signal_strength += register * cycle

        # Part Two
        if cycle > 1 and (cycle - 1) % 40 == 0:
            print("".join(screen))
            screen.clear()

        if register - 1 <= (cycle - 1) % 40 <= register + 1:
            screen.append("#")
        else:
            screen.append(" ")

        # Part Both
        if len(instruction) == 1:
            ins_index += 1
        else:
            if not completion:
                completion = True
            else:
                register += int(instruction[1])
                completion = False
                ins_index += 1
        cycle += 1

    print("".join(screen))
    return signal_strength


if __name__ == "__main__":
    print(f"Print Solution One {solution_provider(False)}")
