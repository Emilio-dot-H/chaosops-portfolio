import re
import numpy as np
from sklearn.ensemble import IsolationForest

# Read the log file
with open("app_logs.txt", "r") as f:
    logs = f.readlines()

# Prepare data for anomaly detection
X = []   # feature vectors
log_lines = []  # to keep original lines for reference
for line in logs:
    line = line.strip()
    # We only care about lines that have our pattern
    # e.g., "INFO:root:Handled / in 123ms" or "ERROR:root:Chaos endpoint error! Took 1500ms"
    # e.g., match = re.search(r'(INFO|ERROR):root:.*?(\d+)ms', line)
    match = re.search(r'(INFO|ERROR) in app:.*?(\d+)ms', line)
    if not match:
        continue
    level = match.group(1)
    time_ms = int(match.group(2))
    error_flag = 1 if level == "ERROR" else 0
    # Feature vector: [time_ms, error_flag]
    X.append([time_ms, error_flag])
    log_lines.append(line)

X = np.array(X)
print(f"Parsed {len(X)} log entries for analysis.")

# Train Isolation Forest
model = IsolationForest(n_estimators=100, contamination="auto", random_state=42)
model.fit(X)
preds = model.predict(X)  # 1 for normal, -1 for anomaly

# Collect anomalies
anomalies = []
for i, pred in enumerate(preds):
    if pred == -1:  # anomaly
        anomalies.append(log_lines[i])

print(f"Detected {len(anomalies)} anomalies out of {len(X)} log entries.")
print("Anomalous log lines:")
for line in anomalies:
    print(line)
