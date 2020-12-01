nr_dividers = 0
costs = []

def find_min_cost():
    global nr_dividers, costs
    nr_dividers, costs = read_input()
    total_cost = sum(costs)
    
    # Remove multiples of 5
    # costs = list(filter(lambda x: x % 5, costs))

    return total_cost - saving_money(0, len(costs)-1, 0)

def read_input():
    nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    while nr_dividers < 0 or nr_dividers > 25 or nr_dividers >= nr_products: 
        print("Please enter a valid number of products and number of dividers!")
        nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    costs = [int(c) for c in input().split(' ')]
    while len(costs) < 1 or len(costs) > 50000 or len(costs) != nr_products: # check if any of the costs is negative
        print("Please enter valid costs")
        costs = [int(c) for c in input().split(' ')]
    return (nr_dividers, costs)

def saving_money(i, j, d):
    # Base case 1
    if i == j:
        # print("i = j, return round5(costs[i]) - costs[i]: " + str(costs[i] - round5(costs[i])))
        return costs[i] - round5(costs[i])
    # Base case 2
    if i == j - 1:
        cost_sum = costs[i] + costs[j]
        # print(" i = j - 1, return max of adding divider and not adding it: " + str(max(cost_sum - round5(cost_sum), cost_sum - (round5(costs[i]) + round5(costs[j])))))
        return max(cost_sum - round5(cost_sum), cost_sum - (round5(costs[i]) + round5(costs[j])))
    # Base case 3
    if d >= nr_dividers:
        cost_sum = sum(costs[i:j+1])
        # print(f"d >= nr_dividers, return {cost_sum - round5(cost_sum)}, {round5(cost_sum)}, {cost_sum}, {len(costs)}, i={i}, j={j}")
        return cost_sum - round5(cost_sum)
    # Recursive case
    max_val = val = 0
    for k in range(i, j+1):
        if k == j:
            cost_sum = sum(costs[i:j+1])
            val = cost_sum - round5(cost_sum)
            # print(f'k == j: {val}')
        else:
            val = saving_money(i, k, d+1) + saving_money(k+1, j, d+1)
            # print(f'k < j: {val}')
        max_val = max(val, max_val)
    return max_val

def round5(x):
    return 5 * round(x/5)
    


