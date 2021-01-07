import random

nr_products = 0            # the number of products
nr_dividers = 0            # the maximum number of dividers
costs = []                 # the list of costs of products
computed = {}              # the dictionary for saving which slices were already computed to avoid double work
max_result = -2            # the maximum result saved so far with the algorithm
magic_number = 0           # the maximum amount possible to save with a given number of dividers
stop_algorithm = False     # true if pruning is possible or the best result (magic number) was already acquired

savings = {}               # the dictionary for memoization in the dynamic programming approach


# reads and processes the input, calls the greedy algorithm and returns the final amount to pay
def find_min_cost():
    global nr_products, nr_dividers, costs, savings, computed,  max_result, magic_number, stop_algorithm
    nr_products, nr_dividers, costs = read_input()
    # nr_products, nr_dividers, costs = randomizer()
    reset_values()
    total_cost = process_input()
    nr_products = len(costs)
    magic_number = (nr_dividers+1)*2
    greedy_approach(0, 0, 0)
    saved1 = max_result
    # saved2, used2 = dynamic_approach(0, len(costs) - 1, 0)
    # print(f'Saved with greedy algorithm: {saved1}. Saved with dynamic programming {saved2}')
    return total_cost - saved1


# reads the input from stdin and saves it into nr_products, nr_dividers and costs
def read_input():
    nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    costs = [int(c) for c in input().split(' ')]
    return nr_products, nr_dividers, costs


# resets some variables for the new sample
def reset_values():
    global savings, computed, max_result, stop_algorithm
    savings = {}
    computed = {}
    max_result = -2
    stop_algorithm = False


# removes multiples of 5, performs modulo 5 on each value and returns the total cost of the costs array
def process_input():
    total_cost = 0
    cost_index = 0
    while cost_index < len(costs):
        c = costs[cost_index]
        total_cost += c
        new_cost = c % 5
        if new_cost == 0:
            del costs[cost_index]
        else:
            cost_index += 1
    return total_cost


# returns a random sample
def randomizer():
    nr_products = random.randint(100, 100)
    nr_dividers = random.randint(25, 25)
    costs = [random.randint(1, 4) for a in range(nr_products)]
    # print(f'nr_products: {nr_products}')
    # print(f'nr_dividers: {nr_dividers}')
    # print(costs)
    return nr_products, nr_dividers, costs


# computes the maximum amount possible to save given the list of costs and the maximum number of dividers
def greedy_approach(c, u, l):
    global computed, max_result, stop_algorithm

    if stop_algorithm or (l, c, u) in computed:
        return

    rewind = False
    used_dividers = u
    current_saved = c
    last_div_location = start_point = l
    current_best = 2
    previous_div_location = saved_from_start = used_from_start = 0

    # computing the maximum saved amount for the slices until the very last divider can be placed
    while used_dividers < nr_dividers and current_best > 0:
        intermediate_sum = 0
        i = last_div_location
        while used_dividers < nr_dividers and i < nr_products - 1:
            intermediate_sum = roundsum(intermediate_sum, costs[i])
            if intermediate_sum >= current_best:
                current_saved += intermediate_sum
                saved_from_start += intermediate_sum
                used_dividers += 1
                used_from_start += 1
                previous_div_location = last_div_location
                last_div_location = i + 1
                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2 and not rewind:
                    # branch 1: continue saving 2 cents
                    greedy_approach(current_saved, used_dividers, last_div_location)
                    # branch 2: rewind and try to save 1 cent first
                    i = previous_div_location
                    last_div_location = i
                    current_saved -= intermediate_sum
                    saved_from_start -= intermediate_sum
                    intermediate_sum = 0
                    current_best = 1
                    used_dividers -= 1
                    used_from_start -= 1
                    rewind = True
                    continue
                rewind = False
                current_best = 2
                intermediate_sum = 0
                if used_dividers >= nr_dividers:
                    break
            i += 1
        current_best -= 1

    # now we compute for the remaining slice how much money is saved/lost. And add it to current_saved + saved_from_start
    total = sum(costs[last_div_location:])
    remainder = total - round5(total)
    saved_from_start += remainder
    current_saved += remainder

    if max_result >= magic_number:
        stop_algorithm = True

    # saving that the given branch was now computed, so that possible double work in other calls is avoided
    used_till_start = used_dividers - used_from_start
    saved_till_start = current_saved - saved_from_start
    computed[(start_point, saved_till_start, used_till_start)] = True

    max_result = max(max_result, current_saved)


# returns the saved amount computed from intermediate saved amount and the current cost
def roundsum(intermediate_sum, current_cost):
    return ((intermediate_sum + current_cost + 2) % 5) - 2

# returns the maximum amount possible to save and the number of dividers used to save such amount
# given the list of costs and the maximum number of dividers
def dynamic_approach(i, j, d):
    # memoization step:
    if (i, j) in savings:
        max_pair = (-2, 0)
        max_found = False
        for cost in savings[(i, j)]:
            if cost > max_pair[0] and savings[(i, j)][cost] <= (nr_dividers - d):
                max_pair = cost, savings[(i, j)][cost]
                max_found = True
        if max_found:
            return max_pair

    # base case 1
    if d >= nr_dividers:
        cost_sum = sum(costs[i:j + 1])
        append_savings(i, j, cost_sum - round5(cost_sum), 0)
        return cost_sum - round5(cost_sum), 0

    # base case 2
    if i == j:
        append_savings(i, j, costs[i] - round5(costs[i]), 0)
        return costs[i] - round5(costs[i]), 0

    # base case 3
    if i == j - 1:
        cost_sum = costs[i] + costs[j]
        with_divider = cost_sum - (round5(costs[i]) + round5(costs[j]))
        without_divider = cost_sum - round5(cost_sum)
        if with_divider > without_divider:
            append_savings(i, j, with_divider, 1)
            return with_divider, 1
        else:
            append_savings(i, j, without_divider, 0)
            return without_divider, 0

    # recursive case
    max_pair = (-2, 0)
    for k in range(i, j + 1):
        if k == j:
            cost_sum = sum(costs[i:j + 1])
            pair = (cost_sum - round5(cost_sum), 0)
        else:
            first = dynamic_approach(i, k, d + 1)
            second = dynamic_approach(k + 1, j, d + 1 + first[1])
            pair = (first[0] + second[0], first[1] + second[1] + 1)
        if pair[0] > max_pair[0] or (pair[0] == max_pair[0] and pair[1] < max_pair[1]):
            max_pair = pair
            if max_pair[0] >= ((nr_dividers - d) + 1) * 2:
                break

    append_savings(i, j, max_pair[0], max_pair[1])
    return max_pair  # tuple of money saved and dividers used


# returns the number rounded to the closest multiple of 5 (for dynamic approach)
def round5(x):
    return 5 * round(x / 5)


# adds the computed value into the dictionary (for dynamic approach)
def append_savings(i, j, c, d):
    if (i, j) in savings:
        if c in savings[(i, j)]:
            if savings[(i, j)][c] > d:
                savings[(i, j)][c] = d
        else:
            savings[(i, j)][c] = d
    else:
        savings[(i, j)] = {c: d}


def main():
    while True:
        try:
            print(find_min_cost())
        except:
            break

if __name__ == '__main__':
    main()