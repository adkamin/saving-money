import sys
import random
import time

nr_products = 0
nr_dividers = 0
costs = []
savings = {}
results_list = {}
remaining_sums = {}
intermediate_sums = {}
max_result = 0
samples = 0
oohnoos = 0
counter = 0
magic_number = 0
stop_algorithm = False

def roundsum(intermediate_sum, next_value):
    return ((intermediate_sum + next_value + 2) % 5) - 2

def find_min_cost():
    global nr_products, nr_dividers, costs, savings, results_list, remaining_sums
    global intermediate_sums, samples, oohnoos, counter, max_result, magic_number, stop_algorithm
    nr_products, nr_dividers, costs = read_input()
    # nr_products, nr_dividers, costs = randomizer()

    savings = {}
    results_list = {}
    remaining_sums = {}
    intermediate_sums = {}
    max_result = -2
    counter = 0
    stop_algorithm = False

    total_cost = process_input()

    nr_products = len(costs)
    magic_number = (nr_dividers+1)*2

    start = time.process_time()
    last_attempt(0, 0, 0)
    mid = time.process_time()
    # saved2, used2 = saving_money(0, len(costs) - 1, 0)
    end = time.process_time()

    # print(f'Greedy algorithm={mid-start} seconds, Dynamic programming={end-mid}', file=sys.stderr)

    saved1 = max_result
    # print(f'div_locs={div_locs}')

    # print(f'c={counter}, u={used}', file=sys.stderr)
    samples += 1
    # print(f'{saved1} and {saved2}')
    # if(saved1 != saved2):
    #     oohnoos += 1
    #     print(f'wrong result')
    #     print(f'OOH NOOs: {oohnoos}')
    #     print(f'Samples: {samples}')
    #     print(nr_products)
    #     print(nr_dividers)
    #     print(costs)
    #     return -10
    # print(f'OOH NOOs: {oohnoos}')
    # print(f'Samples: {samples}')
    # print(f'counter={counter}')
    return total_cost - saved1

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

def read_input():
    nr_products, nr_dividers = [int(d) for d in input().split(' ')]
    costs = [int(c) for c in input().split(' ')]
    return nr_products, nr_dividers, costs

def randomizer():
    nr_products = random.randint(2500,2500)
    nr_dividers = random.randint(25, 25)
    costs = [random.randint(1, 4) for a in range(nr_products)]
    # print(f'nr_products: {nr_products}')
    # print(f'nr_dividers: {nr_dividers}')
    # print(costs)
    return nr_products, nr_dividers, costs

