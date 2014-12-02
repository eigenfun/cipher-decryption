This is a python application for deciphering substitution encryption. 
It uses word statistics from an open corpus to infer words in the encrypted messages and thus arrive at the substitution cipher.

The repository contains:

Python Source Code:
   	  - decode.py (entry point for the implementation)
   	  - corpus.py, cipher.py (helper classes)
   	  - textutil.py (module with useful text manipulation functions)
   	  - solver.py (the main class implementing the decoding algorithm)

   	  Test:
   	  - testdecode.py (a test suite that runs the decoding algorithm on two additional test data)
   	  - ./data/quotes.txt, ./data/raven.txt (two plain text files used for testing the robustness of the code)
   	  - ./data/quotes.txt-enc, ./data/raven.txt-enc (randomly encoded versions of the two pain text data files)

   	  Result:
   	  - decoded.txt (a decoded version of the encoded-en.txt from a sample run)
   	  - decryption_cipher.txt (character mapping char_encoded -> char_plain that was computed by the code and used to decode the encoded file)
   	  - encryption_cipher.txt (character mapping char_plain -> char_encoded that was used to encrypt the plain text)

   	  
To run the code:

      You can run the code on the command line with default settings simply by invoking (from the root directory):

   	  		python ./decode.py

   	  This assumes all the input files to be present in the current directory, and writes the output files as mnetioned above.

   	  Optionally, you can specify the input files (corpus and encoded files) as follows:

   	    	python decode.py ./data/corpus-en.txt ./data/quotes.txt-enc

   	  You can also run the test code (that uses two test data set in the ./data directory) directly:

   	  		python testdecode.py
