# VivecBot
Quick script for probabilistic (Markov chain) generation of semi-sensical text based on a given corpus, using MarkoviPy.

`vivec.txt` contains the full text of The 36 Lessons of Vivec, a series of esoteric in-game books written by Michael Kirkbride for The Elder Scrolls: Morrowind (2002).

### Usage:

Running the script prints 10 sentences to console, based on whichever corpus `TRAINING_PATH` points to. There is also a pre-written function `write_txt()` which you can edit to your needs and call, which just writes the sentences to a file.

Of interest is the variable `CHAIN_LENGTH`. Higher integer values increase computation time, and the resulting generated sentences are more likely to be found in the corpus itself. A Markov chain length of 3 seems to be a good middle-ground, producing mostly legible original sentences.

#### TODO:

Actually hook it up to the twitter account (https://twitter.com/VivecBot) to tweet the generated sentences.
