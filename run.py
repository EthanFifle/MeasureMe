import sys
from pprint import pprint
import torch
from measure import MeasureBody
from measurement_definitions import STANDARD_LABELS

# Retrieve the filename from command-line arguments


# Rest of your code
# Use new_filename where you need to refer to the file
# For example, if you need to load data from the file, use new_filename to open it

measurer = MeasureBody('smpl')

betas = torch.zeros((1, 10), dtype=torch.float32)
measurer.from_body_model(gender="MALE", shape=betas)

measurement_names = measurer.all_possible_measurements # or chose subset of measurements
measurer.measure(measurement_names)
measurer.label_measurements(STANDARD_LABELS)

print("Measurements")
pprint(measurer.measurements)