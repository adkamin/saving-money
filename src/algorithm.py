import sys
import random
import time

nr_products = 0
nr_dividers = 0
costs = []
savings = {}
counter = 0
results_list = {}
remaining_sums = {}
intermediate_sums = {}

def roundsum(intermediate_sum, next_value):
    return ((intermediate_sum + next_value + 2) % 5) - 2

def find_min_cost():
    global nr_products, nr_dividers, costs, savings, counter, results_list, remaining_sums, intermediate_sums
    # nr_products, nr_dividers, costs = read_input()
    nr_products, nr_dividers, costs = randomizer()
    savings = {}
    counter = 0
    results_list = {}
    remaining_sums = {}
    intermediate_sums = {}
    total_cost = sum(costs)

    # Remove multiples of 5
    costs = list(filter(lambda x: x % 5, costs))
    costs = list(map(lambda x: x % 5, costs))
    nr_products = len(costs)

    start = time.process_time()
    saving_money_2c(0, 0, 0, [], [])
    print("------------------------------------------------------------------------------------")
    mid = time.process_time()
    saved2, used2 = saving_money(0, len(costs) - 1, 0)
    end = time.process_time()

    # print(f'Greedy algorithm={mid-start} seconds, Dynamic programming={end-mid}', file=sys.stderr)

    saved1 = max(results_list)
    div_locs = results_list[saved1]
    # print(f'div_locs={div_locs}')

    # print(f'c={counter}, u={used}', file=sys.stderr)
    print(f'{saved1} and {saved2}')
    if(saved1 != saved2):
        print("OOOH NOOO")
        return -10
    return total_cost - saved1

def read_input():
    nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    costs = [int(c) for c in input().split(' ')]
    return nr_products, nr_dividers, costs

def randomizer():
    nr_products = random.randint(10, 10)
    # nr_dividers =
    nr_dividers = random.randint(1,9)
    costs = [random.randint(1, 5) for a in range(nr_products)]
    print(f'nr_dividers: {nr_dividers}')
    print(costs)
    return nr_products, nr_dividers, costs

def saving_money_3():
    # [(2, 3), (3, 5)] save 2 cents. length is at most n*(n-1)/2
    # [(4, 5), (6, 7)] save 1 cent
    # [(4, 5), (6, 7)] save 0 cents
    # [(4, 5), (6, 7)] save -1 cents
    # [(4, 5), (6, 7)] save -2 cents

    slices = {2: [], 1: [], 0: [], -1: [], -2: []}
    
    for size in range(1, nr_products + 1):
        for start_point in range(0, nr_products):
            if start_point + size < nr_products:
                cost_sum = sum(costs[start_point:start_point+size])
                saved = cost_sum - round5(cost_sum)
                slices[saved].append((start_point, start_point+size-1))

    # compute magic number: (d+1)*2
    # d+1: pick d+1 slices from slices[2] which sums to magic number
    # if that doesnt work:
    # magic number: magic number - 1
    # d+1: pick d slices from slices[2] and 1 slice from slices[1]
    # if that doesnt work:
    # magic number: magic number - 1
    # d+1: 
    # d: pick d slices from slices[2]

    # d = 2
    # mn = 6
    # 3: 2 2 2
    # mn = 5
    # 3: 2 2 1
    # mn = 4
    # 3: 2 2 0
    # 3: 2 1 1
    # 2: 2 2
    # mn = 3
    # 3: 2 1 0
    # 3: 1 1 1
    # 3: 2 2 -1
    # 2: 2 1
    # mn = 2
    # 3: 2 2 -2
    # 3: 2 1 -1
    # 3: 2 0 0
    # 3: 1 1 0
    # 2: 2 0
    # 2: 1 1
    # 1: 2
    # mn = 1
    # 3: 1 2 -2
    # 3: 1 1 -1
    # 3: 1 0 0
    # 3: 2 0 -1

    # d = 4
    # mn = 10
    # 5: 2 2 2 2 2
    # mn = 9
    # 5: 2 2 2 2 1
    # mn = 8
    # 5: 2 2 2 2 0
    # 5: 2 2 2 1 1
    # 4: 2 2 2 2

    # 3 8 13 13 | 4 18 | 4

    # print(slices)
    
    return 0

def solve_stuff():
    pass


