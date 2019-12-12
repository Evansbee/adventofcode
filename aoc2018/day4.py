from helpers import *
from collections import defaultdict
import operator
import re


def get_numbers_as_strings(line):
    return [x for x in re.findall("[0-9]+", line)]


def get_numbers(line):
    return [int(x) for x in re.findall("[0-9]+", line)]


def date_sorter(a):
    nums = get_numbers_as_strings(a)[:5]
    return int("".join(nums))


def generate_guard_stats_from_input(problem_input):
    problem_input.sort(key=date_sorter)
    guard_naps = defaultdict(list)
    current_guard = 0
    nap_start_minute = 0
    for line in problem_input:
        if "Guard" in line:
            year, month, day, hour, minute, guard = get_numbers(line)
            current_guard = guard
        elif "wakes up" in line:
            year, month, day, hour, minute = get_numbers(line)
            guard_naps[current_guard] += [(nap_start_minute, minute)]
        elif "falls asleep" in line:
            year, month, day, hour, minute = get_numbers(line)
            nap_start_minute = minute

    guard_nap_stats = dict()

    for guard, naps in guard_naps.items():
        sleep_info = defaultdict(int)
        for nap in naps:
            for time in range(nap[0], nap[1]):
                sleep_info[time] += 1
        guard_nap_stats[guard] = sleep_info
    return guard_nap_stats


def problem1(problem_input):
    nap_stats = generate_guard_stats_from_input(problem_input)

    guard_nap_totals = dict()
    for guard, nap_info in nap_stats.items():
        guard_nap_totals[guard] = sum([v for v in nap_info.values()])

    most_sleep_guard = max(guard_nap_totals.items(), key=operator.itemgetter(1))[0]
    most_sleep_minute = max(
        nap_stats[most_sleep_guard].items(), key=operator.itemgetter(1)
    )[0]

    return most_sleep_guard * most_sleep_minute


def problem2(problem_input):
    nap_stats = generate_guard_stats_from_input(problem_input)

    most_slept_minute = -1
    most_slept_minute_time = 0
    most_slept_guard = 0
    for guard, sleep_info in nap_stats.items():
        for k, v in sleep_info.items():
            if v > most_slept_minute_time and k != "total":
                most_slept_minute = k
                most_slept_minute_time = v
                most_slept_guard = guard

    return most_slept_guard * most_slept_minute
