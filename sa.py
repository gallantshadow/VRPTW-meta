'''
VRPTW cs633 project
author: Bhavdeep Khileri(bk2281), Jay Nair(an1147), Sanish Suwal (ss4657)
'''
import math
import random
from typing import List
from copy import copy
from utils import Utils


class SimulatedAnnealing:
    def __init__(self, depo, vehicle, customer_list, cToc_distance):
        self.no_of_customer = len(customer_list)
        self.depo = depo
        self.vehicle = vehicle
        self.customer_list = customer_list
        self.cToc_distance = cToc_distance

    def run(self, initial_temp, final_temp, cooling_factor, no_of_iteration, filename):
        i=0
        route_list = Utils.generate_random_route_list(self.depo, self.vehicle, self.customer_list, self.cToc_distance)
        #Utils.print_route_list(route_list, self.cToc_distance)
        Utils.plot_customers_and_routes(self.customer_list, route_list,filename+"{i}.png".format(i=i))
        best_route_list = [copy(i) for i in route_list]
        curr_route_list = [copy(i) for i in route_list]
        print(best_route_list)
        neighbour_route_list = [copy(i) for i in route_list]
        cost_of_best_route_list = Utils.calculate_total_distance_of_all_route(best_route_list, self.cToc_distance)
        cost_of_curr_route_list = Utils.calculate_total_distance_of_all_route(curr_route_list, self.cToc_distance)
        curr_temp = initial_temp
        counter =0
        while curr_temp > final_temp:
            print(curr_temp, counter)
            iteration = 0
            while iteration < no_of_iteration:
                neighbour_route_list = self.get_neighbour(curr_route_list)
                cost_of_neighbour_route_list = Utils.calculate_total_distance_of_all_route(neighbour_route_list,
                                                                                            self.cToc_distance)

                # print("BestRouteDis: ", Utils.calculate_total_distance_of_all_route(best_route_list,
                #                                                                      self.cToc_distance),
                #       " currRouteDis: ", Utils.calculate_total_distance_of_all_route(curr_route_list,
                #                                                                       self.cToc_distance),
                #       " temp: ", curr_temp)

                cost_diff = cost_of_neighbour_route_list - cost_of_curr_route_list
                if cost_diff < 0 or math.exp(-cost_diff / curr_temp) > random.uniform(0, 1):
                    curr_route_list = [copy(i) for i in neighbour_route_list]
                    cost_of_curr_route_list = cost_of_neighbour_route_list

                    if cost_of_curr_route_list < cost_of_best_route_list:
                        best_route_list = [copy(i) for i in curr_route_list]
                        cost_of_best_route_list = cost_of_curr_route_list
                        i+=1
                        Utils.plot_customers_and_routes(self.customer_list, best_route_list,filename+"{i}.png".format(i=i))

                iteration += 1
                counter +=1
            curr_temp *= cooling_factor
        i+=1
        Utils.plot_customers_and_routes(self.customer_list, best_route_list,filename+"{i}.png".format(i=i))
        Utils.print_route_list(best_route_list, self.cToc_distance)
        return Utils.return_route_list(best_route_list, self.cToc_distance)

    def get_neighbour(self, route_list):
        rand = random.randint(1, 3)

        if rand == 1:
            return self.mutate_insertion(route_list)
        elif rand == 2:
            return self.mutate_swap(route_list)
        elif rand == 3:
            return self.mutate_inversion(route_list)

    def mutate_insertion(self, route_list):
        neighbour_route_list = [copy(i) for i in route_list]
        random_route_index = random.randint(0, len(neighbour_route_list) - 1)
        random_route = neighbour_route_list[random_route_index]

        if len(random_route) >= 3:
            random_customer_index = random.randint(1, len(random_route) - 2)
            customer = random_route.pop(random_customer_index)

            for route in neighbour_route_list:
                for index in range(1, len(route)):
                    route.insert(index, customer)
                    feasible = Utils.check_time_constraint(route, self.cToc_distance) and \
                               Utils.check_capacity_constraint(route, self.vehicle.capacity)
                    if feasible:
                        return neighbour_route_list
                    else:
                        route.pop(index)
            random_route.insert(random_customer_index, customer)

        return neighbour_route_list

    def mutate_swap(self, route_list):
        neighbour_route_list = [route[:] for route in route_list]

        first_route_index = random.randint(0, len(neighbour_route_list) - 1)
        second_route_index = random.randint(0, len(neighbour_route_list) - 1)
        first_route = neighbour_route_list[first_route_index]
        second_route = neighbour_route_list[second_route_index]

        if first_route_index == second_route_index or len(first_route) <= 2 or len(second_route) <= 2:
            return neighbour_route_list

        first_route_customer_index = random.randint(1, len(first_route) - 2)
        second_route_customer_index = random.randint(1, len(second_route) - 2)
        first_route[first_route_customer_index], second_route[second_route_customer_index] = second_route[second_route_customer_index], first_route[first_route_customer_index]
      
        feasible = Utils.check_time_constraint(first_route,self.cToc_distance) and Utils.check_capacity_constraint(first_route,self.vehicle.capacity) and Utils.check_time_constraint(second_route,self.cToc_distance) and Utils.check_capacity_constraint(second_route,self.vehicle.capacity)

        if not feasible:
            first_route[first_route_customer_index], second_route[second_route_customer_index] = second_route[second_route_customer_index], first_route[first_route_customer_index]

        # print("mutateSwap", feasible)
        return neighbour_route_list

    def mutate_inversion(self,route_list):
        neighbour_route_list = [route[:] for route in route_list]

        route_index = random.randint(0, len(neighbour_route_list) - 1)
        route = neighbour_route_list[route_index]

        if len(route) <= 3:
            return neighbour_route_list

        customer_start = random.randint(1, len(route) - 3)
        count = random.randint(2, len(route) - customer_start - 1)

        route[customer_start:customer_start + count] = reversed(route[customer_start:customer_start + count])

        feasible = Utils.check_time_constraint(route,self.cToc_distance) and Utils.check_capacity_constraint(route,self.vehicle.capacity)

        if not feasible:
            route[customer_start:customer_start + count] = reversed(route[customer_start:customer_start + count])

        # print("mutateInversion", feasible)
        return neighbour_route_list