def saving_money_2c(c, u, l, d, s):     # s = saved_per_slice
    global results_list, first_time, second_time, remaining_sums, intermediate_sums
    
    used_dividers = u
    current_best = 2
    current_saved = c
    last_div_location = l
    previous_div_location = 0
    div_locs = d
    starting_point = l
    skip = False


    # 1 2 | 4 7 8 2 4 6 8 3       rewind
    # 1 2 | 4 7 8 2 | 4 6 | 8 3   normal

    start = time.process_time()
    while used_dividers < nr_dividers-1 and current_best > 0 and not skip:
        intermediate_sum = 0
        i = last_div_location
        while used_dividers < nr_dividers-1 and i < nr_products-1:
            intermediate_sum = roundsum(intermediate_sum, costs[i])
            if intermediate_sum >= current_best:
                current_saved += intermediate_sum
                s.append(current_saved)
                used_dividers += 1
                previous_div_location = last_div_location
                last_div_location = i+1
                div_locs.append(last_div_location)
                if last_div_location in intermediate_sums:

                    lst = list(filter(lambda x: x[0] <= nr_dividers - used_dividers, intermediate_sums[last_div_location]))
                    if len(lst) > 0:
                        skip = True
                        print("memo")
                        best = max(lst, key=lambda x: x[1])[1] # 3 ... nr_products
                        current_saved += best                  # 0 ... 3
                        break
                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2:
                    saving_money_2c(current_saved, used_dividers, last_div_location, div_locs, s)
                    # Rewind step:
                    dummy_sum = intermediate_sum
                    intermediate_sum = 0
                    for j in range(previous_div_location, last_div_location):
                        intermediate_sum = roundsum(intermediate_sum, costs[j])
                        if intermediate_sum >= 1:
                            current_saved = current_saved - dummy_sum + intermediate_sum
                            s.append(current_saved)
                            div_locs.pop()
                            last_div_location = j+1
                            div_locs.append(last_div_location)
                            i = last_div_location-1
                            intermediate_sum = 0
                            break
                current_best = 2
                intermediate_sum = 0
                if used_dividers >= nr_dividers-1:
                    break
            i += 1
        current_best -= 1

    max_saved = -4
    mid = time.process_time()

    if not skip:
        if last_div_location not in remaining_sums:
            if last_div_location+1 < nr_products:
                # print(f'slice from {last_div_location} to {nr_products}')
                total_cost = sum(costs[last_div_location:])
                total_saved = roundsum(0, total_cost)
                max_saved = total_saved
                max_div_loc = last_div_location
                left_saved = 0
                if total_saved != 0:
                    for i in range(last_div_location+1, nr_products):
                        left_saved = roundsum(left_saved, costs[i-1])
                        right_saved = roundsum(total_saved, -left_saved)
                        combined_saved = left_saved + right_saved
                        if combined_saved > max_saved:
                            max_saved = combined_saved
                            max_div_loc = i
                            if max_saved >= 4:
                                break
                if max_div_loc != last_div_location:
                    div_locs.append(max_div_loc)
            else:
                max_saved = costs[last_div_location] - round5(costs[last_div_location])
            remaining_sums[last_div_location] = max_saved
        else:
            max_saved = remaining_sums[last_div_location]
    else:
        max_saved = 0
    results_list[current_saved + max_saved] = div_locs


    # memoization
    saved_till_starting_point = 0
    div_used_from_starting_point = 0
    if starting_point > 0:
        index = div_locs.index(starting_point)
        saved_till_starting_point = s[index]
        div_used_from_starting_point = used_dividers - len(s[index:])
    saved_in_slice = current_saved + max_saved - saved_till_starting_point
    if starting_point in intermediate_sums:
        intermediate_sums[starting_point].append((div_used_from_starting_point, saved_in_slice))
    else:
        intermediate_sums[starting_point] = [(div_used_from_starting_point, saved_in_slice)]
    end = time.process_time()

    print(f'memo for first part: intermediate sums = {intermediate_sums}')
    print(f'memo for second part: resulting sums = {remaining_sums}')
    print(f'results list = {results_list}')

    # 1 2 3 4 5 6 7 8 9
    # 1 | 1 | 3 4 5 6 | 7 8 9)
    # s = [1,2,4,5,7,8]
    # div_locs = [1,2,6]

