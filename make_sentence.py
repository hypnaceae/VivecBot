# Just an interface for markov.py with some error correction and basic functionality.
# GNU General Public License v3

import markov
import re


TRAINING_PATH = "./vivec.txt"
SAVE_PATH = "./gen_output.txt"

CHAIN_LENGTH = 3  # higher lengths increase computation cost; sentences will be closer to corpus
# 3 is a good balance between coherence and originality; around 8 most generated sentences will be identical
# to one in the corpus. Think of this as the N-gram parameter.

"""
import tweepy

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

try:
	api.verify_credentials()
	print("Authentication successful!")
except:
	print("Could not authenticate. Please check your keys.")
"""

def make_sentence():
	"""Generate a sentence from the corpus, using a Markov chain object."""
	obj = markov.Markov(TRAINING_PATH, CHAIN_LENGTH)
	sentence = (obj.generate_sentence())  # start with an initial sentence
	while len(sentence) >= 256:  # short sentences tend to be generated better
		sentence = obj.generate_sentence()
	while '"' in sentence:  # option to skip sentences with quotation marks, since they can be dodgy
		sentence = obj.generate_sentence()
	return error_correction(sentence)

def error_correction(phrase):
	"""Manual correction of some common errors in sentence generation."""

	sentence_final = phrase  # for non-destructive manipulation of input

	# append a trailing quotation mark if an orphaned one is found, unused if above skipping option in effect
	if re.search(r'( ".*\.)', sentence_final):
		sentence_final += '"'

	# some handling of post-punctuation quotation marks, unused if above skipping option in effect
	re.sub(r'(: " \w)', ': "', sentence_final)
	re.sub(r'(, " \w)', ', "', sentence_final)
	re.sub(r'(\? " \w)', '? "', sentence_final)

	# other manual corrections: punctuation and proper nouns are problematic
	if " 'i " in sentence_final:
		sentence_final = sentence_final.replace(" 'i ", " 'I ")
	if " : " in sentence_final:
		sentence_final = sentence_final.replace(" : ", ": ")
	if ",'" in sentence_final:
		sentence_final = sentence_final.replace(",'", ", '")
	if "? ' " in sentence_final:
		sentence_final = sentence_final.replace("? ' ", "?' ")
	if ". ' " in sentence_final:
		sentence_final = sentence_final.replace(". ' ", ".' ")
	if ': " ' in sentence_final:
		sentence_final = sentence_final.replace(': " ', ': "')
	if "! ' " in sentence_final:
		sentence_final = sentence_final.replace("! ' ", "!' ")
	if "- " in sentence_final:
		sentence_final = sentence_final.replace("- ", "-")
	if "almsivi" in sentence_final:
		sentence_final = sentence_final.replace("almsivi", "ALMSIVI")
	if "seht" in sentence_final:
		sentence_final = sentence_final.replace("seht", "Seht")
	if "ayem" in sentence_final:
		sentence_final = sentence_final.replace("ayem", "Ayem")
	if "vehk" in sentence_final:
		sentence_final = sentence_final.replace("vehk", "Vehk")
	if "hortator" in sentence_final:
		sentence_final = sentence_final.replace("hortator", "Hortator")
	if "nerevar" in sentence_final:
		sentence_final = sentence_final.replace("nerevar", "Nerevar")
	if ' " " ' in sentence_final:
		sentence_final = sentence_final.replace(' " " ', ' ')

	return sentence_final


def write_txt():
	"""Write an arbitrary number of generated sentences to a file"""
	n_to_write = 10
	with open(SAVE_PATH, "a") as write_file:
		for i in range(0, n_to_write):
			line = error_correction(make_sentence())
			write_file.write(line + "\n")
			print(i)
	write_file.close()


for i in range(0, 10):
	print(make_sentence())
