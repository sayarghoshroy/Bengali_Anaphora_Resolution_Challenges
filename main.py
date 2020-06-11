# Enter a Valid Sentence to Run Test
# Else, receive statistics from the given

import re
import string

file_handler = open("bengali_sentences_with_pos.txt")
file_string = file_handler.read()

sentences = file_string.split('\n')

experiment_size = 10000000000

singular_pronouns = ["তুমি", "তুই", "সে", "আপনি", "তিনি", "তার", "তোমার", "তোর", "আপনার", "আমার", "ওর"]
plural_pronouns = ["তোমরা", "তোরা", "তারা", "আপনারা", "তোমাদের", "তোদের", "আপনাদের", "আমাদের", "ওদের"]

first_person_pronouns = ["আমি", "আমার"]
second_person_pronouns = ["তুমি", "তুই", "আপনি", "তোমার", "তোর", "আপনার"]
third_person_pronouns = ["সে", "তিনি", "তার", "তারা", "ওদের", "ওর"]

status_formal = ["আপনি", "তিনি", "আপনার", "আপনারা", "আপনাদের"]
status_informal = ["তুমি", "সে", "তার", "তোমার", "তোমরা", "তোমাদের"]
status_close = ["তুই", "তোর", "তোরা", "তোদের", "ওদের", "ওর"]

test_set = ["রাম/NP/S/T/I বই/NN/S/T/I পড়ছে/VB/S/T/I । সে/PRP/S/T/I খুব/JJ/S/T/I ভালো/JJ/S/T/I ।",
			"জুবের/NP/S/T/I একটি/QT/S/T/I বল/NN/S/T/I নিয়ে/VB/S/T/I খেলছে/VB/S/T/I । সেটি/PRP/S/T/I গোলাকার/JJ/S/T/I ।",
			"অভিজ্ঞানরা/NP/P/T/I দার্জিলিং/NP/S/T/I বেড়াতে/VB/S/T/I গেছে/VB/S/T/I । তারা/PRP/P/T/I পরশু/NN/S/T/I ফিরবে/VB/P/T/I ।",
			"শেলি/NP/S/T/I ছবি/NN/S/T/I আঁকছে/VB/S/T/I । সেটি/PRP/S/T/I রঙিন/JJ/S/T/I । ",
			"রামবাবু/NP/S/T/F সমাজের/NN/S/T/I মাথা/NN/S/T/I । ওনাকে/PRP/S/T/F সকলে/QT/P/T/I ভয়/JJ/S/T/I পায়/VB/S/T/I । ",
			"রাম/NP/S/T/I আর/CONJ/S/T/I যদু/NP/S/T/I গান/NN/S/T/I করছে/VP/S/T/I । তারা/PRP/P/T/I ভালো/JJ/S/T/I গান/NN/S/T/I গায়/VB/S/T/I । ",
			"বাঁদরটি/NN/S/T/I নাচ/VB/S/T/I করছিলো/VB/S/T/I । তা/PRP/S/T/I দেখে/VB/S/T/I ছেলেটি/NN/S/T/I খুশি/JJ/S/T/I হলো/VAUX/S/T/I । ",
			"রামের/NP/S/T/I বাড়ি/NN/S/T/I কলকাতায়/NP/S/T/I । সেটা/PRP/S/T/I দেখতে/VB/S/T/I বহু/JJ/P/T/I লোক/NN/S/T/I যায়/VB/S/T/I । ",
			"পাখির/NN/S/T/I বাসা/NN/S/T/I গাছে/NN/S/T/I । সেটির/PRP/S/T/I রং/NN/S/T/I নীল/NN/S/T/I । ",
			"বাড়ির/NN/S/T/I ওপর/POST/S/T/I দিয়ে/VAUX/S/T/I বিমান/NN/S/T/I উড়ে/VB/S/T/I গেল/VAUX/S/T/I । সেটির/PRP/S/T/I গতি/NN/S/T/I বিশাল/JJ/S/T/I । " ]

sentence_set = []
for tester in test_set:
	tokens = tester.split(' ')
	sentence_string = ""
	for token in tokens:
		word = token.split('/')[0]
		sentence_string = sentence_string + word + " "
	sentence_set.append(sentence_string.strip())

def number(c):
	# Feature Encoding for Number Agreement
	if c == 'S':
		return "Singular"
	elif c == 'P':
		return "Plural"

def person(c):
	# Feature Encoding for Person Agreement
	if c == 'T':
		return 'Third'
	elif c == 'S':
		return 'Second'
	elif c == 'F':
		return 'First'

def honorific(c):
	# Feature Encoding for Honorific Agreement
	if c =='I':
		return "Informal"
	elif c == 'C':
		return "Close"
	elif c == 'F':
		return "Formal"

def extract(unit):
	# Extracts features from a Tagged Unit
	listed = unit.split('/')
	diction = {}

	if len(listed) == 1:
		# has not been untagged
		diction['word'] = "NULL"
		diction['POS'] = "SYM"
		diction['number'] = "NULL"
		diction['person'] = "NULL"
		diction['honor'] = "NULL"

	else:
		# has been tagged
		diction['word'] = listed[0]
		diction['POS'] = listed[1]
		diction['number'] = number(listed[2])
		diction['person'] = person(listed[3])
		diction['honor'] = honorific(listed[4])
	
	return diction

