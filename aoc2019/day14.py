from helpers import *
from math import ceil
import math


class Reaction:
    def __init__(self, input_string):
        self.reaction_description = dict()
        inputs, output = input_string.split(" => ")
        self.reaction_description[output.split(" ")[1]] = int(output.split(" ")[0])
        self.reaction_produces = output.split(" ")[1]
        for i in inputs.split(", "):
            # -1 indicates it's consumed by the reaction
            self.reaction_description[i.split(" ")[1]] = -1 * int(i.split(" ")[0])

    def __repr__(self):
        retval = ""
        for chemical, count in {
            k: v for k, v in self.reaction_description.items() if v < 0
        }.items():
            retval += f"{-count} {chemical} "
        retval += "=> "
        for chemical, count in {
            k: v for k, v in self.reaction_description.items() if v > 0
        }.items():
            retval += f"{count} {chemical} "
        return retval


def problem1(problem_input):
    recipes = []

    reactions = []
    for line in problem_input:
        r = Reaction(line)
        reactions += [r]

        print(r, r.reaction_description)

    compound = {"FUEL": -1}
    ore_required = 0

    def find_recipe_for(compound):
        for r in reactions:
            if r.reaction_produces == compound:
                return r
        return None

    while len({k: v for k, v in compound.items() if v < 0}) > 0:
        compound_step = compound.copy()

        for k, v in compound.items():
            if v < 0:
                compound_needed = -v
                recipe = find_recipe_for(k)
                print(recipe, k)
                recipe_makes = recipe.reaction_description[k]

                run_times = math.ceil(compound_needed / recipe_makes)
                print(run_times)
                left_over_count = recipe_makes * run_times - compound_needed

                # compound_step[k] = compound_step.get(k,0) + left_over_count
                for x, y in recipe.reaction_description.items():
                    compound_step[x] = compound_step.get(x, 0) + y * run_times

            # else:
            # compound_step[k] = compound_step.get(k,0) + v

        ore_required -= compound_step.get("ORE", 0)
        compound_step["ORE"] = 0
        compound = {k: v for k, v in compound_step.items() if v != 0}
    return ore_required


def problem2(problem_input):
    recipes = []

    reactions = []
    for line in problem_input:
        r = Reaction(line)
        reactions += [r]

        print(r, r.reaction_description)

    compound = {"FUEL": -1863740}
    fuel = 1863740
    ore_required = 0

    def find_recipe_for(compound):
        for r in reactions:
            if r.reaction_produces == compound:
                return r
        return None

    while ore_required <= 1000000000000:
        if len({k: v for k, v in compound.items() if v < 0}) == 0:
            fuel += 1
            compound["FUEL"] = compound.get("FUEL", 0) - 1
            print(f"Fuel Count: {fuel}, Ore Required: {ore_required}")
        else:
            compound_step = compound.copy()

            for k, v in compound.items():
                if v < 0:
                    compound_needed = -v
                    recipe = find_recipe_for(k)

                    recipe_makes = recipe.reaction_description[k]

                    run_times = math.ceil(compound_needed / recipe_makes)

                    left_over_count = recipe_makes * run_times - compound_needed

                    # compound_step[k] = compound_step.get(k,0) + left_over_count
                    for x, y in recipe.reaction_description.items():
                        compound_step[x] = compound_step.get(x, 0) + y * run_times

                # else:
                # compound_step[k] = compound_step.get(k,0) + v

            ore_required -= compound_step.get("ORE", 0)
            compound_step["ORE"] = 0
            compound = {k: v for k, v in compound_step.items() if v != 0}
    return fuel - 1
