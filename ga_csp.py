import random
import numpy as np
import time
import copy
import math

# stocks = [4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500]
# stock_price = [86, 85, 83, 79, 68, 66, 64, 63]
# order_len = [2350, 2250, 2200, 2100, 2050, 2000, 1950, 1900, 1850, 1700, 1650, 1350, 1300, 1250, 1200, 1150, 1100, 1050]
# order_q = [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3]

# stocks = [10,13,15]
# stock_price = [100,130,150]
# order_len = [3,4,5,6,7,8,9,10]
# order_q = [5,2,1,2,4,2,1,3]

stocks = [50,80,100]
stock_price = [100,175,250]
order_len = [20,25,30]
order_q = [5,7,5]



def random_solution(order_lengths, order_q, n_stocks):
    solution = np.zeros(shape=(len(order_lengths), n_stocks))
    for index, order_len in enumerate(order_lengths):
        quantity = order_q[index]
        quantity_left  = quantity
        activity = np.zeros(shape=(n_stocks))
        # print(activity)
        for i in range(n_stocks):
            random_q = random.randint(0,quantity_left)
            if sum(activity) == quantity:
                break
            if(i == n_stocks-1):
                activity[i] = quantity_left
                break
            activity[i] = random_q
            quantity_left -= random_q
        solution[index] = activity
    return solution
            
def evaluate_csp_old(solution, stocks, stock_price, order_len):
    sol_by_stock_len = np.transpose(solution)
    cost = np.zeros(shape= sol_by_stock_len.shape[0])
    for index, stock_len in enumerate(sol_by_stock_len):
        # Calculate the total length of stock needed for each order length
        total_stock_order = stock_len * order_len
        # Calculate the number of stock lengths needed in total for all order lengths, and then multiply that by the stock price.
        total_stock_len_price = math.ceil(sum(total_stock_order) / stocks[index]) * stock_price[index]
        cost[index] = total_stock_len_price
    return sum(cost)

def evaluate_csp(activities_all, stocks, stock_price, order_len):
    # activities
    # for each stock get the value from activities using stock as key such as activities.get(stocks[0]) -> activities for L50
    # len of activities list for each stock is the number of stock lengths needed, multiply that by cost to get total cost for each stock
    # add up all the costs
    stock_price_dict = dict(zip(stocks, stock_price))
    cost = 0
    for key in activities_all:
        activities = activities_all[key]
        cost += len(activities) * stock_price_dict[key]
    return cost

def solution_to_activities(solution, stocks, stock_price, order_len, order_q):
    sol = np.transpose(solution).astype(int)
    dict1 = {}
    for i, stock in enumerate(stocks):
        my_list = []
        for j, order in enumerate(order_len):
            my_list.extend([order] * sol[i][j])
        my_list.reverse()
        dict1[stock] = my_list
    
    # print(dict1, '\n')
    dict2 = {}

    for stock in stocks:
        orders = dict1[stock]
        if len(orders) == 0:
            continue
        activities = [[]]
        index = 0
        while len(orders) > 0:
            order = orders[index]
            # If the current order len + last activity's sum is exactly equal to stock then 
            # it means that I should stop iterating thorugh the orders to check for another order len to add.
            # It also means that I can add en empty activity so that next iteration I don't have to check that same activity again.
            if sum(activities[-1]) + order == stock:
                activities[-1].append(order)
                orders.remove(orders[index])
                activity = []
                if len(orders) > 0:
                    activities.append(activity)
                index = 0
                continue
            # I know that current order + sum of last activity is not equal to stock length, so check if it's
            # less thank stock length, this means that more orders can be added.
            if sum(activities[-1]) + order < stock:
                activities[-1].append(order)
                orders.remove(orders[index])
                index = 0
                continue
            # The current order len doesn't add up to exactly the stock len and goes over the stock length if added to activity
            else: # sum of last activity + order > stock
                # Continue checking next order len if there's still orders left that maybe could fit until the end of the list
                if index != (len(orders)-1):
                    index += 1
                    continue # This doens't work because it doesn't add the original order to a new activity but the one on the current iteration. I need to find a way to remember what the original length was 
                else:
                    # Have gone through the entire list without a valid order to add, so add the first order from which I started
                    activity = [orders[0]]
                    orders.remove(orders[0])
                    activities.append(activity)
                    index = 0
                    continue
        dict2[stock] = activities
    # print(dict2)
    return dict2

def random_csp(stocks, stock_price, order_len, order_q, time_limit):
    end_time = time.time() + time_limit
    best_sol = []
    best_sol_cost = float('inf')
    iterations = 0
    while time.time() < end_time: 
        # Old evaluate csp based cost calculation
        # solution = random_solution(order_len,order_q, len(stocks))      
        # cost = evaluate_csp_old(solution, stocks, stock_price, order_len)
        
        solution = random_solution(order_len,order_q, len(stocks))
        activities = solution_to_activities(solution, stocks,stock_price, order_len, order_q )
        cost = evaluate_csp(activities, stocks, stock_price, order_len)
        # If the cost is lower than best cost then make s1 the best sol
        if(cost < best_sol_cost):
            best_sol = solution
            best_sol_cost = cost
        iterations += 1
    print(f'Iterations : {iterations}')
    return best_sol, best_sol_cost

