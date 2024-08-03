import os
from pathlib import Path
import pickle
import numpy as np

import wntr
import wntr_quantum

from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator
from qiskit_algorithms import optimizers as opt

from quantum_newton_raphson.vqls_solver import VQLS_SOLVER
from quantum_newton_raphson.splu_solver import SPLU_SOLVER


# input network
inp = "Net1.inp"

network_dir = Path("~/wntr-quantum/docs/notebooks/networks/").expanduser()
inp_file = str(network_dir / inp)

# create a water network model
wn = wntr.network.WaterNetworkModel(inp_file)
wn.options.time.duration = 0

# print options
print(dict(wn.options.hydraulic))
print(dict(wn.options.time))

# run classical simulation using traditional EpanetSimulator
sim = wntr.sim.EpanetSimulator(wn)
res = sim.run_sim()

# run classical simulation using QuantumEpanetSimulator
linear_solver = SPLU_SOLVER()
classical_sim = wntr_quantum.sim.QuantumEpanetSimulator(wn, linear_solver=linear_solver)
classical_res = classical_sim.run_sim()

print("#############################################")
print("Classical results:\n")

print("* Epanet simulator: \n")
print(f"{res.node['pressure']} \n {res.link['flowrate']} \n")

print("* Quantum Epanet simulator with classical linear solver: \n")
print(f"{classical_res.node['pressure']} \n {classical_res.link['flowrate']}")
print("############################################# \n")

# load EPANET A and b matrices from temp
epanet_A, epanet_b = wntr_quantum.sim.epanet.load_epanet_matrix()

# set the size of the Jacobian (A matrix)
epanet_A_dim = epanet_A.todense().shape[0]

print("#############################################")
print(f"Size of the Jacobian in EPANET simulator: {epanet_A_dim}")
print(f"Size of the b vector in EPANET simulator: {epanet_b.shape[0]}")
print("############################################# \n")

# run quantum simulator
n_qubits = int(np.ceil(np.log2(epanet_A_dim)))

print("#############################################")
print(f"Number of qubits needed: {n_qubits}")
print("############################################# \n")

qc = RealAmplitudes(n_qubits, reps=3, entanglement="full")
estimator = Estimator()

linear_solver = VQLS_SOLVER(
    estimator=estimator,
    ansatz=qc,
    optimizer=[opt.COBYLA(maxiter=1000, disp=True), opt.CG(maxiter=500, disp=True)],
    matrix_decomposition="symmetric",
    verbose=True,
    preconditioner="diagonal_scaling",
    reorder=True,
)

quantum_sim = wntr_quantum.sim.QuantumEpanetSimulator(wn, linear_solver=linear_solver)
quantum_res = quantum_sim.run_sim(linear_solver=linear_solver)

print("#############################################")
print("Quantum results:\n")
print(f"{quantum_res.node['pressure']} \n {quantum_res.link['flowrate']}")
print("#############################################")

# list of objects to pickle and their corresponding filenames
objects_to_pickle = [
    (wn, 'wn.pkl'),
    (classical_res, 'classical_res.pkl'),
    (quantum_res, 'quantum_res.pkl')
]

# save each object to its corresponding file
for obj, filename in objects_to_pickle:
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
