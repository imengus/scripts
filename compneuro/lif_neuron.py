"""
Simulates a linear integrate and fire neuron using the recurrence relation:
V_m = - b * V_m + a * (I_exc - I_inh), where the excitatory and inhibitory
inputs I are modelled using a poisson distribution.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson


def lif_neuron_inh(
    num_steps: int = 10000,
    alpha: float = 0.5,
    beta: float = 0.1,
    exc_rate: float = 10.0,
    inh_rate: float = 10,
) -> None:
    
    # initialize arrays to store membrane potential, time, spikes, and 
    # inter-spike intervals
    v = np.zeros(1)
    t = np.zeros(1)
    spikes = np.zeros(2)
    inter_spike_intervals = np.array([])

    # excitatory and inhibitory inputs are modelled using Poisson distributions
    poisson_dist = (
        poisson.rvs(exc_rate, 0, num_steps),
        poisson.rvs(inh_rate, 0, num_steps),
    )

    for n in range(num_steps):
        try:
            # input is modelled by Poisson distribution
            istate = (poisson_dist[0][n] - poisson_dist[1][n])

            # update the membrane potential using the linear LIF model
            v = np.append(
                v, v[n] * (1 - beta) + alpha * istate
            )

            # if the membrane potential exceeds the threshold, record a spike 
            # and reset the membrane potential
            if v[-1] >= 1:
                v[-2] = 1
                v[-1] = 0
                spikes = np.append(spikes, n)
                inter_spike_intervals = np.append(
                    inter_spike_intervals, spikes[-1] - spikes[-2]
                )

            t = np.append(t, n)
        except IndexError:
            pass

    try:
        # calculate the range using the mean of inter-spike intervals
        plot_range = int(np.mean(inter_spike_intervals) * 20)
    except ValueError:
        # if there are no inter-spike intervals, set range to 50 * 20
        plot_range = 50 * 20

    # filter the spikes to only include those that occur within the plotted 
    # range
    filtered_spikes = np.array([])
    for j in spikes:
        if j < plot_range:
            filtered_spikes = np.append(filtered_spikes, j)

    # calculate the 5th and 95th percentiles of the inter-spike interval 
    # distribution
    lb = np.percentile(inter_spike_intervals, 5)
    ub = np.percentile(inter_spike_intervals, 95)

    fig, ax = plt.subplots(2, 1)
    # plot the voltage trace
    ax[0].plot(t[:plot_range], v[:plot_range], c="k", linewidth=0.5)
    ax[0].title.set_text(
        r"$\alpha = %s, \beta = %s, \lambda_{exc} = %s,"
        r" \lambda_{inh} = %s$ :" % (alpha, beta, exc_rate, inh_rate)
    )
    ax[0].set_xlabel("time / s")
    ax[0].set_ylabel(r"$V_m$ / mV")

    # plot vertical lines for spikes
    for i in filtered_spikes:
        ax[0].axvline(i - 1, linestyle="dotted", linewidth=0.5, color="k")

    # plot the histogram of inter-spike intervals
    ax[1].hist(
        inter_spike_intervals,
        bins=25,
        range=(lb, ub),
        histtype="step",
        color="k",
        linewidth=0.5
    )
    ax[1].set_xlabel(r"Inter-spike intervals within $\pm 2\sigma$ / s")
    ax[1].set_ylabel("n")

    title_str = r"Linear LIF neurons: $\Delta V_m = - \beta V_m +" \
    r"\alpha (I_{exc} - I_{inh}), \ \ I_{state} \sim$ Poisson$(\lambda_{state})$"

    plt.suptitle(title_str)

    plt.show()

if __name__ == "__main__":
    lif_neuron_inh(num_steps=1000, alpha=0.01, beta=0, exc_rate=10, inh_rate=8)
