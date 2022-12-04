from utils.stop_watch import time_me

opponent = []
me = []

with open("day_2.txt") as f:
    for line in f.readlines():
        opponent.append(line.strip()[0])
        me.append(line.strip()[2])

hand_points = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3
}
end_points = {
    "Win": 6,
    "Draw": 3,
    "Loss": 0
}
opps_hand = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors"
}


@time_me
def part_one():
    my_hand = {
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissors"
    }
    score = 0
    for i in range(len(opponent)):
        opp_round = opps_hand[opponent[i]]
        my_round = my_hand[me[i]]
        score += hand_points[my_round]

        if opp_round == my_round:
            score += 3
        elif (opp_round == "Rock" and my_round == "Paper") or (opp_round == "Paper" and my_round == "Scissors") or (opp_round == "Scissors" and my_round == "Rock"):
            score += 6

    print(f"Part One Score = {score}")


@time_me
def part_two():
    my_hand = {
        "X": "Loss",
        "Y": "Draw",
        "Z": "Win"
    }
    score = 0
    for i in range(len(opponent)):
        opp_round = opps_hand[opponent[i]]
        round_end = my_hand[me[i]]

        score += end_points[round_end]

        if round_end == "Draw":
            my_round = opp_round

        elif round_end == "Win":
            if opp_round == "Rock":
                my_round = "Paper"
            elif opp_round == "Paper":
                my_round = "Scissors"
            else:
                my_round = "Rock"
        else:
            if opp_round == "Rock":
                my_round = "Scissors"
            elif opp_round == "Paper":
                my_round = "Rock"
            else:
                my_round = "Paper"

        score += hand_points[my_round]

    print(f"Part Two Score = {score}")


if __name__ == "__main__":
    part_one()
    part_two()