def saving_money_2c(c, u, l, s):  # s = saved_per_slice
    global results_list, remaining_sums, intermediate_sums

    # print(f"------------------ {l}")
    # print(f'start of call: {s} {intermediate_sums}')

    used_dividers = u
    current_best = 2
    current_saved = c
    last_div_location = l
    previous_div_location = 0
    prev_used_div = u  # to indicate how many slices there are till a starting point
    starting_point = l
    skip = False

    if last_div_location in intermediate_sums:
        lst = list(
            filter(lambda x: x[0] <= nr_dividers - used_dividers, intermediate_sums[last_div_location]))
        if len(lst) > 0:
            skip = True
            best = max(lst, key=lambda x: x[1])[1]
            print(f'LET"S RETRIEVE {best} from {intermediate_sums}')
            current_saved += best

    while used_dividers < nr_dividers - 1 and current_best > 0 and not skip:
        intermediate_sum = 0
        i = last_div_location
        while used_dividers < nr_dividers - 1 and i < nr_products - 1:
            intermediate_sum = roundsum(intermediate_sum, costs[i])
            print(f'{last_div_location} {i + 1}: {costs[last_div_location:i + 1]} {intermediate_sum} normal')
            if intermediate_sum >= current_best:
                current_saved += intermediate_sum
                s.append(current_saved)
                used_dividers += 1
                previous_div_location = last_div_location
                last_div_location = i + 1
                # if last_div_location in intermediate_sums:
                #     lst = list(
                #         filter(lambda x: x[0] <= nr_dividers - used_dividers, intermediate_sums[last_div_location]))
                #     if len(lst) > 0:
                #         skip = True
                #         best = max(lst, key=lambda x: x[1])[1]
                #         print(f'LET"S RETRIEVE {best}')
                #         current_saved += best
                #         break
                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2:
                    saving_money_2c(current_saved, used_dividers, last_div_location, s.copy())
                    # prev_used_div = used_dividers
                    # Rewind step:

                    dummy_sum = intermediate_sum
                    intermediate_sum = 0
                    for j in range(previous_div_location, last_div_location):
                        intermediate_sum = roundsum(intermediate_sum, costs[j])
                        print(
                             f'{previous_div_location} {j + 1}: {costs[previous_div_location:j + 1]} {intermediate_sum} rewind')
                        if intermediate_sum >= 1:
                            current_saved = current_saved - dummy_sum + intermediate_sum
                            s.pop()
                            s.append(current_saved)
                            last_div_location = j + 1
                            i = last_div_location - 1
                            intermediate_sum = 0
                            # weird case
                            if used_dividers >= nr_dividers - 1:
                                prev_used_div = used_dividers
                            break
                current_best = 2
                intermediate_sum = 0
                if used_dividers >= nr_dividers - 1:
                    break
            i += 1
        current_best -= 1

    div_placed = False

    max_saved = -4
    if not skip:
        if last_div_location not in remaining_sums:
            if last_div_location + 1 < nr_products:
                total_cost = sum(costs[last_div_location:])
                total_saved = roundsum(0, total_cost)
                max_saved = total_saved
                max_div_loc = last_div_location
                left_saved = 0
                if total_saved != 0:
                    for i in range(last_div_location + 1, nr_products):
                        left_saved = roundsum(left_saved, costs[i - 1])
                        right_saved = roundsum(total_saved, -left_saved)
                        combined_saved = left_saved + right_saved
                        if combined_saved > max_saved:
                            div_placed = True
                            max_saved = combined_saved
                            max_div_loc = i
                            if max_saved >= 4:
                                break
            else:
                max_saved = costs[last_div_location] - round5(costs[last_div_location])
            remaining_sums[last_div_location] = max_saved
        else:
            max_saved = remaining_sums[last_div_location]
    else:
        max_saved = 0
    results_list[current_saved + max_saved] = used_dividers  # we dont need to save anything special here, we just need the index

    if div_placed:
        # I don't think it matters what the integer is that we're appending s with here, 
        # because it only matters for div_used_from_starting_point (which is computed by looking at the length of s)
        s.append(1)
        used_dividers += 1

    # memoization
    if not skip:
        saved_till_starting_point = 0
        div_used_from_starting_point = used_dividers
        if starting_point > 0:
            index = prev_used_div - 1
            # print(f'index={index}: prev_used_div={prev_used_div} - used_div={used_dividers}')
            saved_till_starting_point = s[index]
            div_used_from_starting_point = len(s[index:]) - 1
            # print(f'div_used_from_starting_point={div_used_from_starting_point} = used_dividers={used_dividers} - rem={len(s[index:])}')
        saved_in_slice = current_saved + max_saved - saved_till_starting_point
        # print(f'current_saved={current_saved}: max_saved={max_saved} - saved_till_starting_point={saved_till_starting_point}')
        # print(f's:{s}')
        # print(f'lets save sp={starting_point} (u, s): {(div_used_from_starting_point, saved_in_slice)}')
        if starting_point in intermediate_sums:
            pass
            # intermediate_sums[starting_point].append((div_used_from_starting_point, saved_in_slice))
        else:
            pass
            # intermediate_sums[starting_point] = [(div_used_from_starting_point, saved_in_slice)]

