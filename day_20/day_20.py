import math
from typing import List

from utils.stop_watch import time_me


def get_encrypted_file(filename):
    encrypted = []
    zero = None
    decryption_key = 811589153
    with open(filename) as f:
        for line in f.readlines():
            val = int(line.strip())
            dek_val = val * decryption_key
            value = Value(value=val, dek_value=dek_val)
            encrypted.append(value)
            if value.value == 0:
                zero = value
        return encrypted, zero


class Value:
    def __init__(self, value, dek_value):
        self.value = value
        self.dek_value = dek_value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.dek_value}"


def decryption_algorythm(encrypted_in: List[Value], decrypted_in=None, basic=True):
    if basic:
        decrypted = encrypted_in.copy()
    else:
        decrypted = decrypted_in
    length = len(encrypted_in) - 1
    for number in encrypted_in:
        if number.value == 0:
            continue
        old_index = decrypted.index(number)
        value = number.value if basic else number.dek_value
        new_index = (old_index + value)

        while new_index > length:
            new_index %= length
        while new_index < 0:
            new_index += math.ceil(abs(new_index/length)) * length
        if new_index == 0:
            new_index = length
        decrypted.insert(new_index, decrypted.pop(old_index))

    return decrypted


@time_me
def get_decrypted_solutions():
    test = False
    filename = "test.txt" if test else "day_20.txt"

    encrypted, zero = get_encrypted_file(filename)
    # Part one
    decrypted = decryption_algorythm(encrypted_in=encrypted)
    zero_index = decrypted.index(zero)
    solution_one = 0
    for millennium in range(1000, 3001, 1000):
        searching_for = (zero_index + millennium) % len(decrypted)
        solution_one += decrypted[searching_for].value

    # Part two
    advanced_decrypted = encrypted.copy()
    for i in range(10):
        advanced_decrypted = decryption_algorythm(encrypted_in=encrypted, decrypted_in=advanced_decrypted, basic=False)
    solution_two = 0
    zero_index = advanced_decrypted.index(zero)
    for millennium in range(1000, 3001, 1000):
        searching_for = (zero_index + millennium) % len(advanced_decrypted)
        solution_two += advanced_decrypted[searching_for].dek_value

    return solution_one, solution_two


if __name__ == "__main__":
    one, two = get_decrypted_solutions()
    print(f"One: {one}")
    print(f"Two: {two}")
