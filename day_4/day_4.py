from utils.stop_watch import time_me

first_elfs = []
second_elfs = []

with open("day_4.txt") as f:
    for line in f.readlines():
        split_line = line.strip().split(",")
        for i in range(2):
            split_coords = split_line[i].split("-")
            the_dict = {"from": int(split_coords[0]), "to": int(split_coords[1])}
            if i == 0:
                first_elfs.append(the_dict)
            else:
                second_elfs.append(the_dict)


@time_me
def part_one():
    contains = 0
    for i in range(len(first_elfs)):
        if first_elfs[i]["from"] >= second_elfs[i]["from"] and first_elfs[i]["to"] <= second_elfs[i]["to"] or \
                second_elfs[i]["from"] >= first_elfs[i]["from"] and second_elfs[i]["to"] <= first_elfs[i]["to"]:
            contains += 1
    print(f"Part Uno Solution: {contains}")


@time_me
def part_two():
    overlaps = 0
    for i in range(len(first_elfs)):
        if second_elfs[i]["from"] <= first_elfs[i]["from"] <= second_elfs[i]["to"] or \
                second_elfs[i]["from"] <= first_elfs[i]["to"] <= second_elfs[i]["to"]:
            overlaps += 1
        elif first_elfs[i]["from"] <= second_elfs[i]["from"] <= first_elfs[i]["to"] or \
                first_elfs[i]["from"] <= second_elfs[i]["to"] <= first_elfs[i]["to"]:
            overlaps += 1

    print(f"Part Due Solution: {overlaps}")


if __name__ == "__main__":
    part_one()
    part_two()