def saving_money_2c_old(c, u, l, d, s):     # s = saved_per_slice
    global results_list, first_time, second_time, remaining_sums, intermediate_sums, counter
    
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
                        # print("memo")
                        best = max(lst, key=lambda x: x[1])[1] # 3 ... nr_products
                        current_saved += best                  # 0 ... 3
                        break
                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2:
                    counter += 1
                    saving_money_2c_old(current_saved, used_dividers, last_div_location, div_locs, s)
                    # Rewind step:
                    dummy_sum = intermediate_sum
                    intermediate_sum = 0
                    for j in range(previous_div_location, last_div_location):
                        intermediate_sum = roundsum(intermediate_sum, costs[j])
                        if intermediate_sum == 1:
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
    # mid = time.process_time()

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
    # saved_till_starting_point = 0
    # div_used_from_starting_point = 0
    # if starting_point > 0:
    #     index = div_locs.index(starting_point)
    #     saved_till_starting_point = s[index]
    #     div_used_from_starting_point = used_dividers - len(s[index:])
    # saved_in_slice = current_saved + max_saved - saved_till_starting_point
    # if starting_point in intermediate_sums:
    #     intermediate_sums[starting_point].append((div_used_from_starting_point, saved_in_slice))
    # else:
    #     intermediate_sums[starting_point] = [(div_used_from_starting_point, saved_in_slice)]
    # end = time.process_time()

    # print(f'memo for first part: intermediate sums = {intermediate_sums}')
    # print(f'memo for second part: resulting sums = {remaining_sums}')
    # print(f'results list = {results_list}')

    # 1 2 3 4 5 6 7 8 9
    # 1 | 1 | 3 4 5 6 | 7 8 9)
    # s = [1,2,4,5,7,8]
    # div_locs = [1,2,6]

def round5(x):
    return 5 * round(x / 5)

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

def append_savings(i, j, c, d):
    if (i, j) in savings:
        if c in savings[(i, j)]:
            if savings[(i, j)][c] > d:
                savings[(i, j)][c] = d
        else:
            savings[(i, j)][c] = d
    else:
        savings[(i, j)] = {c: d}

