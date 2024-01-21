import random
import math


file_paths = {
    'x51': 'ModellingLocalSearch\data\\x51.txt',
    'y51': 'ModellingLocalSearch\data\\y51.txt',
    'dem51': 'ModellingLocalSearch\data\\dem51.txt',
    'x76': 'ModellingLocalSearch\data\\x76.txt',
    'y76': 'ModellingLocalSearch\data\\y76.txt',
    'dem76': 'ModellingLocalSearch\data\\dem76.txt'
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
        facility_to_replace = random.choice(perturbed_solution)
        new_facility = (random.choice(x), random.choice(y))
        perturbed_solution.remove(facility_to_replace)
        perturbed_solution.append(new_facility)
    return perturbed_solution

def iterated_local_search(x, y, dem, p, max_iterations_per_local_search=1000, num_restarts=5, perturbation_strength=2):
    s = generate_initial_solution(x, y, p)
    best_solution = s
    best_evaluation = evaluate_solution(s, x, y, dem)
    
    for restart in range(num_restarts):
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
                print(f"\n--> New best solution found at iteration {iteration} of restart {restart + 1}:")
                print(f"    Evaluation: {best_evaluation:.2f}")
                print(f"    Solution: {best_solution}")

            # Print the best evaluation every 1000 iterations
            if iteration % 1000 == 0:
                print(f"At iteration {iteration}, current best evaluation: {best_evaluation:.2f}")

        # Perturb the best solution to escape local optima
        s = perturb_solution(best_solution, x, y, perturbation_strength)
        print(f"\nPerturbed solution set at the end of restart {restart + 1}: {s}")

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
