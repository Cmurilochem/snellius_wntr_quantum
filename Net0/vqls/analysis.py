import pickle
import matplotlib.pyplot as plt
import wntr

TOL = 5  # => per cent
DELTA = 1.0e-12


def get_ape_from_pd_series(quantum_pd_series, classical_pd_series):
    """Helper function to evaluate absolute percentage error between classical and quantum results."""
    ape = abs(quantum_pd_series - classical_pd_series) * 100.0 / abs(classical_pd_series + DELTA)
    return ape


def compare_results(classical_result, quantum_result):
    """
    Helper function that compares the classical and quantum simulation results.
    """
    classical_data = []
    quantum_data = []

    def check_ape(classical_value, quantum_value):
        """Helper function to check if the absolute percentage error between classical and quantum results is within TOL."""
        ape = abs(quantum_value - classical_value) * 100.0 / abs(classical_value + DELTA)
        is_close_to_classical = ape <= TOL
        if is_close_to_classical:
            print(f"Quantum result {quantum_value} within {ape}% of classical result {classical_value}")
            quantum_data.append(quantum_value)
            classical_data.append(classical_value)
        return is_close_to_classical

    for link in classical_result.link["flowrate"].columns:
        classical_value = classical_result.link["flowrate"][link].iloc[0]
        quantum_value = quantum_result.link["flowrate"][link].iloc[0]
        message = f"Flowrate {link}: {quantum_value} not within {TOL}% of classical result {classical_value}"
        assert check_ape(classical_value, quantum_value), message

    for node in classical_result.node["pressure"].columns:
        classical_value = classical_result.node["pressure"][node].iloc[0]
        quantum_value = quantum_result.node["pressure"][node].iloc[0]
        message = f"Pressure {node}: {quantum_value} not within {TOL}% of classical result {classical_value}"
        assert check_ape(classical_value, quantum_value), message

    return classical_data, quantum_data


# Load objects
with open("classical_res.pkl", "rb") as f:
    classical_res = pickle.load(f)

with open("quantum_res.pkl", "rb") as f:
    quantum_res = pickle.load(f)

with open("wn.pkl", "rb") as f:
    wn = pickle.load(f)

inp_file = "Net0"

# make the plot of the network
wntr.graphics.plot_network(
    wn,
    node_attribute=get_ape_from_pd_series(
        quantum_res.node["pressure"].iloc[0],
        classical_res.node["pressure"].iloc[0]
    ),
    link_attribute=get_ape_from_pd_series(
        quantum_res.link["flowrate"].iloc[0],
        classical_res.link["flowrate"].iloc[0],
    ),
    node_colorbar_label='Pressures',
    link_colorbar_label='Flows',
    node_size=50,
    title=f"{inp_file}: Absolute Percent Error",
    node_labels=False,
    filename=f"plot_{inp_file}_network_ape.png"
)

n_pipes = wn.num_pipes

results_classical, results_quantum = compare_results(classical_res, quantum_res)

# compare results
plt.close()
plt.scatter(results_classical[:n_pipes], results_quantum[:n_pipes], label="Flow rates", color="blue", marker="o")
plt.scatter(results_classical[n_pipes:], results_quantum[n_pipes:], label="Pressures", color="red", marker="s", facecolors='none')
plt.axline((0, 0), slope=1, linestyle="--", color="gray", label="")
plt.xlabel("Classical results")
plt.ylabel("Quantum results")
plt.legend()
plt.savefig(f"plot_{inp_file}_results_correlation.png")
# plt.show()