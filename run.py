import sys
import torch
import json
from measure import MeasureBody
from measurement_definitions import STANDARD_LABELS

# Check if the required arguments were passed to the script
if len(sys.argv) < 2:
    raise ValueError("Gender not provided as a command-line argument.")

gender = sys.argv[1].upper()
measurer = MeasureBody('smpl')

betas = torch.zeros((1, 10), dtype=torch.float32)
measurer.from_body_model(gender=gender, shape=betas)

measurement_names = measurer.all_possible_measurements # or chose subset of measurements
measurer.measure(measurement_names)
measurer.label_measurements(STANDARD_LABELS)

# Serialize the measurements to a JSON-formatted string
measurements_json = json.dumps(measurer.measurements)

# Print the JSON-formatted string
print(measurements_json)