def generate_random_population(size, stocks, order_len, order_q):
    population = []
    for _ in range(size):
        population.append(random_solution(order_len,order_q,len(stocks)))
    return np.array(population)

def mutation(solution):
    solution = np.array(solution)
    for row in solution:
        # Decreasing random positive element by 1
        indeces = np.where((row > 0))[0]
        i = np.random.choice(indeces)
        print(f'index of element getting decremented: {i}')
        row[i] -= 1

        # Increasing random element that is not i by 1
        indeces = np.where((row != row[i]))[0]
        j = np.random.choice(indeces)
        print(f'index of element getting incremented: {j}\n')
        row[j] += 1
    return solution

def tournament_selection(popoulation, pop_size):
    
    
    print('test')



#region Testing

# test = random_csp(stocks, stock_price, order_len, order_q, 2)
# print(f'Cost: {test[1]}')

# sol = random_solution(order_len,order_q,len(stocks))
# print(sol)

# population = generate_random_population(10, stocks, order_len, order_q)
# print(population)

# mutated = mutation(sol)
# print(mutated)
# make Mutation
# row = np.array([0,0,7,0,2,3,0,0,1])
# print(f'Row before mutation:{row}')
# q = 5
# # Pick an operation to perform on a random element such as +4, no need to include negative elements since the same valued be 
# # subtracted from another element
# # operations = np.arange(1,row.max()+1) 
# # operation = np.random.choice(operations)
# # # print(operations)
# # print(f'Operation to perform: +{operation}')

# indeces = np.arange(0,len(row))
# # indeces = np.arange(3)
# # valid_pick = False
# # while not valid_pick:
# #     i = np.random.choice(indeces)
# #     if row[i] != 0: valid_pick = True

# i = np.random.choice(indeces)
# # print(indeces)
# print(f'index of element getting incremented: {i}')
# # print(f'indeces before removal: {indeces}')
# # Increasing random element by 1
# row[i] += 1

# # Decreasing random element by 1
# indeces = np.where((row > 0) & (indeces != i))[0]
# # indeces = np.delete(indeces, np.where(indeces == i)) # the index whose value is equal to i, simply writing i produces errors since the index might not match with the value
# # print(f'Indeces to choose from to decrease by 1: {indeces}')
# i = np.random.choice(indeces)
# print(f'index of element getting decremented: {i}')
# row[i] -= 1
# print(f'Row after mutation: {row}')

# make crossover

# make parent selection

#####################

# random.seed(1)
# solution = random_solution(order_len,order_q, len(stocks))
# activities = solution_to_activities(solution, stocks,stock_price, order_len, order_q )
# cost = evaluate_csp(activities, stocks, stock_price, order_len)
# print(solution)
# print(activities)
# print(cost)

# dict1 = {50: [30, 20, 20, 20, 20, 20], 80: [30,30,30,25,25,25,25,20,20], 100: [30, 30, 30, 25, 25, 25]}
# # print(dict1)
# dict2 = {}
# for stock in stocks:
#     # print(dict1[stock])
#     orders = dict1[stock]
#     activities = [[]]
#     index = 0
#     while len(orders) > 0:
#         order = orders[index]
#         # If the current order len + last activity's sum is exactly equal to stock then 
#         # it means that I should stop iterating thorugh the orders to check for another order len to add.
#         # It also means that I can add en empty activity so that next iteration I don't have to check that same activity again.
#         if sum(activities[-1]) + order == stock:
#             activities[-1].append(order)
#             orders.remove(order)
#             activity = []
#             activities.append(activity)
#             index = 0
#             continue
#         # I know that current order + sum of last activity is not equal to stock length, so check if it's
#         # less thank stock length, this means that more orders can be added.
#         if sum(activities[-1]) + order < stock:
#             activities[-1].append(order)
#             orders.remove(order)
#             index = 0
#             continue
#         # The current order len doesn't add up to exactly the stock len and goes over the stock length if added to activity
#         else: # sum of last activity + order > stock
#             # Continue checking next order len if there's still orders left that maybe could fit until the end of the list
#             if index != (len(orders)-1):
#                 index += 1
#                 continue # This doens't work because it doesn't add the original order to a new activity but the one on the current iteration. I need to find a way to remember what the original length was 
#             else:
#                 activity = [orders[0]]
#                 orders.remove(order)
#                 activities.append(activity)
#                 index = 0
#                 continue
        
#     dict2[stock] = activities

# print(dict2)
            

# my_dict = {}
# stock_len = [50,80,100]
# order_len = [20,25,30]
# sol = [[1,2,1], [2,4,3], [2,1,1]]

# for i, stock in enumerate(stock_len):
#     my_list = []
#     for j, order in enumerate(order_len):
#         my_list.extend([order] * sol[i][j])
#     my_dict[stock] = my_list
# print(my_dict)

# my_list = []
# my_list.extend([25] *3 + [30] * 4)
# my_list.reverse()
# print(my_list)

# l50 = np.transpose(s1)[0]
# total_stock_order = l50 * order_len
# total_stock_len_l50_price = math.ceil(sum(total_stock_order)/stocks[0])*stock_price[0]
# print(l50)
# print(f'Stock times order len: {total_stock_order}')
# print(f'Total stock price for L-50: {total_stock_len_l50_price}')
#endregion
