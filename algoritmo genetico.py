import numpy as np

# --- 1. Definición de Parámetros ---
POP_SIZE = 100    # Tamaño de la población
N_BITS = 5        # Número de bits del cromosoma (x de 0 a 31)
GEN_MAX = 50      # Número máximo de generaciones
PROB_MUT = 0.01   # Probabilidad de mutación
PROB_CROSS = 0.7  # Probabilidad de cruce

# --- 2. Función Objetivo (Fitness) ---
# Se busca maximizar f(x) = x^2, donde x es el valor entero del cromosoma
def calculate_fitness(pop):
    # Decodificar el cromosoma binario a valor entero 'x'
    weights = 2**np.arange(N_BITS)[::-1]
    x = np.dot(pop, weights)
    
    # Calcular el valor de fitness
    return x**2, x

# --- 3. Operadores Genéticos ---

# a) Inicialización de la Población
def initialize_population():
    return np.random.randint(0, 2, size=(POP_SIZE, N_BITS))

# b) Selección por Ruleta
def select_parents(pop, fitness):
    # Ajustar fitness si hay valores negativos (no aplica aquí, pero es buena práctica)
    if np.min(fitness) < 0:
        norm_fitness = fitness - np.min(fitness)
    else:
        norm_fitness = fitness
        
    total_fitness = np.sum(norm_fitness)
    probabilities = norm_fitness / total_fitness # Cálculo de probabilidades (ruleta)
    
    # Seleccionar POP_SIZE de individuos con reemplazo
    indices = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, p=probabilities)
    return pop[indices]

# c) Cruce (Crossover) en un punto aleatorio
def crossover(p1, p2):
    if np.random.rand() < PROB_CROSS:
        cross_point = np.random.randint(1, N_BITS)
        o1 = np.concatenate((p1[:cross_point], p2[cross_point:]))
        o2 = np.concatenate((p2[:cross_point], p1[cross_point:]))
        return o1, o2
    return p1, p2

# d) Mutación (Bit-flip)
def mutate(chromosome):
    for i in range(N_BITS):
        if np.random.rand() < PROB_MUT:
            chromosome[i] = 1 - chromosome[i] # Voltear el bit
    return chromosome

# --- 4. Algoritmo Genético Principal ---
def genetic_algorithm():
    population = initialize_population()
    
    for gen in range(GEN_MAX):
        # 1. Evaluación
        fitness, x_values = calculate_fitness(population)
        
        # 2. Selección
        parents = select_parents(population, fitness)
        
        # 3. Reproducción (Cruce y Mutación)
        new_population = []
        for i in range(0, POP_SIZE, 2):
            p1, p2 = parents[i], parents[i+1]
            o1, o2 = crossover(p1, p2)
            o1 = mutate(o1)
            o2 = mutate(o2)
            new_population.extend([o1, o2])
            
        population = np.array(new_population)

    # Retorno del mejor individuo de la última población
    final_fitness, final_x = calculate_fitness(population)
    overall_best_index = np.argmax(final_fitness)
    return final_x[overall_best_index], final_fitness[overall_best_index]

# Ejecutar el algoritmo
# best_x, best_fitness = genetic_algorithm()