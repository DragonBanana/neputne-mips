import json
from data_generation import DataGenerator
import data_graph_visualization as gv
from data_check import *
import json

EXPORT_PATH = 'output.json'

# Load configuration from config.json
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

auto_generate = config["auto_generate"]
SEED = config["SEED"]
max_attempts = config["max_attempts"]
url = config["request"]["url"]



data_generator = DataGenerator(auto_generate=auto_generate, seed=SEED)

input_data, num_nodes, num_functions, num_tables = data_generator.generate_input_data(max_attempts=max_attempts)

remove_keys = { 'write_per_req_matrix', 'table_sizes', 'table_names', 'v_old_matrix', 'solver', 'with_db', 'read_per_req_matrix', 'r_ft_matrix', 'node_storage' }

input_data = { k:v for k,v in input_data.items() if k not in remove_keys and 'gpu' not in k}


with open(EXPORT_PATH, 'w') as f:
    json.dump(input_data, f, sort_keys=True, indent=4)