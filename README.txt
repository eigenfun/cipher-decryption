The goal of this problem is to write a program that decrypts a set of
Tweets that have been encrypted with a simple substitution cipher.

Input Data
----------
You have been given two data files. 

"encoded-en.txt" is a set of short messages (e.g. Tweets) in English,
where each has been encrypted using a simple substitution cipher. Such
a cipher works by replacing all occurrences of a character with a
different (randomly selected, but consistent) character. The
substitution is not case sensitive. 

For example:

Original message: "Hello world."
Encrypted message: "Lkccz mzfca."

Cipher:
d -> a
e -> k
h -> l
l -> c
o -> z
r -> f
w -> m

For this problem white space and punctuation are not substituted.

"corpus-en.txt" is a corpus of English text consisting of the contents
of a number of books.


Your Program
------------
We prefer that you code this in python.  If you would like to submit
solutions in other programming languages, we will certainly read them.
Language nimbleness is an important skill.  If non-standard libraries
are required to run the solution you need to provide them (ideally
none).

Your program should be runnable from the command line and output at
least two things:

(1) The decryption cipher (i.e. the inverse mapping of encoded
character back to original), in a single text file with the format:

<encrypted> -> <decrypted>
...

for each character. No header row, thus there should be 26 rows (one
for each English letter).

e.g.
a -> z
b -> y
c -> x
...
z -> a

(2) The original Tweets decrypted based on this decryption cipher.
This should be in a single text file, following the same formatting as
the encrypted messages provided.


You should submit at the conclusion of the exercise:

- All code written

- Example output files as specified above

- Any supplementary files (e.g. tests, data)

- A brief write-up explaining your approach, how well it worked, what
  further avenues you might explore given time, along with any
  necessary instructions on how to run the code. Specify the language
  version if important to running the solution.



Important Notes
---------------

In addition to evaluating the simplicity and cleverness of your
technical approach, we also give marks for ease of use, engineering
hygiene, craftmanship & style.

Correct solutions get the reverse cipher without fail.  That is,
programs should *not* require repeated manual operation to eventually
get a valid reverse cipher.

Your program should be sufficiently generalized that it can be run on
*other* input files, or even incorporated into a larger system.  We
want to see how you organize the interface to your algorithm.

Pythonic style counts.  `pip install pylint` and aim for >8.  Use the
python standard library.
