from utils.stop_watch import time_me

vse_vsote = []


@time_me
def part_one():
    vsota = 0
    with open("day_1.txt") as f:
        for line in f.readlines():
            if line.strip() == "":
                vse_vsote.append(vsota)
                vsota = 0
            else:
                print(line.strip())
                vsota += int(line.strip())
    vse_vsote.append(vsota)
    print(f"MAX VSOTA = {max(vse_vsote)}")


@time_me
def part_two():
    trije_najjaci = 0
    for i in range(3):
        trije_najjaci += max(vse_vsote)
        vse_vsote.remove(max(vse_vsote))
    print(f"Vsota treh najjačih = {trije_najjaci}")


if __name__ == "__main__":
    part_one()
    part_two()
