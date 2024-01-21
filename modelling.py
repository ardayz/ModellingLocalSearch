import random
import math
import time

# Function to read the files and return the data as a list of floats
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split() for line in file.readlines()]
    return [float(item) for sublist in data for item in sublist]

# Euclidean distance function
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Initial solution generator
def generate_initial_solution(x, y, p):
    candidates = list(zip(x, y))
    return random.sample(candidates, p)

# Evaluation function
def evaluate_solution(solution, x, y, dem):
    total_distance = 0
    for i in range(len(x)):
        min_distance = float('inf')
        for facility in solution:
            dist = euclidean_distance(x[i], y[i], facility[0], facility[1])
            if dist < min_distance:
                min_distance = dist
        total_distance += min_distance * dem[i]
    return total_distance

# Main local search function
def local_search(x, y, dem, p, max_iterations=10000):
    start_time = time.time()
    s = generate_initial_solution(x, y, p)
    best_solution = s
    best_evaluation = evaluate_solution(s, x, y, dem)
    
    for iteration in range(max_iterations):
        s_new = s.copy()
        facility_to_replace = random.choice(s_new)
        new_facility = (random.choice(x), random.choice(y))
        s_new.remove(facility_to_replace)
        s_new.append(new_facility)
        current_evaluation = evaluate_solution(s_new, x, y, dem)
        if current_evaluation < best_evaluation:
            best_solution = s_new
            best_evaluation = current_evaluation
        if iteration % 1000 == 0:
            print(f"Iteration: {iteration}, Best Evaluation: {best_evaluation}")
        if time.time() - start_time > 60:
            print("Stopping early due to time constraint.")
            break

    end_time = time.time()
    print(f"Completed local search in {end_time - start_time:.2f} seconds for p={p}.")
    print(f"Total iterations: {iteration}")
    print(f"Best solution found for p={p}: {best_solution}")
    print(f"Best solution evaluation for p={p}: {best_evaluation}")
    return best_solution, best_evaluation

# Load the data for eil51 and eil76 instances
x51, y51, dem51 = load_data('ModellingLocalSearch\data\dem51.txt'), load_data('ModellingLocalSearch\data\y51.txt'), load_data('ModellingLocalSearch\data\dem51.txt')
x76, y76, dem76 = load_data('ModellingLocalSearch\data\\x76.txt'), load_data('ModellingLocalSearch\data\y76.txt'), load_data('ModellingLocalSearch\data\dem76.txt')

# Execute the local search for eil51 with p = 3, 4, 5
print("Starting local search for eil51...")
for p in [3, 4, 5]:
    print(f"\nRunning local search for eil51 with p={p}")
    local_search(x51, y51, dem51, p)

# Execute the local search for eil76 with p = 9, 10, 11
print("\nStarting local search for eil76...")
for p in [9, 10, 11]:
    print(f"\nRunning local search for eil76 with p={p}")
    local_search(x76, y76, dem76, p)