def saving_money_2b(start, end, d, reverse):
    used_dividers = 0
    current_best = 2
    current_saved = 0
    last_div_location = start
    if reverse:
        last_div_location = end
    previous_div_location = 0
    div_locs = []

    while used_dividers < d and current_best > 0:
        if reverse:
            for i in range(last_div_location, start, -1):
                print(f'{i} {last_div_location+1}: {costs[i:last_div_location+1]}')
                cost_sum = sum(costs[i:last_div_location+1])
                saved = cost_sum - round5(cost_sum)
                # cost_rest = sum(costs[last_div_location:])
                # saved_rest = cost_rest - round5(cost_rest)
                # if saved_rest > saved:
                #     continue
                # x | x x x x: saved = 1, saved_rest = 2
                if saved >= current_best:
                    current_saved += saved
                    used_dividers += 1
                    previous_div_location = last_div_location
                    last_div_location = i-1
                    print(last_div_location)
                    div_locs.append(last_div_location+1)
                    if used_dividers >= d:
                        break
                    # Rewind step
                    if previous_div_location-last_div_location > 2:
                        print("recursion")
                        saved_on_reverse, used_on_reverse = saving_money_2b(last_div_location+1, previous_div_location, d-used_dividers, not reverse)
                        if saved_on_reverse > saved:
                            current_saved = current_saved - saved + saved_on_reverse
                            used_dividers += used_on_reverse
        else:
            for i in range(last_div_location, end):
                print(f'{last_div_location} {i+1}: {costs[last_div_location:i+1]}')
                cost_sum = sum(costs[last_div_location:i+1])
                saved = cost_sum - round5(cost_sum)
                # cost_rest = sum(costs[last_div_location:])
                # saved_rest = cost_rest - round5(cost_rest)
                # if saved_rest > saved:
                #     continue
                # x | x x x x: saved = 1, saved_rest = 2
                if saved >= current_best:
                    current_saved += saved
                    used_dividers += 1
                    previous_div_location = last_div_location
                    last_div_location = i+1
                    print(last_div_location)
                    div_locs.append(last_div_location)
                    if used_dividers >= d:
                        break
                    # Rewind step
                    if last_div_location-previous_div_location > 2:
                        print("recursion")
                        saved_on_reverse, used_on_reverse = saving_money_2b(previous_div_location, last_div_location-1, d-used_dividers, not reverse)
                        if saved_on_reverse > saved:
                            current_saved = current_saved - saved + saved_on_reverse
                            used_dividers += used_on_reverse
        current_best -= 1

    # Backward search
    # print(used_dividers)
    # if used_dividers < nr_dividers:
    #     for i in range(len(div_locs)+1):
    #         start = 0
    #         end = nr_products
    #         if i > 0:
    #             start = div_locs[i-1]
    #         if i < len(div_locs):
    #             end = div_locs[i]
    #         print(f'slice=({start}, {end})')


    print(f'div locs: {div_locs}')
    remaining_sum = 0
    if reverse:
        print("reverse")
        print(f'{start} {last_div_location+1}')
        remaining_sum = sum(costs[start:last_div_location+1])
        print(f'current_saved = {current_saved}')
        print(f'remaining: {remaining_sum} - {round5(remaining_sum)}')
    else:
        remaining_sum = sum(costs[last_div_location:end+1])
        print(f'current_saved = {current_saved}')
        print(f'remaining: {remaining_sum} - {round5(remaining_sum)}')
    return current_saved + (remaining_sum - round5(remaining_sum)), used_dividers

def saving_money_2():
    used_dividers = 0
    current_best = 2
    current_saved = 0
    last_div_location = 0

    while used_dividers < nr_dividers and current_best > 0:
        for i in range(last_div_location, nr_products):
            cost_sum = sum(costs[last_div_location:i+1])
            saved = cost_sum - round5(cost_sum)
            cost_rest = sum(costs[last_div_location:])
            saved_rest = cost_rest - round5(cost_rest)
            if saved_rest > saved:
                continue
            # print(f'saved={saved}, i={i}, saved_rest={saved_rest}')
            if saved >= current_best:
                current_saved += saved
                used_dividers += 1
                last_div_location = i+1
                print(f'div location={last_div_location}')
                if used_dividers >= nr_dividers:
                    # print("break")
                    break
        current_best -= 1

    remaining_sum = sum(costs[last_div_location:])
    return current_saved + (remaining_sum - round5(remaining_sum))

def saving_money(i, j, d):
    global counter
    counter += 1

    # Memoization step:
    if (i,j) in savings:
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
        append_savings(i, j, cost_sum - round5(cost_sum), 0)
        return cost_sum - round5(cost_sum), 0

    # Base case 2
    if i == j:
        append_savings(i, j, costs[i] - round5(costs[i]), 0)
        return costs[i] - round5(costs[i]), 0

    # Base case 3
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

    # Recursive case
    max_pair = (-2,0)
    for k in range(i, j + 1):
        if k == j:
            cost_sum = sum(costs[i:j + 1])
            pair = (cost_sum - round5(cost_sum), 0)
        else:
            first = saving_money(i, k, d + 1)
            second = saving_money(k + 1, j, d + 1 + first[1])
            pair = (first[0] + second[0], first[1] + second[1] + 1)
        if pair[0] > max_pair[0] or (pair[0] == max_pair[0] and pair[1] < max_pair[1]):
            max_pair = pair
            if max_pair[0] >= ((nr_dividers-d)+1)*2:
                break
            
    append_savings(i, j, max_pair[0], max_pair[1])
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

