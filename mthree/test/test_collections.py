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
# pylint: disable=no-name-in-module

"""Test collection classes"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAthens
from qiskit_ibm_runtime import SamplerV2 as Sampler
import mthree


def test_mit_overhead():
    """Test if mitigation overhead over collection is same as loop
    """
    backend = FakeAthens()
    qc = QuantumCircuit(5)
    qc.h(2)
    qc.cx(2, 1)
    qc.cx(2, 3)
    qc.cx(1, 0)
    qc.cx(3, 4)
    qc.measure_all()

    sampler = Sampler(backend=backend)
    primitive_results = sampler.run([qc]*10).result()
    raw_counts = [pub_result.data.meas.get_counts() for pub_result in primitive_results]
    mit = mthree.M3Mitigation(sampler)
    mit.cals_from_system()
    mit_counts = mit.apply_correction(raw_counts, qubits=range(5),
                                      return_mitigation_overhead=True)

    ind_overheads = np.asarray([cnt.mitigation_overhead for cnt in mit_counts])
    assert np.allclose(mit_counts.mitigation_overhead, ind_overheads)


def test_shots():
    """Test if shots works over collections
    """
    backend = FakeAthens()
    qc = QuantumCircuit(5)
    qc.h(2)
    qc.cx(2, 1)
    qc.cx(2, 3)
    qc.cx(1, 0)
    qc.cx(3, 4)
    qc.measure_all()

    sampler = Sampler(backend=backend)
    primitive_results = sampler.run([qc]*10, shots=4321).result()
    raw_counts = [pub_result.data.meas.get_counts() for pub_result in primitive_results]
    mit = mthree.M3Mitigation(sampler)
    mit.cals_from_system()
    mit_counts = mit.apply_correction(raw_counts, qubits=range(5),
                                      return_mitigation_overhead=True)

    assert np.allclose(mit_counts.nearest_probability_distribution().shots,
                       mit_counts.shots)

    assert np.all(mit_counts.shots == 4321)
