# Authors:      Joel MacVicar 
# Date Updated: 5/9/2025
# Name :        remoteMLControl.py
# Purpose:      A controller class to implement the weights and bias from our ML Model.
import gc
class remoteMLControl:
    def __init__(self):
        self.b0, self.w0 = [], []
        self.b1, self.w1 = [], []
        self.b2, self.w2 = [], []
        self.mean = []
        self.std = []

        folder = 'remoteMLControl/modelWeights'

        def load_vector(file_path, is_matrix=True):
            result = []
            with open(file_path, 'r') as f:
                for line in f:
                    row = [float(x) for x in line.strip().split(',') if x.strip() != '']
                    if is_matrix:
                        result.append(row)
                    else:
                        result.extend([[val] for val in row])
            return result

        files_to_load = [
            ('linear0_bias.txt', self.b0, False),
            ('linear0_weight.txt', self.w0, True),
            ('linear1_bias.txt', self.b1, False),
            ('linear1_weight.txt', self.w1, True),
            ('linear2_bias.txt', self.b2, False),
            ('linear2_weight.txt', self.w2, True),
            ('mean.txt', self.mean, False),
            ('std.txt', self.std, False)
        ]
        gc.collect() #help with loading in the large weight files
        for fname, target_list, is_matrix in files_to_load:
            file_path = f'{folder}/{fname}'
            try:
                target_list.extend(load_vector(file_path, is_matrix=is_matrix))
            except Exception as e:
                print(f'Error reading {file_path}: {e}')

        self.mean = [x[0] for x in self.mean]
        self.std = [x[0] for x in self.std]
        self.debug_shapes()

    def debug_shapes(self):
        def print_shape(name, data):
            try:
                if isinstance(data[0], list):
                    row_lengths = set(len(row) for row in data)
                    print(f"{name}: {len(data)} rows, row lengths: {row_lengths}")
                    if len(row_lengths) > 1:
                        print(f" Inconsistent row lengths in {name}")
                else:
                    print(f"{name}: {len(data)} elements (flat list)")
            except IndexError:
                print(f"{name}: EMPTY")

        print("===== Model Weights and Vectors Shape Check =====")
        print_shape("b0", self.b0)
        print_shape("w0", self.w0)
        print_shape("b1", self.b1)
        print_shape("w1", self.w1)
        print_shape("b2", self.b2)
        print_shape("w2", self.w2)
        print_shape("mean", self.mean)
        print_shape("std", self.std)
        print("=================================================")


    def standardize(self, inputs):
        return [(inputs[i] - self.mean[i]) / self.std[i] for i in range(len(inputs))]

    def MLPred(self, inputs):
        normInputs = self.standardize(inputs)

        # Layer 0
        z0 = []
        for i in range(len(self.b0)):
            temp = self.b0[i][0]
            for j in range(len(normInputs)):
                temp += normInputs[j] * self.w0[i][j]
            z0.append(temp)

        # Layer 1
        z1 = []
        for i in range(len(self.b1)):
            temp1 = self.b1[i][0]
            for j in range(len(z0)):
                temp1 += z0[j] * self.w1[i][j]
            z1.append(temp1)

        # Layer 2
        z2 = []
        for i in range(len(self.b2)):
            temp2 = self.b2[i][0]
            for j in range(len(z1)):
                temp2 += z1[j] * self.w2[i][j]
            z2.append(temp2)

        return z2
