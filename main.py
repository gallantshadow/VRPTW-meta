'''
VRPTW cs633 project
author: Bhavdeep Khileri(bk2281), Jay Nair(an1147), Sanish Suwal (ss4657)
'''
import os
from customer import Customer
from depo import Depo
from sa import SimulatedAnnealing
from utils import Utils
from vehicle import Vehicle
from trials import main as trails

def main(filepath="./solomon-100/In/",filename="c201.txt"):
    depo = Depo()
    vehicle = Vehicle()
    customer_list = []

    vehicle.id = 0
    vehicle.capacity = None
    is_depo = True
    customer_id = 0
    idx =0
    # Getting customer data from data.txt which contains data from Solomon's dataset
    # URL for Solomon's dataset: http://web.cba.neu.edu/~msolomon/r101.htm
    with open(filepath+filename, "r") as file:
        for line in file:
            if idx == 4:
                data = line.strip().split()
                vehicle.capacity = int(data[1])
                print(vehicle.capacity)
            if idx <= 8:
                idx+=1
                continue

            data = line.strip().split()
            if is_depo:
                depo.id = customer_id
                depo.x_coordinate = float(data[1])
                depo.y_coordinate = float(data[2])
                depo.demand = float(data[3])
                depo.timeWindow_start = float(data[4])
                depo.timeWindow_end = float(data[5])
                depo.serviceTime = float(data[6])
                is_depo = False
            else:
                customer = Customer()
                customer.id = customer_id
                customer.x_coordinate = float(data[1])
                customer.y_coordinate = float(data[2])
                customer.demand = float(data[3])
                customer.timeWindow_start = float(data[4])
                customer.timeWindow_end = float(data[5])
                customer.serviceTime = float(data[6])
                customer_list.append(customer)
            customer_id += 1

    # Inserting depo as customer at beginning
    customer_list.insert(0, Utils.depo_as_customer(depo))

    # Calculating customer-to-customer distance (0 index represents depo)
    no_of_customer = len(customer_list)
    c_to_c_distance = [[0] * no_of_customer for _ in range(no_of_customer)]
    for i in range(no_of_customer):
        for j in range(no_of_customer):
            c_to_c_distance[i][j] = Utils.calculate_distance(
                customer_list[i].x_coordinate,
                customer_list[i].y_coordinate,
                customer_list[j].x_coordinate,
                customer_list[j].y_coordinate,
            )
    # Calling Simulated Annealing
    simulated_annealing = SimulatedAnnealing(depo, vehicle, customer_list, c_to_c_distance)
    print(simulated_annealing.run(100, 1, 0.98, 50000, filename)) #use this pypy3 it will take 1 minute for 50000 iteration
    # print(simulated_annealing.run(100, 1, 0.98, 6000, filename)) #use 6000 iteration if you dont have pypy3 installed

if __name__ == "__main__":
    trails(main) #trails take 7 hours to run over 56 files
    #main()
