def load_csv(filename):
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                # Remove whitespace and newline characters
                stripped = line.strip()
                if stripped:
                    # Split by comma and convert each element to float
                    row = [float(val) for val in stripped.split(",")]
                    data.append(row)
    except Exception as e:
        print("Error reading file", filename, e)
    return data

# For vectors, you might want a flattened list:
def load_csv_vector(filename):
    d = load_csv(filename)
    # Assuming the CSV is written in a single row
    return d[0] if d and len(d) == 1 else d

# Adjust paths based on how you stored the files on the microcontroller.
w0 = load_csv("linear0_weight.csv")
b0 = load_csv_vector("/model_weights_csv/linear0_bias.csv")
w1 = load_csv("/model_weights_csv/linear1_weight.csv")
b1 = load_csv_vector("/model_weights_csv/linear1_bias.csv")
w2 = load_csv("/model_weights_csv/linear2_weight.csv")
b2 = load_csv_vector("/model_weights_csv/linear2_bias.csv")
