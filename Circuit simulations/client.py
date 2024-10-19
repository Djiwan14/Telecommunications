import sys
import json
import os


def load_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Failed to load JSON from {file_path}")
        sys.exit(1)


def find_available_circuit(circuits, links, start, end, demand):
    for circuit in circuits:
        if circuit[0] == start and circuit[-1] == end:
            if all(links.get((circuit[i], circuit[i + 1]), 0) >= demand for i in range(len(circuit) - 1)):
                return circuit
    return None


def book_resources(path, links, demand):
    for i in range(len(path) - 1):
        link = (path[i], path[i + 1])
        links[link] -= demand


def release_resources(path, links, demand):
    for i in range(len(path) - 1):
        link = (path[i], path[i + 1])
        links[link] += demand



def simulate(simulation, circuits, links):
    events = simulation['demands']
    reservations = {}
    event_number = 1  # Track the event count for output formatting

    for time in range(simulation['duration'] + 1):
        for event in events:


            if event['start-time'] == time:
                path = find_available_circuit(circuits, links, event['end-points'][0], event['end-points'][1], event['demand'])
                if path:
                    book_resources(path, links, event['demand'])
                    reservations[(event['end-points'][0], event['end-points'][1])] = path
                    print(f"{event_number}. demand allocation: {event['end-points'][0]}<->{event['end-points'][1]} st:{time} – successful")
                else:
                    print(f"{event_number}. demand allocation: {event['end-points'][0]}<->{event['end-points'][1]} st:{time} – unsuccessful")
                event_number += 1


            if event['end-time'] == time:
                if (event['end-points'][0], event['end-points'][1]) in reservations:
                    path = reservations[(event['end-points'][0], event['end-points'][1])]
                    release_resources(path, links, event['demand'])
                    print(f"{event_number}. demand deallocation: {event['end-points'][0]}<->{event['end-points'][1]} st:{time}")
                    del reservations[(event['end-points'][0], event['end-points'][1])]
                    event_number += 1



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 client.py <path_to_json_file>")
        sys.exit(1)

    json_file = sys.argv[1]

    if not os.path.isfile(json_file):
        print(f"Error: {json_file} does not exist in the current directory.")
        sys.exit(1)

    data = load_json_from_file(json_file)

    links = {tuple(link['points']): link['capacity'] for link in data['links']}

    simulate(data['simulation'], data['possible-circuits'], links)
