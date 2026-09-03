from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

import math


def quantum_risk_optimizer(risk_score):

    # Convert risk score (0-100) into angle
    angle = (risk_score / 100) * math.pi

    qc = QuantumCircuit(1, 1)

    # Encode risk into qubit
    qc.ry(angle, 0)

    # Measure
    qc.measure(0, 0)

    simulator = AerSimulator()

    result = simulator.run(
        qc,
        shots=1000
    ).result()

    counts = result.get_counts()

    probability = (
        counts.get("1", 0) / 1000
    ) * 100

    return {
        "quantum_probability": round(
            probability,
            2
        ),
        "quantum_counts": counts
    }