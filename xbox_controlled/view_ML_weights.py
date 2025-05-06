import torch

# Load the saved state dict
state_dict = torch.load("motor_effort_model.pth")

# Print all parameters (layer name and tensor values)
print("🔍 Model Parameters:\n")

for name, param in state_dict.items():
    print(f"Layer: {name}")
    print(f"Shape: {param.shape}")
    print(f"Values:\n{param}\n")
    print("-" * 50)