def rewrite_attempt(c, u, l, s):  # s = saved_per_slice
    global results_list, remaining_sums, intermediate_sums

    # print(f"------------------ {l}")
    # print(f'start of call: {s} {intermediate_sums}')

    used_dividers = u
    current_best = 2
    current_saved = c
    last_div_location = l
    previous_div_location = 0
    prev_used_div = u  # to indicate how many slices there are till a starting point
    starting_point = l
    skip = False

    rewind = False

    if last_div_location in intermediate_sums:
        lst = list(
            filter(lambda x: x[0] <= nr_dividers - used_dividers, intermediate_sums[last_div_location]))
        if len(lst) > 0:
            skip = True
            best = max(lst, key=lambda x: x[1])[1]
            use = max(lst, key=lambda x: x[1])[0]
            current_saved += best
            # print(f'LET"S RETRIEVE {best} from {intermediate_sums} current_saved={current_saved}')
            # print(f'MORE: current_saved={current_saved} ud={used_dividers} u={use}')

    while used_dividers < nr_dividers - 1 and current_best > 0 and not skip:
        intermediate_sum = 0
        i = last_div_location
        while used_dividers < nr_dividers - 1 and i < nr_products - 1:
            intermediate_sum = roundsum(intermediate_sum, costs[i])
            # print(f'{last_div_location} {i + 1}: {costs[last_div_location:i + 1]} {intermediate_sum} normal {current_best}')
            if intermediate_sum >= current_best:
                current_saved += intermediate_sum
                s.append(current_saved)
                used_dividers += 1
                previous_div_location = last_div_location
                last_div_location = i + 1
                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2 and not rewind:
                    # print("---recurse")
                    rewrite_attempt(current_saved, used_dividers, last_div_location, s.copy())
                    # Rewind step:
                    # print(f"---rewind {last_div_location} {previous_div_location}")
                    i = previous_div_location
                    last_div_location = i
                    current_saved -= intermediate_sum
                    intermediate_sum = 0
                    current_best = 1
                    s.pop()
                    used_dividers -= 1
                    rewind = True
                    continue
                rewind = False
                current_best = 2
                intermediate_sum = 0
                if used_dividers >= nr_dividers - 1:
                    break
            i += 1
        current_best -= 1

    div_placed = False

    max_saved = -4
    if not skip:
        if last_div_location not in remaining_sums:
        # if True:
            if last_div_location + 1 < nr_products:
                total_cost = sum(costs[last_div_location:])
                total_saved = roundsum(0, total_cost)
                max_saved = total_saved
                max_div_loc = last_div_location
                left_saved = 0
                if total_saved != 0:
                    for i in range(last_div_location + 1, nr_products):
                        left_saved = roundsum(left_saved, costs[i - 1])
                        right_saved = roundsum(total_saved, -left_saved)
                        combined_saved = left_saved + right_saved
                        if combined_saved > max_saved:
                            div_placed = True
                            max_saved = combined_saved
                            max_div_loc = i
                            if max_saved >= 4:
                                break
            else:
                max_saved = costs[last_div_location] - round5(costs[last_div_location])
            remaining_sums[last_div_location] = (max_saved, div_placed)
        else:
            (max_saved, place_div) = remaining_sums[last_div_location]
            if place_div:
                s.append(1)
                used_dividers += 1
    else:
        max_saved = 0
    results_list[current_saved + max_saved] = used_dividers  # we dont need to save anything special here, we just need the index

    if div_placed:
        # I don't think it matters what the integer is that we're appending s with here, 
        # because it only matters for div_used_from_starting_point (which is computed by looking at the length of s)
        s.append(1)
        used_dividers += 1

    # memoization
    if not skip:
        saved_till_starting_point = 0
        div_used_from_starting_point = used_dividers
        if starting_point > 0:
            index = prev_used_div - 1
            #     print(f"------------------------------------------------------------------------- {skip} {div_placed}")
            #     print(f'remainingsums = {remaining_sums[last_div_location]} last_div_loc={last_div_location} prev_div_loc={previous_div_location}')
            #     print(f'index={index}: prev_used_div={prev_used_div} - used_div={used_dividers}')
            saved_till_starting_point = s[index]
            div_used_from_starting_point = len(s[index:]) - 1
            #     print(f'div_used_from_starting_point={div_used_from_starting_point} = used_dividers={used_dividers} - rem={len(s[index:])}')
        saved_in_slice = current_saved + max_saved - saved_till_starting_point
        #     print(f'current_saved={current_saved}: max_saved={max_saved} - saved_till_starting_point={saved_till_starting_point}')
        #     print(f's:{s}')
        #     print(f'lets save sp={starting_point} (u, s): {(div_used_from_starting_point, saved_in_slice)}')
        if starting_point in intermediate_sums:
            # pass
            intermediate_sums[starting_point].append((div_used_from_starting_point, saved_in_slice))
        else:
            # pass
            intermediate_sums[starting_point] = [(div_used_from_starting_point, saved_in_slice)]

def rewrite_attempt2(c, u, l):
    global results_list, remaining_sums, intermediate_sums, max_result, stop_algorithm

    if stop_algorithm:
        return
    
    used_dividers = u
    current_best = 2
    current_saved = c
    last_div_location = l
    previous_div_location = 0
    skip = False
    rewind = False

    while used_dividers < nr_dividers - 1 and current_best > 0 and not skip:
        intermediate_sum = 0
        i = last_div_location
        while used_dividers < nr_dividers - 1 and i < nr_products - 1:
            intermediate_sum = roundsum(intermediate_sum, costs[i])
            # print(f'{last_div_location} {i + 1}: {costs[last_div_location:i + 1]} {intermediate_sum} normal {current_best}')
            if intermediate_sum >= current_best:
                current_saved += intermediate_sum
                used_dividers += 1
                previous_div_location = last_div_location
                last_div_location = i + 1
                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2 and not rewind:
                    rewrite_attempt2(current_saved, used_dividers, last_div_location)
                    # Rewind step:
                    i = previous_div_location
                    last_div_location = i
                    current_saved -= intermediate_sum
                    intermediate_sum = 0
                    current_best = 1
                    used_dividers -= 1
                    rewind = True
                    continue
                rewind = False
                current_best = 2
                intermediate_sum = 0
                if used_dividers >= nr_dividers - 1:
                    break
            i += 1
        current_best -= 1

    max_saved = -4
    if not skip:
        if last_div_location not in remaining_sums:
            if last_div_location + 1 < nr_products:
                total_cost = sum(costs[last_div_location:])
                total_saved = roundsum(0, total_cost)
                max_saved = total_saved
                left_saved = 0
                if total_saved != 0:
                    for i in range(last_div_location + 1, nr_products):
                        left_saved = roundsum(left_saved, costs[i - 1])
                        right_saved = roundsum(total_saved, -left_saved)
                        combined_saved = left_saved + right_saved
                        if combined_saved > max_saved:
                            max_saved = combined_saved
                            if max_saved >= 4:
                                break
            else:
                max_saved = costs[last_div_location] - round5(costs[last_div_location])
            remaining_sums[last_div_location] = max_saved
        else:
            max_saved = remaining_sums[last_div_location]
    else:
        max_saved = 0

    max_result = max(max_result, current_saved + max_saved)

    if max_result >= magic_number:
        stop_algorithm = True

