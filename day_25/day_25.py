from utils.stop_watch import time_me


def load_numbers(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def snafu_to_human(weird_num: str):
    human_number: int = 0
    for i, char in enumerate(weird_num):
        what_you_call_it = 5 ** (len(weird_num) - i - 1)
        if char.isdigit():
            human_number += what_you_call_it * int(char)
        elif char == "-":
            human_number -= what_you_call_it
        elif char == "=":
            human_number -= 2 * what_you_call_it
    return human_number


def human_to_snafu(human_number: int):
    snafu = ""
    snafu_digits = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}
    exponent = 0
    going_up = True
    while exponent >= 0:
        if going_up:
            while 5 ** exponent <= human_number:
                exponent += 1
            going_up = False
        digits = 0
        while digits * 5 ** exponent < human_number + 2 * 5 ** exponent:
            digits += 1
            test = digits * 5 ** exponent
        digits -= 2
        test2 = digits * 5 ** exponent
        if abs(human_number - digits * 5 ** exponent) > abs(human_number - (digits - 1) * 5 ** exponent):
            digits -= 1
        snafu += snafu_digits[digits]
        human_number -= digits * 5 ** exponent
        exponent -= 1
    if snafu[0] == "0":
        snafu = snafu[1:]
    return snafu

@time_me
def last_day_woo():
    test = False
    filename = "test.txt" if test else "day_25.txt"
    weird_numbers = load_numbers(filename)
    combined_fuel = 0
    for odd_number in weird_numbers:
        combined_fuel += snafu_to_human(weird_num=odd_number)
    snafu = human_to_snafu(combined_fuel)

    if combined_fuel == snafu_to_human(snafu):
        return snafu


if __name__ == "__main__":
    print(f"Day 25 yay {last_day_woo()}")