def process(sentence):
	# Process a Tagged Sentence
	tokens = sentence.split(' ')
	sentence_features = []
	for token in tokens:
		temp_dict = extract(token)
		sentence_features.append(temp_dict)
	return sentence_features

def identify_pronouns(feature_sentence):
	# Identify the pronominal anaphor for disambiguation
	for item in feature_sentence:
		if item['POS'] == 'PRP':
			return item

def indentify_antecedents(feature_sentence):
	# Identify the possible antecedents for the pronoun
	possible_antec = []
	for elem in feature_sentence:
		if elem['POS'] == 'PRP':
			break
		if elem['POS'] == 'NN' or elem['POS'] == 'NP':
			possible_antec.append(elem)
	return possible_antec

def disambiguate(pronoun, antecs):
	person = 0
	if pronoun in third_person_pronouns:
		person = 3
	elif pronoun in second_person_pronouns:
		person = 2
	elif pronoun in first_person_pronouns:
		person = 1

	formal_level = 0
	if pronoun in status_formal:
		formal_level = 3
	elif pronoun in status_informal:
		formal_level = 2
	elif pronoun in status_close:
		formal_level = 1

	number = 0
	if pronoun in singular_pronouns:
		number = 1
	elif pronoun in plural_pronouns:
		number = 2
	else:
		number = -1

	if number == -1:
		# Not found in List, Use tagged features
		if pronoun['number'] == 'Singular':
			number = 1
		elif pronoun['number'] == 'Plural':
			number = 2

		if pronoun['person'] == 'Third':
			person = 3
		elif pronoun['person'] == 'Second':
			person = 2
		elif pronoun['person'] == 'First':
			person = 1

		if pronoun['honor'] == 'Informal':
			formal_level = 2
		elif pronoun['honor'] == 'Formal':
			formal_level = 3
		elif pronoun['honor'] == 'Close':
			formal_level = 1

	# Primary Features Allotted

	# By default, let it refer to a Person
	person_reference = 1
	if pronoun['word'].endswith("টা") or pronoun['word'].endswith("টি") or pronoun['word'].endswith("টির"):
		# Does not refer to a person
		person_reference = 0

	ruled_out_set = []

	# Rule out antecedents
	for elem in antecs:
		# Reference type constraint
		if elem['POS'] == 'NP' and person_reference == 0:
			continue
		if elem['POS'] == 'NN' and person_reference == 1:
			continue

		# Constraint on Number
		if elem['number'] == 'Singular' and number == 2:
			continue
		if elem['number'] == 'Plural' and number == 1:
			continue

		# Constraint on Person
		if elem['person'] == 'Third' and person != 3:
			continue
		if elem['person'] == 'Second' and person != 2:
			continue
		if elem['person'] == 'First' and person != 1:
			continue

		# Honorific Constraint
		if elem['honor'] == 'Formal' and formal_level != 3:
			continue
		if elem['honor'] == 'Informal' and formal_level != 2:
			continue
		if elem['honor'] == 'Close' and formal_level != 1:
			continue

		ruled_out_set.append(elem)

	# List of antecedents processed

	print("Pronominal Anaphor : ", pronoun)
	print("Set of Possible Antecedents : ", antecs)

	if len(ruled_out_set) == 1:
		print("Identified Antecedent : ", ruled_out_set[0])

	elif len(ruled_out_set) == 0:
		print("None of the Antecedents fit the Constraints")

	else:
		print("Following Antecedents are Possible : ", ruled_out_set)


input_string = input()

print(input_string)

if input_string.strip() in sentence_set:
	# Run the experiment on the input sentence
	index = 0
	
	for elem in sentence_set:
		if elem in input_string or input_string in elem:
			break
		index = index + 1

	unprocessed_sentence = test_set[index]

	feature_sentence = process(unprocessed_sentence)
	# Sentence with feature mapping created

	pronoun = identify_pronouns(feature_sentence)
	# Pronominal Anaphor with features extracted
	antecs = indentify_antecedents(feature_sentence)
	# List of Antecedents for Disambiguation
	disambiguate(pronoun, antecs)


else:
	# Run the experiment on the corpus
	
	antec = 0
	no_antec = 0

	count = 0

	for sentence in sentences:
		if count > experiment_size:
			break

		word_list = sentence.split(' ')

		word_tagged_list = []
		for word in word_list:
			if '/' not in word:
				break
			meta = word.split('/')
			word_tagged_list.append(meta)
			
			#stores [ word_text, word_tag ] pairs in the list

		if_pronoun = 0
		max_index = -1
		possible_antecedents = []

		for word in word_tagged_list:
			max_index = max_index + 1
			if 'PRP' in word[1]:
				if_pronoun = 1
				index = -1
				for pair in word_tagged_list:
					index = index + 1
					if index == max_index:
						break
					if '_NN' in pair[1]:
						temp = []
						temp.append(pair[0])
						temp.append(pair[1])
						temp.append(index)
						possible_antecedents.append(temp)
				break

		if if_pronoun:
			if possible_antecedents == []:
				no_antec = no_antec + 1
			else:
				antec = antec + 1
			print("Pronominal Anaphor : ", word_tagged_list[max_index], "; Possible Referents in Vicinity : ", possible_antecedents)
		
		count = count + 1

	print("# Sentences Processed : ", count)
	print("# Pronominal Anaphors Detected : ", (antec + no_antec))
	print("# With possible Antecedents in Vicinity : ", antec)
	print("# Without possible Antecedents in Vicinity : ", no_antec)