def last_attempt(c, u, l):  # s = saved_per_slice
    global results_list, remaining_sums, intermediate_sums, max_result, stop_algorithm

    if stop_algorithm:
        # print("Let's call it a day")
        return
   
    if (l, c, u) in intermediate_sums:
        # print("We're done here")
        return

    used_dividers = u
    current_best = 2
    current_saved = c
    last_div_location = l
    previous_div_location = 0

    start_point = l
    saved_from_start = 0
    used_from_start = 0

    rewind = False

    while used_dividers < nr_dividers - 1 and current_best > 0:
        intermediate_sum = 0
        i = last_div_location
        while used_dividers < nr_dividers - 1 and i < nr_products - 1:
            intermediate_sum = roundsum(intermediate_sum, costs[i])
            # print(f'{last_div_location} {i + 1}: {costs[last_div_location:i + 1]} {intermediate_sum} normal {current_best}')
            if intermediate_sum >= current_best:
                current_saved += intermediate_sum
                saved_from_start += intermediate_sum
                used_dividers += 1
                used_from_start += 1
                previous_div_location = last_div_location
                last_div_location = i + 1

                if last_div_location - previous_div_location > 2 and intermediate_sum >= 2 and not rewind:
                    last_attempt(current_saved, used_dividers, last_div_location)
                    # Rewind
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
                if used_dividers >= nr_dividers - 1:
                    break
            i += 1
        current_best -= 1

    div_placed = False

    max_saved = -4
    if last_div_location not in remaining_sums:
        if last_div_location + 1 < nr_products:
            total_cost = sum(costs[last_div_location:])
            total_saved = roundsum(0, total_cost)
            max_saved = total_saved
            left_saved = 0
            if total_saved != 0:
                for i in range(last_div_location + 1, nr_products):
                    left_saved = roundsum(left_saved, costs[i - 1])
                    right_saved = roundsum(total_saved, -left_saved)
                    combined_saved = left_saved + right_saved
                    if combined_saved > max_saved:
                        div_placed = True
                        max_saved = combined_saved
                        if max_saved >= 4:
                            break
        else:
            max_saved = costs[last_div_location] - round5(costs[last_div_location])
        remaining_sums[last_div_location] = (max_saved, div_placed)
    else:
        (max_saved, place_div) = remaining_sums[last_div_location]
        if place_div:
            used_dividers += 1
            used_from_start += 1

    if div_placed:
        used_dividers += 1
        used_from_start += 1

    max_result = max(max_result, current_saved + max_saved)

    if max_result >= magic_number:
        stop_algorithm = True

    saved_from_start += max_saved
    current_saved += max_saved
    used_till_start = used_dividers - used_from_start
    saved_till_start = current_saved - saved_from_start
    add_to_intermediate_sums(start_point, saved_till_start, used_till_start)

def add_to_intermediate_sums(start_point, saved_till_start, used_till_start):
    intermediate_sums[(start_point, saved_till_start, used_till_start)] = True