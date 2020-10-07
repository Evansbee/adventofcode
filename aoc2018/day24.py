from helpers import *
from copy import deepcopy
import re


class Group:
    def __init__(
        self,
        team,
        units,
        hit_points_per_unit,
        immunities,
        weaknesses,
        attack_value,
        attack_type,
        initiative,
    ):
        self.team = team
        self.units = units
        self.hp = hit_points_per_unit
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.ap = attack_value
        self.attack_type = attack_type
        self.initiative = initiative
        self.targetting = None
        self.targetted_by = None

    def effective_power(self):
        return self.units * self.ap

    def expected_damage(self, power, attack_type):
        if attack_type in self.immunities:
            return 0
        if attack_type in self.weaknesses:
            return power * 2
        return power

    def do_damage(self, power, attack_type):
        if attack_type in self.immunities:
            return

        if attack_type in self.weaknesses:
            power *= 2

        units_killed = power // self.hp

        self.units = max(self.units - units_killed, 0)

    def __repr__(self):
        i = ", ".join(self.immunities)
        if len(i) == 0:
            i = "none"

        w = ", ".join(self.weaknesses)
        if len(w) == 0:
            w = "none"

        return f"<Group ({self.team}): Units: {self.units} HP/unit: {self.hp} Attack Power: {self.ap} ({self.attack_type}) Immunities: {i} Weaknesses: {w} Initiative: {self.initiative}>"


def run_simulation(army, boost=0):
    army = deepcopy(army)
    for a in army:
        if a.team == "immune system":
            a.ap += boost

    immune_system_size = len([x for x in army if x.team == "immune system"])
    infection_size = len([x for x in army if x.team == "infection"])

    army.sort(key=lambda x: x.initiative)
    army.sort(key=lambda x: x.effective_power(), reverse=True)

    while immune_system_size > 0 and infection_size > 0:
        print("ROUND")

        did_damage = False
        # reset targgeting information
        for a in army:
            a.targetting = None
            a.targetted_by = None

        # start with the targgeting phase
        army.sort(key=lambda x: x.initiative, reverse=True)
        army.sort(key=lambda x: x.effective_power(), reverse=True)

        for a in army:
            available_targets = [
                t for t in army if t.team != a.team and t.targetted_by == None
            ]
            available_targets.sort(key=lambda t: t.initiative, reverse=True)
            available_targets.sort(key=lambda t: t.effective_power(), reverse=True)
            available_targets.sort(
                key=lambda t: t.expected_damage(a.effective_power(), a.attack_type),
                reverse=True,
            )

            if (
                len(available_targets) > 0
                and available_targets[0].expected_damage(
                    a.effective_power(), a.attack_type
                )
                > 0
            ):
                print(f"UNIT: {a}\nATTACKS: {available_targets[0]}\n\n")
                did_damage = True
                a.targetting = available_targets[0]
                available_targets[0].targetted_by = a

        army.sort(key=lambda x: x.initiative, reverse=True)
        for a in army:
            if a.targetting:
                if a.units > 0:
                    a.targetting.do_damage(a.effective_power(), a.attack_type)

        army = [a for a in army if a.units > 0]

        if not did_damage:
            return []
        # update the result
        immune_system_size = len([x for x in army if x.team == "immune system"])
        infection_size = len([x for x in army if x.team == "infection"])

    return army


def make_army_from_input(problem_input):
    army = []
    current_information = ""
    for line in problem_input:
        if len(line) == 0:
            pass
        elif line == "Immune System:":
            current_information = "immune system"
        elif line == "Infection:":
            current_information = "infection"
        else:
            res = re.search(r"(\d+) units", line)
            units = int(res.group(1))
            res = re.search(r"(\d+) hit points", line)
            hit_points = int(res.group(1))

            res = re.search(r"attack that does (\d+) (\w+) damage", line)
            attack_value = int(res.group(1))
            attack_type = res.group(2)

            res = re.search(r"initiative (\d+)", line)
            initiative = int(res.group(1))

            res = re.search(r"weak to((( \w+),?)+[;\)])", line)
            if res:

                weaknesses = res.group(1).strip(" ;)")
                weaknesses = [w.strip(" ") for w in weaknesses.split(",")]
            else:
                weaknesses = []

            res = re.search(r"immune to((( \w+),?)+[;\)])", line)
            if res:

                immunities = res.group(1).strip(" ;)")
                immunities = [w.strip(" ") for w in immunities.split(",")]
            else:
                immunities = []

            army += [
                Group(
                    current_information,
                    units,
                    hit_points,
                    immunities,
                    weaknesses,
                    attack_value,
                    attack_type,
                    initiative,
                )
            ]

    return army


def problem1(problem_input):

    army = make_army_from_input(problem_input)
    army = run_simulation(army)
    return sum([a.units for a in army])


def problem2(problem_input):
    army = make_army_from_input(problem_input)
    boost = 42
    while True:
        result = run_simulation(army, boost)
        if len(result) > 0:
            if result[0].team == "immune system":
                print(
                    f"WON with boost of {boost}, winning army had {sum([a.units for a in result])} units"
                )
                return sum([a.units for a in result])
            else:
                print(
                    f"Lost with boost of {boost}, winning army had {sum([a.units for a in result])} units"
                )
        else:
            print("Stalemate")
        boost += 1
