'''
VRPTW cs633 project
author: Bhavdeep Khileri(bk2281), Jay Nair(an1147), Sanish Suwal (ss4657)
'''
import os
import statistics
import concurrent.futures
import csv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='output.log', level=logging.INFO)

def get_file_names(folder_path):
    file_names = []
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate through all files in the folder
        for file_name in os.listdir(folder_path):
            # Check if the path is a file (not a folder)
            if os.path.isfile(os.path.join(folder_path, file_name)):
                file_names.append(file_name)
    else:
        print("Folder doesn't exist.")
    return file_names

def trial_function(file_name, function, folder_path, trials):
    logging.info('Trial started for %s', file_name)
    vehicles = []
    distances = []
    for _ in range(trials):
        vehicles_used, total_distance = function(folder_path, file_name)
        vehicles.append(vehicles_used)
        distances.append(total_distance)
    vehicles_used_mean = statistics.mean(vehicles)
    vehicles_used_std = statistics.stdev(vehicles)
    distance_mean = statistics.mean(distances)
    distance_std = statistics.stdev(distances)
    logging.info("Trial ended for %s", file_name)
    logging.info("Trail result for %s: %s %s %s %s", file_name, vehicles_used_mean, vehicles_used_std, distance_mean, distance_std)
    return file_name, vehicles_used_mean, vehicles_used_std, distance_mean, distance_std

def run_trials(function, trials=30):
    folder_path = "./solomon-100/In/"
    file_names = get_file_names(folder_path)  # Example file names for testing
    file_names.sort()

    results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_results = [executor.submit(trial_function, file_name, function, folder_path, trials) for file_name in file_names]
        for future in concurrent.futures.as_completed(future_results):
            results.append(future.result())

    return results

def write_to_csv(results, filename='results.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'Vehicles Used Mean', 'Vehicles Used StdDev', 'Distance Mean', 'Distance StdDev'])
        writer.writerows(results)

def main(function):
    results = run_trials(function)
    write_to_csv(results)