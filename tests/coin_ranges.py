import regex as re
import os

with open(os.path.join(os.path.dirname(__file__), 'coin_ranges.txt')) as f:
  lines = f.readlines()

speeds = []
diameters = []

for line in lines:
  match = re.search(r"Calculated speed: (\d+\.\d+)$", line)
  if match:
    speeds.append(float(match.group(1)))

  match = re.search(r"Calculated diameter: (\d+\.\d+)$", line)
  if match:
    diameters.append(float(match.group(1)))

print("Found", len(speeds), "records.")
print("Min speed:", min(speeds))
print("Max speed:", max(speeds))
print("Min diameter:", min(diameters))
print("Max diameter:", max(diameters))