import numpy as np
import matplotlib.pyplot as plt


def wilson_cowan(time_max, dt, initial_values, constants):
    """
    Simulate the Wilson-Cowan model, which describes the dynamics of excitatory
    and inhibitory neurons in the brain. This function calculates the values 
    for r_E and r_I, which represent the average activity of excitatory and 
    inhibitory populations, respectively, over time.

    Args:
        time_max (float): The maximum simulation time.
        time_step (float): The time step for the simulation. dt.
        initial_values (np.ndarray): An array of initial values for r_E, r_I, 
            and time.
        constants (np.ndarray): An array of constants for tau_E, tau_I, w_EE, 
            w_EI, w_IE, and w_II.

    Returns:
        np.ndarray: A 2D array containing the values of r_E, r_I, and time at each time step.
    """
    # Create an (int(time_max/dt) + 1)x3 array to store r_E, r_I, and t in
    variables = np.vstack((initial_values, np.zeros((int(time_max/dt), 3))))

    for step in range(int(time_max/dt)):
        # Get results of previous iteration
        vars = variables[step]
        mult_vector = np.array([vars[0], vars[1]])

        # Compute r_E and r_I according to the simplified model
        r_E = vars[0] + dt / constants[0][0] * (constants[1] @ mult_vector)
        r_I = vars[1] + dt / constants[0][1] * (constants[2] @ mult_vector)

        # Update time
        t = vars[2] + dt

        next_vars = np.array([r_E, r_I, t])
        variables[step + 1] = next_vars

    return variables


def plotter(variables, constants):
    """
    Plot the results of the Wilson-Cowan simulation, including time-series 
    plots of r_E and r_I, as well as a phase space diagram with nullclines.

    Args:
        variables (np.ndarray): A 2D array of the values of r_E, r_I, and time 
            at each time step.
        constants (np.ndarray): An array of constants for tau_E, tau_I, w_EE, 
            w_EI, w_IE, and w_II.

    Returns:
        None
    """
    # Plot r_E against time
    plt.plot(variables[:, 2], variables[:, 0], c='0', label=r'$r_E$')

    # Plot r_I against time
    plt.plot(variables[:, 2], variables[:, 1], c='0.8', label=r'$r_I$')
    
    plt.title(r'$\tau_E \frac{dr_E}{dt} = w_{EE}r_E + w_{EI}r_I, \ $'
              + r'$\tau_I \frac{dr_I}{dt} = w_{IE}r_E + w_{II}r_I$')
    plt.xlabel('time')
    plt.ylabel('rate')
    plt.suptitle('The Wilson-Cowan Model:')
    plt.legend()
    plt.show()
    
    nullclines = [-constants[i][0] / constants[i][1] * variables[:,0]
                 for i in range(2)]
    for i in range(2):
        plt.plot(variables[:,0], nullclines[i], '0.5', linewidth=0.5)

    # Plot r_E against r_I
    plt.plot(variables[:,0], variables[:,1], 'k', linewidth=0.5)
    plt.xlabel(r'$r_E$')
    plt.ylabel(r'$r_I$')
    plt.ylim(max(variables[:,1]), min(variables[:,1]))
    plt.title('Phase space diagram with nullclines')
    plt.show()


# r_E, r_I, and time
initial_variables = np.array([[30, 20, 0]])

# tau_E, tau_I, w_EE, w_EI, w_IE, and w_II
constants = np.array([[100, 120], [1, -5], [0.6, -1]])

if __name__ == "__main__":
    variables = wilson_cowan(1000, 1, initial_variables, constants)
    plotter(variables, constants)