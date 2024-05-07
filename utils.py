'''
VRPTW cs633 project
author: Bhavdeep Khileri(bk2281), Jay Nair(an1147), Sanish Suwal (ss4657)
'''
import math
import copy
from typing import List
import matplotlib.pyplot as plt
import os

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
    def return_route_list(route_list, cToc_distance):
        used_vehicle_count = sum(1 for route in route_list if len(route) >= 3)

        total_distance = 0
        for i, route in enumerate(route_list):
            total_distance += Utils.calculate_total_distance(route, cToc_distance)

        return used_vehicle_count, total_distance

    @staticmethod
    def print_total_distance(route_list, cToc_distance):
        total_distance = Utils.calculate_total_distance_of_all_route(route_list, cToc_distance)
        print(f"Total Distance Of All Routes: {total_distance}")

    @staticmethod
    def copy_list_of_list(list_from, list_to):
        for route in list_from:
            new_customer_list = [copy.deepcopy(customer) for customer in route]
            list_to.append(new_customer_list)
    
    @staticmethod
    def plot_customers_and_routes(customers, routes, filename):
        routes = [route for route in routes if len(route) >= 3]
        colors = [
    'red', 'blue', 'green', 'purple', 'orange', 'yellow', 'cyan', 'magenta', 'lime', 'pink',
    'teal', 'lavender', 'brown', 'beige', 'maroon', 'turquoise', 'olive', 'hotpink', 'navy', 'grey',
    'black', 'white', 'crimson', 'turquoise', 'indigo', 'silver', 'gold', 'violet', 'tan', 'rosybrown']
        # Extract customer coordinates
        x_coords = [customer.x_coordinate for customer in customers]
        y_coords = [customer.y_coordinate for customer in customers]

        # Plot customers
        plt.scatter(x_coords, y_coords, color='blue')

        # Plot depot
        depot_x = routes[0][0].x_coordinate  # First route, first customer
        depot_y = routes[0][0].y_coordinate
        # Plot routes
        for i, route in enumerate(routes):
            route_x = [depot_x] + [customer.x_coordinate for customer in route] + [depot_x]
            route_y = [depot_y] + [customer.y_coordinate for customer in route] + [depot_y]
            plt.plot(route_x, route_y, marker='o', color=colors[i])

        plt.scatter(depot_x, depot_y, color='turquoise', label='Depot',zorder=100)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Customer Locations and Routes')
        plt.legend()
        plt.grid(True)
        # Extract directory name from filename
        directory_name = filename.split('.')[0]
        assets_directory = os.path.join('assets', directory_name)
        # Create directory if it doesn't exist
        os.makedirs(assets_directory, exist_ok=True)
        # Save plot image
        plt.savefig(os.path.join(assets_directory+"/"+filename))
        plt.cla()
        plt.close()
