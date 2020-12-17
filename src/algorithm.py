import sys

nr_dividers = 0
costs = []
savings = {}
counter = 0

debug = False

def find_min_cost():
    global nr_dividers, costs, savings, counter
    nr_dividers, costs = read_input()
    savings = {}
    counter = 0
    total_cost = sum(costs)

    # Remove multiples of 5
    costs = list(filter(lambda x: x % 5, costs))

    saved, used = saving_money(0, len(costs) - 1, 0)
    print(f'c={counter}, u={used}', file=sys.stderr)
    return total_cost - saved

def read_input():
    nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    costs = [int(c) for c in input().split(' ')]
    return nr_dividers, costs

def saving_money(i, j, d):
    global counter
    counter += 1

    # Memoization step:
    if (i,j) in savings:
        if debug:
            print(f'i={i},j={j},savings={savings[(i,j)]}', file=sys.stderr)
        max_pair = (-2,0)
        max_found = False
        for cost in savings[(i,j)]:
            if cost > max_pair[0] and savings[(i, j)][cost] <= (nr_dividers - d):
                max_pair = cost, savings[(i, j)][cost]
                max_found = True
        if max_found:
            return max_pair

    # Base case 1
    if d >= nr_dividers:
        cost_sum = sum(costs[i:j + 1])
        if debug:
            print(f'case 1, d = nr_dividers: {d} = {nr_dividers}, returning {cost_sum - round5(cost_sum)}', file=sys.stderr)
        append_savings(i, j, cost_sum - round5(cost_sum), 0)
        return cost_sum - round5(cost_sum), 0

    # Base case 2
    if i == j:
        if debug:
            print(f'case 2, i == j: {i} = {j}, returning {costs[i] - round5(costs[i])}', file=sys.stderr)
        append_savings(i, j, costs[i] - round5(costs[i]), 0)
        return costs[i] - round5(costs[i]), 0

    # Base case 3
    if i == j - 1:
        if debug:
            print("case 3", file=sys.stderr)
        cost_sum = costs[i] + costs[j]
        with_divider = cost_sum - (round5(costs[i]) + round5(costs[j]))
        without_divider = cost_sum - round5(cost_sum)
        if with_divider > without_divider:
            append_savings(i, j, with_divider, 1)
            return with_divider, 1
        else:
            append_savings(i, j, without_divider, 0)
            return without_divider, 0

    # Recursive case
    max_pair = (-2,0)
    for k in range(i, j + 1):
        if k == j:
            cost_sum = sum(costs[i:j + 1])
            pair = (cost_sum - round5(cost_sum), 0)
            if debug:
                print(f'k == j, {pair}', file=sys.stderr)
        else:
            if debug:
                print(f'k < j', file=sys.stderr)
            first = saving_money(i, k, d + 1)
            if debug:
                print(f'first: {first}', file=sys.stderr)
            second = saving_money(k + 1, j, d + 1 + first[1])
            if debug:
                print(f'second: {second}', file=sys.stderr)
            pair = (first[0] + second[0], first[1] + second[1] + 1)
            if debug:
                print(f'total: {pair}', file=sys.stderr)
        if pair[0] > max_pair[0] or (pair[0] == max_pair[0] and pair[1] < max_pair[1]):
            max_pair = pair
    append_savings(i, j, max_pair[0], max_pair[1])
    if debug:
        print(f' max pair: {max_pair}', file=sys.stderr)
    return max_pair # tuple of money saved and dividers used

def round5(x):
    return 5 * round(x / 5)

def append_savings(i, j, c, d):
    if (i, j) in savings:
        if c in savings[(i, j)]:
            if savings[(i, j)][c] > d:
                savings[(i, j)][c] = d
        else:
            savings[(i, j)][c] = d
    else:
        savings[(i, j)] = {c: d}
                



