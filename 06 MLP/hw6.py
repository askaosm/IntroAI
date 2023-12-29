import numpy as np

epsilon = 1e-3
import numpy as np

def calculate_transition_probability(mdp_model, row, col, action, direction):
    """
    Calculate the transition probability for a given action and direction.
    """
    M, N = mdp_model.M, mdp_model.N
    new_row, new_col = row + direction[0], col + direction[1]

    # Check grid boundaries and walls
    if 0 <= new_row < M and 0 <= new_col < N and not mdp_model.W[new_row, new_col]:
        return new_row, new_col, mdp_model.D[row, col, action]
    else:
        return row, col, mdp_model.D[row, col, action]

def compute_transition_matrix(mdp_model):
    """
    Build a transition matrix for the MDP model.
    """
    M, N = mdp_model.M, mdp_model.N
    transition_matrix = np.zeros((M, N, 4, M, N))
    
    # Define actions
    actions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # left, up, right, down

    # Process each cell in the grid
    for row in range(M):
        for col in range(N):
            if mdp_model.T[row, col]:
                continue

            # Process each action
            for a in range(4):
                # Straight move
                r, c, prob = calculate_transition_probability(mdp_model, row, col, 0, actions[a])
                transition_matrix[row, col, a, r, c] += prob

                # Counter-clockwise move
                r, c, prob = calculate_transition_probability(mdp_model, row, col, 1, actions[(a - 1) % 4])
                transition_matrix[row, col, a, r, c] += prob

                # Clockwise move
                r, c, prob = calculate_transition_probability(mdp_model, row, col, 2, actions[(a + 1) % 4])
                transition_matrix[row, col, a, r, c] += prob

    return transition_matrix










def update_utility(model, P, U_current):
    """
    Parameters:
    model - The MDP model returned by load_MDP()
    P - The precomputed transition matrix returned by compute_transition_matrix()
    U_current - The current utility function, which is an M x N array

    Output:
    U_next - The updated utility function, which is an M x N array
    """

    M, N = model.M, model.N  # get grid size
    U_next = np.zeros((M, N))  # init

    # for loop all possible cases of grid
    for r in range(M):
        for c in range(N):
            # if it is a terminal state, the utility remains the same
            if model.T[r, c]:
                U_next[r, c] = model.R[r, c]
                continue
            # Compute expected utility for each possible action
            U_actions=[]
            for a in range(4):
                U_excepted=0
                for r_prime in range(M):
                    for c_prime in range(N):
                        U_excepted+=P[r,c,a,r_prime,c_prime]*U_current[r_prime][c_prime]
                U_actions.append(U_excepted)
             # Update the utility for the current state
            U_next[r, c] = model.R[r, c] + model.gamma * max(U_actions)

    
    return U_next


def value_iteration(model):
    """
    Parameters:
    model - The MDP model returned by load_MDP()

    Output:
    U - The utility function, which is an M x N array
    """


    M, N = model.M, model.N  
    U = np.zeros((M, N))  


    P = compute_transition_matrix(model)   # Compute the state transition probabilities.
    gamma = model.gamma  # discount probability

    while True:
        U_prev = U.copy()  # copy  the current utility 
        U = update_utility(model, P, U_prev) #update uitlity
        delta = np.abs(U - U_prev).max()  
        if delta < epsilon:  # end condtion:# End the iteration when the change is small enough
            break

    return U

