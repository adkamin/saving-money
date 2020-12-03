nr_dividers = 0
costs = []
savings = []


def find_min_cost():
    global nr_dividers, costs, savings
    nr_dividers, costs = read_input()
    savings = [[None] * len(costs)] * len(costs)
    total_cost = sum(costs)

    # Remove multiples of 5
    costs = list(filter(lambda x: x % 5, costs))

    saved = saving_money(0, len(costs) - 1, 0)
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
    # Memoization step:
    if savings[i][j] is not None and d < nr_dividers:
        print(f'i={i},j={j},savings={savings[i][j]}')
        return savings[i][j]
    # Base case 1
    if d >= nr_dividers:
        cost_sum = sum(costs[i:j + 1])
        print(f'case 1, d = nr_dividers: {d} = {nr_dividers}, returning {cost_sum - round5(cost_sum)}')
        return cost_sum - round5(cost_sum)
    # Base case 2
    if i == j:
        print(f'case 2, i == j: {i} = {j}, returning {costs[i] - round5(costs[i])}')
        savings[i][j] = costs[i] - round5(costs[i])
        return savings[i][j]
    # Base case 3
    if i == j - 1:
        cost_sum = costs[i] + costs[j]
        print(f'case 3, i == j - 1: {i} = {j - 1}, returning {max(cost_sum - round5(cost_sum), cost_sum - (round5(costs[i]) + round5(costs[j])))}')
        savings[i][j] = max(cost_sum - round5(cost_sum), cost_sum - (round5(costs[i]) + round5(costs[j])))
        return savings[i][j]
    # Recursive case
    max_val = -2
    val = -2
    for k in range(i, j + 1):
        if k == j:
            cost_sum = sum(costs[i:j + 1])
            val = cost_sum - round5(cost_sum)
            print(f'k == j, summing all: {val}')
        else:
            val = saving_money(i, k, d + 1) + saving_money(k + 1, j, d + 1)
            print(f'k < j, result of recursion: {val}')
        max_val = max(val, max_val)
        print(f'best so far: {max_val}')
    print(f'best solution: {max_val}')
    savings[i][j] = max_val
    return max_val


def round5(x):
    return 5 * round(x / 5)
    


