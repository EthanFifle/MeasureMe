# techpack.py
import torch
import json
from measure import MeasureBody
from measurement_definitions import STANDARD_LABELS

def measure_body(gender, betas_list):
    """
    Takes gender and betas, and returns the measurements as a JSON string.

    Parameters:
    - gender (str): Gender of the body model ('MALE', 'FEMALE', 'NEUTRAL').
    - betas_list (list): List of beta values for body shape.

    Returns:
    - str: JSON-formatted string of measurements.
    """
    # Convert betas_list to a torch tensor
    betas = torch.tensor(betas_list, dtype=torch.float32)

    measurer = MeasureBody('smpl')
    measurer.from_body_model(gender=gender, shape=betas)

    measurement_names = measurer.all_possible_measurements  # or choose a subset of measurements
    measurer.measure(measurement_names)
    measurer.label_measurements(STANDARD_LABELS)

    # Serialize the measurements to a JSON-formatted string
    measurements_json = json.dumps(measurer.measurements)

    return measurements_json
