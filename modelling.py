import random
import math

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

# Function to find the nearest neighbor of an element
def find_nearest_neighbor(solution, element):
    nearest = None
    min_distance = float('inf')
    for candidate in solution:
        if candidate == element:
            continue
        dist = euclidean_distance(element[0], element[1], candidate[0], candidate[1])
        if dist < min_distance:
            min_distance = dist
            nearest = candidate
    return nearest

# Function to permute elements in the solution
def permute_elements(solution, element, nearest):
    new_solution = solution.copy()
    new_solution.remove(element)
    new_solution.append(nearest)
    return new_solution

# Main local search function
def local_search(x, y, dem, p, max_iterations=1000):
    s = generate_initial_solution(x, y, p)
    best_solution = s
    best_evaluation = evaluate_solution(s, x, y, dem)
    
    for iteration in range(max_iterations):
        s_new = s.copy()
        random_element = random.choice(s_new)
        nearest_neighbor = find_nearest_neighbor(s_new, random_element)
        s_new = permute_elements(s_new, random_element, nearest_neighbor)
        current_evaluation = evaluate_solution(s_new, x, y, dem)
        
        if current_evaluation < best_evaluation:
            best_solution = s_new
            best_evaluation = current_evaluation
            
        # Stopping criteria check (can be based on a minimal error, max number of iterations, etc.)
        if iteration == max_iterations - 1:
            break
            
    return best_solution, best_evaluation

# Main function to run the local search algorithm for different values of p
def main():
    # Load the data for eil51 and eil76 instances
    x51, y51, dem51 = load_data('x51.txt'), load_data('y51.txt'), load_data('dem51.txt')
    x76, y76, dem76 = load_data('x76.txt'), load_data('y76.txt'), load_data('dem76.txt')

    # Run the local search for eil51 with p = 3, 4, 5
    for p in [3, 4, 5]:
        solution, evaluation = local_search(x51, y51, dem51, p)
        print(f"Solution for eil51 with p={p}: {solution}")
        print(f"Evaluation: {evaluation}\n")

    # Run the local search for eil76 with p = 9, 10, 11
    for p in [9, 10, 11]:
        solution, evaluation = local_search(x76, y76, dem76, p)
        print(f"Solution for eil76 with p={p}: {solution}")
        print(f"Evaluation: {evaluation}\n")

if __name__ == "__main__":
    main()
