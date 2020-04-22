class Circuit:

	def __init__(self, path):
		with open(path, "r") as f:
			data = f.read()
		self.operations, self.output_indexes, self.tape_len = self.__load_bristol_circuit(data)

	def evaluate(self, inputs):
		tape = [None for _ in range(self.tape_len)]
		tape[0] = 0
		tape[1] = 1
		for i in range(len(inputs)):
			tape[i+2] = inputs[i]
		for gate in self.operations:
			if len(gate) != 4:
				raise ValueError(f"Improperly formatted gate: {gate}")
			if gate[-1] == 'XOR':
				tape[gate[-2]] = tape[gate[-3]]^tape[gate[-4]]
			elif gate[-1] == 'AND':
				tape[gate[-2]] = tape[gate[-3]]&tape[gate[-4]]
			else:
				raise ValueError(f"Improperly formatted gate: {gate}")
		return [tape[k] for k in self.output_indexes]

	def __load_bristol_circuit(self, data):
		lines = data.split("\n")
		last_index = int(lines[0].split()[-1])
		outputs = [int(i) for i in lines[2].split() if i!='']
		n_outputs = outputs[1] if len(outputs)==2 else outputs[1]+outputs[2]
		output_indexes = list(range(last_index-n_outputs+2, last_index+2))
		lines = lines[4:]
		max_idx = 0
		ops = []
		for l in lines:
			words = l.split()
			if len(words) < 2:
				pass		
			elif words[-1] == 'EQW':
				for i in range(len(outputs)):
					if outputs[i] == int(words[-2])+2:
						outputs[i] = int(words[-3])+2
			elif words[-1] == 'AND' or words[-1] == 'XOR':
				ops.append((int(words[-4])+2, int(words[-3])+2, int(words[-2])+2, words[-1]))
			elif words[-1] == "INV":
				ops.append((int(words[-3])+2, 1, int(words[-2])+2, 'XOR'))
			else:
				raise ValueError("Improperly formatted circuit")
			if int(words[-2]) + 2 > max_idx:
				max_idx = int(words[-2]) + 2

		return ops, output_indexes, max_idx+1
