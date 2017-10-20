from PIL import Image
import numpy as np

rule = int(input("Rule please: "))
random_initial_condition = True
time_steps = 1000
width = 1000
point_size = 2

print(rule)

def flatten(items, seqtypes=(list, tuple)):
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i+1] = items[i]
    return items

def apply_rule_to_cell(rule, left, center, right):
	index = 4*left+2*center+right
	ret = int(rule[7 -index])
	return ret

def generate_tape(n):
	left = [0 for _ in range(int(n/2))]
	middle = 1
	right = [0 for _ in range(int(n/2))]
	tape = left.copy()
	tape.append(middle)
	tape.append(middle)
	for i in right:
		tape.append(i)
	return tape

def make_data(rule, time_steps, width, random=False):
	if random:
		my_tape = np.random.randint(0, 2, size=(width, 1)).round().tolist()
		tape = flatten(my_tape)
	else:
		tape = generate_tape(width)
	memory = [tape]
	next_gen = tape.copy()
	for t in range(time_steps):
		for i, cell in enumerate(tape[1:-1]):
			next_gen[i] = apply_rule_to_cell(rule, tape[i - 1], tape[i], tape[i + 1])
		tape = next_gen.copy()
		memory.append(tape)
	return memory

def main(rule, random_initial_condition, time_steps, width, point_size):
	rule = '{0:08b}'.format(rule)
	memory = make_data(rule, time_steps, width, random=random_initial_condition)
	img = Image.new('RGB', (point_size*width, point_size*time_steps), "white")
	pixels = img.load()
	for i in range(img.size[0]):    # for every pixel:
		for j in range(img.size[1]):
			value = memory[j//point_size][i//point_size]
			value = not value
			value*=255
			pixels[i,j] = (value, value, value)
	img.show()

if __name__ == '__main__':
	main(rule, random_initial_condition, time_steps, width, point_size)
