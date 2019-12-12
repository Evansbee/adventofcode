from helpers.all_of_them import get_numbers


def get_high_score(num_players, last_worth):
    scores = [0] * num_players
    marble_set = [0]
    current_marble = 1
    current_position = 0
    current_player = 0

    while current_marble <= last_worth:
        # print(current_marble,current_position)
        if current_marble % 23 != 0:
            next_position = (current_position + 1) % len(marble_set)
            next_position += 1
            marble_set.insert(next_position, current_marble)
            current_position = next_position
        else:
            scores[current_player] += current_marble
            next_position = (current_position - 7) % len(marble_set)
            scores[current_player] += marble_set[next_position]
            del marble_set[next_position]
            current_position = next_position

        current_marble += 1
        current_player = (1 + current_player) % num_players

    return max(scores)


def problem1(problem_input):
    num_players = get_numbers(problem_input)[0]
    last_worth = get_numbers(problem_input)[1]
    return get_high_score(num_players, last_worth)


def problem2(problem_input):
    num_players = get_numbers(problem_input)[0]
    last_worth = get_numbers(problem_input)[1]
    return get_high_score(num_players, last_worth * 100)
