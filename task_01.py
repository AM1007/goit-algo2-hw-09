import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Define the Sphere function
def sphere_function(x):
    return sum(xi ** 2 for xi in x)


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    # Generate a random starting point within bounds
    dimensions = len(bounds)
    current_point = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dimensions)]
    current_value = func(current_point)
    
    # Track progress
    history = [(current_point.copy(), current_value)]
    
    for i in range(iterations):
        # Try a small step in each dimension
        improved = False
        for dim in range(dimensions):
            # Try a positive step
            test_point = current_point.copy()
            step_size = (bounds[dim][1] - bounds[dim][0]) * 0.01  # 1% of range as step size
            test_point[dim] += step_size
            
            # Ensure we stay within bounds
            test_point[dim] = max(bounds[dim][0], min(bounds[dim][1], test_point[dim]))
            
            test_value = func(test_point)
            if test_value < current_value:
                current_point = test_point
                current_value = test_value
                improved = True
                break
                
            # Try a negative step
            test_point = current_point.copy()
            test_point[dim] -= step_size
            
            # Ensure we stay within bounds
            test_point[dim] = max(bounds[dim][0], min(bounds[dim][1], test_point[dim]))
            
            test_value = func(test_point)
            if test_value < current_value:
                current_point = test_point
                current_value = test_value
                improved = True
                break
        
        # Record progress
        history.append((current_point.copy(), current_value))
        
        # If no improvement or reached epsilon threshold, terminate
        if not improved or (len(history) > 1 and abs(history[-2][1] - history[-1][1]) < epsilon):
            break
            
    return current_point, current_value, history


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    # Generate a random starting point within bounds
    dimensions = len(bounds)
    current_point = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dimensions)]
    current_value = func(current_point)
    
    # Track progress
    history = [(current_point.copy(), current_value)]
    
    # Define the neighborhood size (starts big, gets smaller)
    neighborhood_size = 1.0  # Starting with a relatively large neighborhood
    
    for i in range(iterations):
        # Generate a random point in the neighborhood
        test_point = []
        for dim in range(dimensions):
            offset = random.uniform(-neighborhood_size, neighborhood_size)
            value = current_point[dim] + offset
            # Ensure we stay within bounds
            value = max(bounds[dim][0], min(bounds[dim][1], value))
            test_point.append(value)
        
        test_value = func(test_point)
        
        # If better, accept the new point
        if test_value < current_value:
            current_point = test_point
            current_value = test_value
            # Reduce neighborhood size slightly for more focused search
            neighborhood_size *= 0.99
        else:
            # Increase neighborhood size slightly for exploration
            neighborhood_size *= 1.01
            # But keep it reasonable
            neighborhood_size = min(neighborhood_size, 2.0)
        
        # Record progress
        history.append((current_point.copy(), current_value))
        
        # Check termination condition
        if len(history) > 1 and abs(history[-2][1] - history[-1][1]) < epsilon:
            break
            
    return current_point, current_value, history


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    # Generate a random starting point within bounds
    dimensions = len(bounds)
    current_point = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(dimensions)]
    current_value = func(current_point)
    
    # Initialize best point found so far
    best_point = current_point.copy()
    best_value = current_value
    
    # Track progress
    history = [(current_point.copy(), current_value)]
    
    # Temperature schedule
    temperature = temp
    
    for i in range(iterations):
        # Stop if temperature is too low
        if temperature < epsilon:
            break
            
        # Generate a neighbor
        test_point = []
        for dim in range(dimensions):
            # Scale the step size by temperature (larger steps at higher temps)
            step_size = (bounds[dim][1] - bounds[dim][0]) * 0.1 * (temperature / temp)
            offset = random.uniform(-step_size, step_size)
            value = current_point[dim] + offset
            # Ensure we stay within bounds
            value = max(bounds[dim][0], min(bounds[dim][1], value))
            test_point.append(value)
        
        test_value = func(test_point)
        
        # Decide whether to accept the new point
        # Always accept better solutions, sometimes accept worse ones
        if test_value < current_value:
            current_point = test_point
            current_value = test_value
            
            # Update best solution if needed
            if test_value < best_value:
                best_point = test_point.copy()
                best_value = test_value
        else:
            # Calculate acceptance probability
            # Worse solutions are accepted with a probability that decreases with temperature
            delta = test_value - current_value
            acceptance_probability = math.exp(-delta / temperature)
            
            if random.random() < acceptance_probability:
                current_point = test_point
                current_value = test_value
        
        # Record progress
        history.append((current_point.copy(), current_value))
        
        # Cool down the temperature
        temperature *= cooling_rate
        
        # Check termination condition (excluding temperature criterion that is checked at the start)
        if len(history) > 1 and abs(history[-2][1] - history[-1][1]) < epsilon:
            # Only terminate if we've been at the same value for a while
            if len(history) > 10 and abs(history[-10][1] - history[-1][1]) < epsilon:
                break
            
    return best_point, best_value, history


def plot_optimization_progress(title, history):
    """Plot the function values over iterations."""
    values = [entry[1] for entry in history]
    plt.figure(figsize=(10, 6))
    plt.plot(values)
    plt.xlabel('Iteration')
    plt.ylabel('Function Value')
    plt.title(f'{title} Optimization Progress')
    plt.yscale('log')  # Log scale often helps visualize convergence
    plt.grid(True)
    plt.savefig(f'{title.lower().replace(" ", "_")}_progress.png')


def visualize_sphere_function():
    """Create a 3D visualization of the Sphere function."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a grid of x, y values
    x1 = np.linspace(-5, 5, 100)
    x2 = np.linspace(-5, 5, 100)
    X1, X2 = np.meshgrid(x1, x2)
    
    # Calculate function values for the grid
    Z = X1**2 + X2**2
    
    # Create the surface plot
    surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
    
    # Set labels and title
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x1, x2)')
    ax.set_title('Функція Сфери')
    
    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    plt.savefig('sphere_function_3d.png')


if __name__ == "__main__":
    # Define function bounds
    bounds = [(-5, 5), (-5, 5)]
    
    # Visualize the Sphere function
    visualize_sphere_function()
    
    # Execute algorithms
    print("Hill Climbing:")
    hc_solution, hc_value, hc_history = hill_climbing(sphere_function, bounds)
    print("Solution:", hc_solution, "Value:", hc_value)
    plot_optimization_progress("Hill Climbing", hc_history)
    
    print("\nRandom Local Search:")
    rls_solution, rls_value, rls_history = random_local_search(sphere_function, bounds)
    print("Solution:", rls_solution, "Value:", rls_value)
    plot_optimization_progress("Random Local Search", rls_history)
    
    print("\nSimulated Annealing:")
    sa_solution, sa_value, sa_history = simulated_annealing(sphere_function, bounds)
    print("Solution:", sa_solution, "Value:", sa_value)
    plot_optimization_progress("Simulated Annealing", sa_history)
    
    # Compare results
    print("\nResults Comparison:")
    print(f"{'Algorithm':<20} {'Solution':<40} {'Function Value':<15}")
    print("-" * 75)
    print(f"{'Hill Climbing':<20} {str(hc_solution):<40} {hc_value:<15.10f}")
    print(f"{'Random Local Search':<20} {str(rls_solution):<40} {rls_value:<15.10f}")
    print(f"{'Simulated Annealing':<20} {str(sa_solution):<40} {sa_value:<15.10f}")