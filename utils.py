import math
import copy
from typing import List


class Utils:
    @staticmethod
    def generate_random_route_list(depo, vehicle, customer_list, cToc_distance):
        customer_list = customer_list[1:]  # removing depo
        route_list = []
        unrouted_customer_list = customer_list[:]
        idx=0
        while unrouted_customer_list:
            current_route_customer_list = [Utils.depo_as_customer(depo), Utils.depo_as_customer(depo)]
            current_route_customer_index = 1
            feasible = False

            for unrouted_customer in unrouted_customer_list:
                current_route_customer_list.insert(current_route_customer_index, unrouted_customer)
                feasible = Utils.check_capacity_constraint(current_route_customer_list, vehicle.capacity) and \
                           Utils.check_time_constraint(current_route_customer_list, cToc_distance)
                if feasible:
                    unrouted_customer_list.remove(unrouted_customer)
                    current_route_customer_index += 1
                    idx+=1
                else:
                    current_route_customer_list.pop(current_route_customer_index)

            route_list.append(current_route_customer_list)
            

        return route_list

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def check_time_constraint(customer_list, cToc_distance):
        arrival_time = 0
        previous_customer = None

        for customer in customer_list:
            if previous_customer is not None:
                arrival_time += previous_customer.serviceTime
                arrival_time += cToc_distance[previous_customer.id][customer.id]
            if arrival_time <= customer.timeWindow_start:
                arrival_time = customer.timeWindow_start
            if arrival_time > customer.timeWindow_end:
                return False
            previous_customer = customer
        return True

    @staticmethod
    def check_capacity_constraint(customer_list, capacity):
        curr_capacity = 0

        for customer in customer_list:
            curr_capacity += customer.demand
            
            if curr_capacity > capacity:
                return False

        return True

    @staticmethod
    def calculate_total_distance(customer_list, cToc_distance):
        total_distance = 0
        previous_customer = None

        for customer in customer_list:
            if previous_customer is not None:
                total_distance += cToc_distance[previous_customer.id][customer.id]
            previous_customer = customer

        return total_distance

    @staticmethod
    def calculate_total_distance_of_all_route(route_list, cToc_distance):
        total_distance = 0

        for route in route_list:
            total_distance += Utils.calculate_total_distance(route, cToc_distance)

        return total_distance

    @staticmethod
    def calculate_total_route_time(customer_list, cToc_distance):
        curr_time = 0
        previous_customer = None

        for customer in customer_list:
            if previous_customer is not None:
                curr_time += cToc_distance[previous_customer.id][customer.id]
            if curr_time < customer.timeWindow_start:
                curr_time = customer.timeWindow_start
            curr_time += customer.serviceTime
            previous_customer = customer

        return curr_time

    @staticmethod
    def depo_as_customer(depo):
        return copy.deepcopy(depo)

    @staticmethod
    def print_route_list(route_list, cToc_distance):
        used_vehicle_count = sum(1 for route in route_list if len(route) >= 3)
        print(f"Total Vehicle used {used_vehicle_count} out of {len(route_list)}")

        total_distance = 0
        for i, route in enumerate(route_list):
            print(f"Total Distance of Route {i}: {Utils.calculate_total_distance(route, cToc_distance)}")
            total_distance += Utils.calculate_total_distance(route, cToc_distance)
            print(" ".join(str(customer.id) for customer in route))

        print(f"Total Distance Of All Routes: {total_distance}")

    @staticmethod
    def print_total_distance(route_list, cToc_distance):
        total_distance = Utils.calculate_total_distance_of_all_route(route_list, cToc_distance)
        print(f"Total Distance Of All Routes: {total_distance}")

    @staticmethod
    def copy_list_of_list(list_from, list_to):
        for route in list_from:
            new_customer_list = [copy.deepcopy(customer) for customer in route]
            list_to.append(new_customer_list)
