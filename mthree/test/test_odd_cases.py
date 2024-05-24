# This code is part of Mthree.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test utils functions"""
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import SamplerV2 as Sampler
import mthree


def test_simulator_overhead():
    """Verify a single bitstring from the sim works with mitigation overhead"""
    qc = QuantumCircuit(6)
    qc.measure_all()

    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    mit = mthree.M3Mitigation(sampler)
    mit.cals_from_system(range(6))

    trans_qc = transpile(qc, backend)
    raw_counts = sampler.run([trans_qc], shots=100).result()[0].data.meas.get_counts()

    quasi = mit.apply_correction(raw_counts, range(6), return_mitigation_overhead=True)
    assert quasi.mitigation_overhead == 1.0
