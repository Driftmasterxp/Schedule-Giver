import random
from math import ceil


CyclePool = {
    "ProVOD": [4, "10 | VOD Review + Ripcore + Concepts (GENGvs.MST)", 10],
    "AwareVOD": [1, "10 | Awareness VOD Review (GENGvs.MST)", 10],
    "Meditation": [2, "15 | Meditation", 15],
    "MyVOD": [4, "5 | VOD Review + Ripcore + Concepts (6mans)", 5],
    "CommVOD": [1, "10 | Comms VOD Review (6mans)", 10],
    "Ripcore": [5, "5 | Ripcore (6mans + GENG)", 5],
    "Concepts": [2, "10 | Concepts (Map)", 15],
    "FastAerial": [1, "5 | Fast Aerial (2.159 **Down + X Gap**)", 5],
    "Rx ImpossibleRings": [1, "5:00 | Impossible Rings: {}x (Fin **Use Sides of Stick + Don't hold 1 direction = Be Majestic**)", 5],
    "Rx AirDribbleGauntlet": [1, "5 | Air Dribble Gauntlet: {}x (Lvl. 9 **Get under the ball + Full Boost or Feather + Use Stick Less | Every attempt should look good**)", 5],
    "Rx AirDribbleGauntlet AR": [1, "5 | Air Dribble Gauntlet: {}x (Full Airroll Lvl. 9 **Get under the ball + Full Boost or Feather + Use Stick Less | Every attempt should look good**)", 5],
    "UltiLines": [1, "5 | Boost Drills (**Ulti Lines**)", 5],
    "Rx Alpha": [2, "30 | Alpha: {}x (1 | , 2 | , 3 | , 4 | )", 30],
    "Rx Beta": [1, "30 | Beta: {}x (1 | , 2 | , 3 | , 4 | )", 30],
    "Focus 6mans": [0, "24 | 6mans (b 3-0 9/10 Focus Rep | Great Control | Great Demos | A lot of IMPACT Goals | No mistakes into goals)", 24],
    "Comm 6mans": [0, "24 | 6mans (b 3-0 9/10 Comm Rep | Great Control | Great Demos | A lot of IMPACT Goals | No mistakes into goals)", 24],
    "Flow 6mans": [0, "24 | 6mans (b 3-0 9/10 Flow Rep | Great Control | Great Demos | A lot of IMPACT Goals | No mistakes into goals)", 24]
}

Typeof6mans = {
    "Focus 6mans": [3, "24 | 6mans (b 3-0 9/10 Focus Rep | Great Control | Great Demos | A lot of IMPACT Goals | No mistakes into goals)", 24],
    "Comm 6mans": [1, "24 | 6mans (b 3-0 9/10 Comm Rep | Great Control | Great Demos | A lot of IMPACT Goals | No mistakes into goals)", 24],
    "Flow 6mans": [1, "24 | 6mans (b 3-0 9/10 Flow Rep | Great Control | Great Demos | A lot of IMPACT Goals | No mistakes into goals)", 24]
}

Orderof6mans = random.sample(list(Typeof6mans.keys()), 5, counts=[Typeof6mans[x][0] for x in Typeof6mans.keys()])

CyclePool[Orderof6mans[4]] = [1, Typeof6mans[Orderof6mans[4]][1], 24]


Clen = sum(CyclePool[x][0] for x in CyclePool)

Day = random.sample(list(CyclePool.keys()), Clen, counts=[CyclePool[x][0] for x in CyclePool.keys()])

# print(Day)


def Break(Cycle, Time):
    if Cycle == 1:
        return "> 20 min Break MRH"
    elif Cycle == 2:
        return "> 50 min Break MRHE"
    elif Cycle == 3:
        return "> 120 min Break Workout + Shower + Protein Shake"
    elif Cycle == 4:
        return "> " + str(ceil(Time/4/5) * 5) + " min Break MRHE"
    else:
        return


time = 0


def cycletobreak(cycle):
    if cycle == 1:
        return time > 100
    elif cycle == 2:
        return time > 240
    elif cycle == 3:
        return time == 24
    else:
        return False


shift = 0
num6ms = 0

for c in range(1, 6):
    # print("c = {}".format(c))
    # print(Day)  # Maintenance purposes

    if c != 2:
        time = 0

        Day.insert(shift, Orderof6mans[num6ms])

        num6ms += 1
        time += 24
        shift += 1

    if c == 5:
        Day.append("> 5 min Break Meditation")
        break

    for no in range(len(Day[shift:])):
        if cycletobreak(c):
            shift += no  # Plus 1 accounting for what we just let into cycle
            break

        x = Day[shift:][no]
        time += CyclePool[x][2]

        # print("c = {} time = {} no = {} x = {}".format(c, time, no, x))  # Maintenance purposes
        if no == len(Day[shift:]) - 1:
            shift += no + 1

    Day.insert(shift, Break(c, time))
    shift += 1

# print(Day)

for mo in range(len(Day)-1):  # Inserts Meditation break after every 6mans if not already accounted for in bigger break
    m = Day[mo]
    if m.find("6mans") > -1:
        if Day[mo + 1].find("> ") == -1:
            Day.insert(mo + 1, "> 5 min Break Meditation")

# print(Day)


def rounder(notround):
    r = str(round(notround, 2))
    if len(r) == 4:
        return r
    else:
        return r + "0"


for x in range(0, len(Day)):  # Add Weighted Randomizer Speeds
    if Day[x].find("Rx ") > -1:  # If it can find the "x " of the "#.##x "
        Day[x] = rounder(1 * random.random() ** .6 + .5) + Day[x][Day[x].find("x "):]
        # print(Day[x])  # Testing purposes


on = 0
off = 15

print(" :\n5 | Meditation\n10 | Run")

for x in Day:
    if x.isidentifier() or x.endswith("6mans"):
        on += CyclePool[x][2]  # Counts time on for inspection purposes later
        print(CyclePool[x][1])
    elif x[0].isnumeric():  # Checks if this a Randomized Speed Portion
        on += CyclePool["Rx" + x[5:]][2] # Takes Randomized Speeds off for dictionary parsing then adds time of portion
        print(CyclePool["Rx" + x[5:]][1].format(x[:4])) # Takes Randomized Speeds off for dictionary parsing then inserts it back into output string
    else:  # Breaks aren't apart of the CyclePool so we filter for them and
        off += int(x.split()[1])
        print(x)  # output them cleanly


total = on + off
variance = 24 * 5
print("\n\nMaintenance\ntotal ({}-{}) = on ({}-{}) + off ({})\n{}".format(total, total + variance, on, on + variance, off, Day))
