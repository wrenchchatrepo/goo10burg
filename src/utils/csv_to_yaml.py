import csv
import os
import sys
import subprocess
import json

def csv_to_yaml(csv_file_path):
    """
    Converts a CSV file to a YAML file.

    Args:
        csv_file_path (str): The path to the CSV file.
    """
    yaml_file_path = os.path.splitext(csv_file_path)[0] + ".yaml"
    data = []
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    
    try:
        # Attempt to use the system's pyyaml if available
        import yaml
        with open(yaml_file_path, 'w') as yamlfile:
            yaml.dump(data, yamlfile, indent=2)
    except ImportError:
        # If pyyaml is not available, use a subprocess to run a python script with pyyaml
        print("pyyaml not found, using subprocess")
        script_content = """
import yaml
import sys
import json
data = json.loads(sys.argv[1])
with open(sys.argv[2], 'w') as yamlfile:
    yaml.dump(data, yamlfile, indent=2)
"""
        process = subprocess.Popen([sys.executable, '-c', script_content, json.dumps(data), yaml_file_path], executable=sys.executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Error during subprocess execution: {stderr.decode()}")
        if stdout:
            print(f"Subprocess output: {stdout.decode()}")

if __name__ == '__main__':
    # Example usage:
    csv_file = "/Users/dionedge/dev/goo10burg/tests/image.csv"
    csv_to_yaml(csv_file)
    csv_file = "/Users/dionedge/dev/goo10burg/tests/markdown.csv"
    csv_to_yaml(csv_file)
    csv_file = "/Users/dionedge/dev/goo10burg/tests/package.csv"
    csv_to_yaml(csv_file)
    csv_file = "/Users/dionedge/dev/goo10burg/tests/script.csv"
    csv_to_yaml(csv_file)
