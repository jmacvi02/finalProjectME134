import torch
import csv
import os

# Define the same model architecture used during training
import torch.nn as nn

class MotorEffortNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(8, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )
    
    def forward(self, x):
        return self.net(x)

# Load the trained model
model = MotorEffortNet()
model.load_state_dict(torch.load("motor_effort_model.pth"))
model.eval()

# Extract state_dict (a dictionary of weights)
state_dict = model.state_dict()

# Define a helper to save matrices or vectors to CSV
def save_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Data is expected to be a list of lists (or a flat list for biases)
        if isinstance(data[0], list):  # matrix
            for row in data:
                writer.writerow(row)
        else:  # vector
            writer.writerow(data)

# Prepare output directory
output_dir = "model_weights_csv"
os.makedirs(output_dir, exist_ok=True)

# Save each layer's weights and biases
# Note: The keys might be named like "net.0.weight", "net.0.bias", etc.
weights_files = {
    "net.0.weight": "linear0_weight.csv",
    "net.0.bias": "linear0_bias.csv",
    "net.2.weight": "linear1_weight.csv",
    "net.2.bias": "linear1_bias.csv",
    "net.4.weight": "linear2_weight.csv",
    "net.4.bias": "linear2_bias.csv",
}

for key, filename in weights_files.items():
    # Convert tensor to list of lists
    tensor = state_dict[key]
    data = tensor.tolist()
    filepath = os.path.join(output_dir, filename)
    save_csv(filepath, data)
    print("Saved", key, "to", filepath)
