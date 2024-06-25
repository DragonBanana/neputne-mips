import csv
import numpy as np
import requests
import pprint
import networkx as nx
import time
from datetime import datetime

from data.data_generation import DataGenerator
import data.graph_visualization as gv
from data.data_check import *
import json

# Generate the random data

# Load configuration from config.json
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

auto_generate = config["auto_generate"]
SEED = config["SEED"]
max_attempts = config["max_attempts"]
url = config["request"]["url"]



data_generator = DataGenerator(auto_generate=auto_generate, seed=SEED)

input_data, num_nodes, num_functions, num_tables = data_generator.generate_input_data(max_attempts=max_attempts)

gv.print_data(input_data)

start_time = time.time()
response = requests.request(method='get', url=url, json=input_data)
end_time = time.time()
response_time = end_time - start_time 
print(f"Response time: {response_time:.4f} seconds\n")

print("\nReply received!")
print("")

response_data = response.json()
# gv.draw_network(response_data)

graph = gv.create_graph_from_data(input_data)

#gv.draw_topology_graph(input_data, graph)

gv.draw_migrations_graph(response_data)
gv.draw_function_dep_graph(response_data)

# Write results
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
objective_value = response_time


output_file = 'optimization_results.csv'
with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                        response_data["score"], 
                        response_time, 
                        response_data["status"],
                        num_nodes,
                        num_functions,
                        num_tables,
                        SEED

                    ])


# TODO: riconsiderare i costi


# TODO: richiesta costa un tot, inoltrare richiesta può pesare
