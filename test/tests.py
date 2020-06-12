# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# pylint: disable=invalid-name

"""Unit tests for quantum shift registers."""

import unittest
from random import randint
import sys
from ddt import ddt, data, unpack
from qiskit.circuit.exceptions import CircuitError

sys.path.append("../pyQSR")

from quantum_left_shift import QuantumLeftShift

@ddt
class TestQuantumLeftShift(unittest.TestCase):
    """Tests for Quantum Left/circular left shift registers."""

    def assertQSRNonCircularIsCorrect(self, seed, qsr, num_shifts):
        """Assert that the left shift operation performed is correct."""

        init_seed = int(seed, 2)
        for _ in range(num_shifts):
            init_seed = init_seed << 1
            qsr.shift()

        bits = len(seed)
        self.assertEqual(bin(init_seed)[::-1][:bits][::-1],
                         list(qsr.get_register_state().keys())[0])

    def assertQSRCircularIsCorrect(self, seed, qsr, num_shifts):
        """Assert that the left circular shift operation is correct."""

        seed = list(seed)
        for _ in range(num_shifts):
            temp = seed[0]
            seed[:-1] = seed[1:]
            seed[-1] = temp
            qsr.shift()

        seed = "".join(seed)
        self.assertEqual(seed, list(qsr.get_register_state().keys())[0])

    @data(
        [4, "1010", False],
        [5, "11010", False],
        [6, "100001", False],
        [7, "1100110", False]
    )
    @unpack
    def test_qsr_non_circular(self, data_qubits, seed, circular):
        """Test if the QSR circuit for non-cirular left shift is correct."""

        qsr = QuantumLeftShift(data_qubits, seed, circular)
        self.assertQSRNonCircularIsCorrect(seed, qsr, randint(1, data_qubits))

    @data(
        [4, "1010", True],
        [5, "11010", True],
        [6, "100001", True],
        [7, "1100110", True]
    )
    @unpack
    def test_qsr_circular(self, data_qubits, seed, circular):
        """Test if the QSR circuit for cirular left shift is correct."""

        qsr = QuantumLeftShift(data_qubits, seed, circular)
        self.assertQSRCircularIsCorrect(seed, qsr, randint(1, data_qubits))

    def test_raises_error(self):
        """Test if error is raised when length of seed is not
        equal to number of data qubits.
        """

        with self.assertRaises(CircuitError):
            QuantumLeftShift(5, "100", True)

if __name__ == '__main__':
    unittest.main()
