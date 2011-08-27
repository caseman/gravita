import random
import pkg_resources

random = random.Random()
tables = {}


def load(filename):
	if filename not in tables:
		start_table = []
		word_counts = []
		letter_counts = []
		combos_table = {}
		for line in pkg_resources.resource_stream(__name__, filename):
			line = line.strip().lower()
			start_table.append(line[0])
			word_counts.append(len(line.split()))
			letter_counts.append(len(line))
			for i, letter in enumerate(line):
				if i < 1:
					last_letter = ' '
				else:
					last_letter = line[i-1]
				if (i+1) >= len(line):
					next_letter = ' '
				else:
					next_letter = line[i+1]
				combos_table.setdefault(last_letter + letter, []).append(letter + next_letter)

		tables[filename] = (start_table, word_counts, letter_counts, combos_table)
	return tables[filename]


def generate(filename, max_words=None, max_letters=None):
	start_table, word_counts, letter_counts, combos_table = load(filename)

	word_count = 0
	if max_words is None:
		max_words = random.choice(word_counts)
	if max_letters is None:
		max_letters = random.choice(letter_counts)

	letters = ' ' + random.choice(start_table)
	while word_count < max_words and len(letters) < max_letters:
		key = letters[-2:]
		if not combos_table.has_key(key):
			break
		letters += str(random.choice(combos_table[key])[-1])
		if letters[-1] == ' ':
			word_count += 1

	return letters.strip().title()

