# -*- coding: utf-8 -*-
# pylint: disable=no-member

"""An IBM Qiskit implementation of quantum shift registers."""

__author__ = "Madhav Jivrajani"

from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.exceptions import CircuitError

class QuantumLeftShift:
    """Circuit to implement a quantum shift register.

    Two types of shift registers can be implemented:
        1. Left shift register.
        2. Circular left shift register.

    Reference:

    [1] Jae-weon Lee and Eok Kyun Lee and Jaewan Kim and Soonchil Lee, Quantum Shift Register, 2001.
    https://arxiv.org/abs/quant-ph/0112107
    """

    def __init__(self, data_qubits: int, seed: str, circular: bool = False) -> None:
        """Initializes a circuit for quantum shift register.
        - Encodes qubits according to the initial seed.

        To perform a shift operation on n data qubits, atleast n ancillary qubits are required
        to store information. Therefore, a circuit will have a total of 2*n qubits. An extra
        qubit apart from the 2*n qubits is required to store information about whether the circuit
        should behave as a left shift register or a circular left shift register.

        Args:
            data_qubits  :   The number of data qubits to be alloted. Needs to be equal to
                             length of seed.
            seed         :   Initial value the quantum shift register should start with.
            circular     :   Flag to indicate if the shifts are circular in nature or not.

        Raises:
            CircuitError :   If the number of data qubits is not equal to the length of the seed.
        """

        self.seed_string = seed

        #to follow qiskit's little endian encoding.
        self.seed = list(map(int, list(seed)))[::-1]
        self.num_data_qubits = data_qubits

        if len(seed) != self.num_data_qubits:
            raise CircuitError("Length of seed should be equal to number of data qubits.")

        self.shift_circuit = QuantumCircuit(self.num_data_qubits + self.num_data_qubits + 1,
                                            self.num_data_qubits)
        self.shifts_done = 0
        self.circular = circular
        self.__prepare_circuit()

        self.shift_gate = self.construct_shift_gate()

    def __repr__(self):
        return ("QuantumShiftLeft(data_qubits = %d, "
                "seed = \"%s\", "
                "circular = %s)") %  (self.num_data_qubits, self.seed_string, str(self.circular))

    def __str__(self):
        print(self.shift_circuit)
        return ("Data qubits: %d\n"
                "Initial seed: %s\n"
                "Shifts performed: %d\n"
                "Circular: %s") % (self.num_data_qubits, self.seed_string,
                                   self.shifts_done, str(self.circular))

    def __prepare_circuit(self):
        """Encodes qubits according to initial seed and the flag: circular"""
        for i in range(len(self.seed)):
            if self.seed[i] == 1:
                self.shift_circuit.x(i)
        if self.circular:
            self.shift_circuit.x(self.num_data_qubits + self.num_data_qubits)
        self.shift_circuit.barrier(range(self.num_data_qubits + self.num_data_qubits + 1))

    def construct_shift_gate(self):
        """Constructs a left/circular left shift circuit and
        returns the circuit as a Gate object.
        """
        if self.circular:
            name = "Circular Left Shift"
        else:
            name = "Left Shift"

        shift_circ = QuantumCircuit(self.num_data_qubits + self.num_data_qubits + 1, name=name)
        for qubit in range(1, self.num_data_qubits + self.num_data_qubits)[::-1]:
            shift_circ.swap(qubit, qubit - 1)

        shift_circ.cx(0, self.num_data_qubits)
        shift_circ.toffoli(self.num_data_qubits + self.num_data_qubits, self.num_data_qubits, 0)
        shift_circ.cx(0, self.num_data_qubits)

        shift_gate = shift_circ.to_gate()
        return shift_gate

    def shift(self):
        """Performs a single shift operation on the values of the data qubits."""
        self.shifts_done += 1
        self.shift_circuit.append(self.shift_gate,
                                  range(self.num_data_qubits + self.num_data_qubits + 1))

    def get_register_state(self):
        """Performs a measurement in the |0> basis on each of the data qubits
        and returns the counts of the measurement.
        """
        self.shift_circuit.barrier(range(self.num_data_qubits + self.num_data_qubits + 1))
        self.shift_circuit.measure(range(self.num_data_qubits), range(self.num_data_qubits))
        self.shift_circuit.barrier(range(self.num_data_qubits + self.num_data_qubits + 1))

        backend = Aer.get_backend('statevector_simulator')
        register_state = execute(self.shift_circuit, backend, shots=1024).result().get_counts()

        return register_state
