#Installation and configuration
**1.** First ensure that you have Python 3 installed. You can check whether you have Python installed, and if so, which version of Python you have by typing ```python``` into the command line and hitting enter. If you are running Python 2, you will need to install Python 3. The latest version can be found at https://www.python.org/downloads/.

**2.** Download ScaffoldStitcher.py. 

#Acquire test data
**3.** Download the small test file included here, titled "ScaffoldStitcher_test.fa". This file contains 4 chromosomes (identified by 'chr') and 16 scaffold sequences (identified by 'scaffold').

#Running ScaffoldStitcher
 **4.** Generate a file with chromosomes left intact and the 16 scaffolds reduced to 3 super-scaffolds. Type the following into the command line: 
 
 ```python ScaffoldStitcher.py -fasta ScaffoldStitcher_test.fa -identifier scaffold -nlength 210 -maxlength 1500 -short 70 > ScaffoldStitcher_output.fa```
 
 *Notes: if you have both Python 2 and Python 3 installed, you may need to specify python3 rather than simply python. If you are running the script in a folder other than the folder containing the ScaffoldStitcher script and test file, you will need to specify the full file path to each.*
 
 **5.** Watch the terminal – progress notes will appear as each step is being performed. Because the test file we've provided is so small, this will happen very quickly (well under one second). For a several-gigabyte file, expect the program to complete in a couple of minutes.
 
#Results
**6.** The ```ScaffoldStitcher_output.fa``` file will contain your original chromosomes, followed by 3 super-scaffolds containing all 16 short scaffolds, separated by strings of Ns 210 characters long. No super-scaffold will be longer than the specified 1500 characters long.

**7.** The ```ScaffoldStitcher_test_scaffold_index.txt``` file contains a tab-delimited record of which scaffold was placed into which super-scaffold, with its position (first, second, third, etc) in the  super-scaffold:

	[New scaffold name]	[Position]	[Original scaffold name]
	
At the end of the file, you can find a list of scaffolds eliminated due to length shorter than the desired length. In this test case, you should see that scaffolds 19 and 20 were left out of the final output.
 
 

 
 