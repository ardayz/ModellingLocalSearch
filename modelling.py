import random
import math
import time
import matplotlib.pyplot as plt

def plot_facilities_and_demand_nodes(x, y, dem, facilities):
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.scatter(x, y, c='blue', label='Demand Nodes')  # Plot demand nodes
    facilities_x = [facility[0] for facility in facilities]
    facilities_y = [facility[1] for facility in facilities]
    plt.scatter(facilities_x, facilities_y, c='red', label='Facilities')  # Plot facilities

    # Draw lines from each demand node to the closest facility
    for i in range(len(x)):
        closest_facility = min(facilities, key=lambda facility: euclidean_distance(x[i], y[i], facility[0], facility[1]))
        plt.plot([x[i], closest_facility[0]], [y[i], closest_facility[1]], 'k--', linewidth=0.5)

    plt.title('Facility and Demand Node Assignments')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()



start_time = time.time()
file_paths = {
    'x51': 'x51.txt',
    'y51': 'y51.txt',
    'dem51': 'dem51.txt',
    'x76': 'x76.txt',
    'y76': 'y76.txt',
    'dem76': 'dem76.txt'
}

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

# Perturbation function
def perturb_solution(solution, x, y, perturbation_strength):
    perturbed_solution = solution.copy()
    for _ in range(perturbation_strength):
        perturbation_start_time = time.time()  # Record the start time of the perturbation
    
        facility_to_replace = random.choice(perturbed_solution)
        new_facility = (random.choice(x), random.choice(y))
        perturbed_solution.remove(facility_to_replace)
        perturbed_solution.append(new_facility)
        perturbation_end_time = time.time()  # Record the end time of the iteration
        perturbation_duration = perturbation_end_time - perturbation_start_time
    return perturbed_solution

def iterated_local_search(x, y, dem, p, max_iterations_per_local_search=1000, num_restarts=5, perturbation_strength=2):
    s = generate_initial_solution(x, y, p)
    best_solution = s
    best_evaluation = evaluate_solution(s, x, y, dem)
    
    for restart in range(num_restarts):
        iteration_start_time = time.time()  # Record the start time of the iteration
        s = best_solution  # Start with the best found solution
        print(f"\nStarting restart {restart + 1} with initial solution: {s}")
        for iteration in range(max_iterations_per_local_search):
            s_new = s.copy()
            facility_to_replace = random.choice(s_new)
            new_facility = (random.choice(x), random.choice(y))
            s_new.remove(facility_to_replace)
            s_new.append(new_facility)
            current_evaluation = evaluate_solution(s_new, x, y, dem)
            if current_evaluation < best_evaluation:
                best_solution = s_new
                best_evaluation = current_evaluation
                iteration_end_time = time.time()  # Record the end time of the iteration
                iteration_duration = iteration_end_time - iteration_start_time

                print(f"\n--> New best solution found at iteration {iteration} of restart {restart + 1}:")
                print(f"    Evaluation: {best_evaluation:.2f}")
                print(f"    Solution: {best_solution}")
                print(f"    Iteration duration is: {iteration_duration}")

            # Print the best evaluation every 1000 iterations
            if iteration % 1000 == 0:
                print(f"At iteration {iteration}, current best evaluation: {best_evaluation:.2f}")

        # Perturb the best solution to escape local optima
        s = perturb_solution(best_solution, x, y, perturbation_strength)
        print(f"\nPerturbed solution set at the end of restart {restart + 1}: {s}")
        #print(f"\nPerturbed solution duration at the end of restart {perturbation_duration})

    print(f"\nCompleted iterated local search after {num_restarts} restarts.")
    print(f"Best solution found: {best_solution}")
    print(f"Best solution evaluation: {best_evaluation:.2f}")
    return best_solution, best_evaluation



# Load the data for eil51 and eil76 instances
x51, y51, dem51 = load_data(file_paths['x51']), load_data(file_paths['y51']), load_data(file_paths['dem51'])
x76, y76, dem76 = load_data(file_paths['x76']), load_data(file_paths['y76']), load_data(file_paths['dem76'])

# Execute the iterated local search for eil51 with p = 3, 4, 5
print("Running iterated local search for eil51...")
for p in [3, 4, 5]:
    print(f"\nRunning iterated local search for eil51 with p={p}")
    iterated_local_search(x51, y51, dem51, p)

# Execute the iterated local search for eil76 with p = 9, 10, 11
print("\nRunning iterated local search for eil76...")
for p in [9, 10, 11]:
    print(f"\nRunning iterated local search for eil76 with p={p}")
    iterated_local_search(x76, y76, dem76, p)

best_solution, best_evaluation = iterated_local_search(x51, y51, dem51, p=5)
plot_facilities_and_demand_nodes(x51, y51, dem51, best_solution)
end_time= time.time()
total_runtime = end_time - start_time
print(f"Total run time of the script: {total_runtime:.2f} seconds.")
