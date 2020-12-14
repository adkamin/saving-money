import sys

nr_dividers = 0
costs = []
savings = {}
counter = 0


def find_min_cost():
    global nr_dividers, costs, savings, counter
    nr_dividers, costs = read_input()
    savings = {}
    counter = 0
    total_cost = sum(costs)

    # Remove multiples of 5
    costs = list(filter(lambda x: x % 5, costs))

    saved, used = saving_money(0, len(costs) - 1, 0)
    # print(f'saved: {saved}')
    # print(f'used: {used}', file=sys.stderr)
    print(f'c={counter}, u={used}')
    return total_cost - saved

def read_input():
    nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    # while nr_dividers < 0 or nr_dividers > 25 or nr_dividers >= nr_products:
    #     print("Please enter a valid number of products and number of dividers!")
    #     nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    costs = [int(c) for c in input().split(' ')]
    # while len(costs) < 1 or len(costs) > 50000 or len(costs) != nr_products: # check if any of the costs is negative
    #     print("Please enter valid costs")
    #     costs = [int(c) for c in input().split(' ')]
    return nr_dividers, costs


def saving_money(i, j, d):
    global counter
    counter += 1
    # print(counter)
    # Memoization step:
    # if (i,j) in savings:
    #     print(f'i={i},j={j},savings={savings[(i,j)]}')
    #     max_pair = (-2,0)
    #     max_found = False
    #     # print(len(savings[(i,j)]))
    #     for (cost, dividers) in savings[(i,j)]:
    #         if cost > max_pair[0] and dividers <= (nr_dividers - d):
    #             max_pair = cost, dividers
    #             # print("hiiiiiii")
    #             # print(f'({i},{j}): {cost}; dividers={dividers}, nr_dividers={nr_dividers}, d={d}')
    #             max_found = True
    #     if max_found:
    #         return max_pair

    # Base case 1
    if d >= nr_dividers:
        cost_sum = sum(costs[i:j + 1])
        print(f'case 1, d = nr_dividers: {d} = {nr_dividers}, returning {cost_sum - round5(cost_sum)}')
        if (i,j) in savings:
            savings[(i,j)].append((cost_sum - round5(cost_sum), 0))
        else:
            savings[(i,j)] = [(cost_sum - round5(cost_sum), 0)]
        return cost_sum - round5(cost_sum), 0

    # Base case 2
    if i == j:
        print(f'case 2, i == j: {i} = {j}, returning {costs[i] - round5(costs[i])}')
        if (i,j) in savings:
            savings[(i,j)].append((costs[i] - round5(costs[i]), 0))
        else:
            savings[(i,j)] = [(costs[i] - round5(costs[i]), 0)]
        return costs[i] - round5(costs[i]), 0

    # Base case 3
    if i == j - 1:
        print("case 3")
        cost_sum = costs[i] + costs[j]
        with_divider = cost_sum - (round5(costs[i]) + round5(costs[j]))
        without_divider = cost_sum - round5(cost_sum)
        if with_divider > without_divider:
            if (i,j) in savings:
                savings[(i,j)].append((without_divider, 1))
            else:
                savings[(i,j)] = [(without_divider, 1)]
            return with_divider, 1
        else:
            if (i,j) in savings:
                savings[(i,j)].append((with_divider, 0))
            else:
                savings[(i,j)] = [(with_divider, 0)]
            return without_divider, 0

    # Recursive case
    max_pair = (-2,0)
    for k in range(i, j + 1):
        if k == j:
            cost_sum = sum(costs[i:j + 1])
            pair = (cost_sum - round5(cost_sum), 0)
            print(f'k == j, {pair}')
        else:
            print(f'k < j')
            first = saving_money(i, k, d + 1)
            print(f'first: {first}')
            second = saving_money(k + 1, j, d + 1)
            print(f'second: {second}')
            pair = (first[0] + second[0], first[1] + second[1] + 1)
            print(f'total: {pair}')
        if pair[0] > max_pair[0] or (pair[0] == max_pair[0] and pair[1] > max_pair[1]):
            max_pair = pair
    if (i,j) in savings:
        savings[(i,j)].append(max_pair)
    else:
        savings[(i,j)] = [max_pair]
    print(f' max pair: {max_pair}')
    return max_pair  # tuple of money saved and dividers used

def round5(x):
    return 5 * round(x / 5)


