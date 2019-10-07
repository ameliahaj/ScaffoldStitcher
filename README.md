[![DOI](https://zenodo.org/badge/213423835.svg)](https://zenodo.org/badge/latestdoi/213423835)

# Introduction 
ScaffoldStitcher is a Python tool that concatenates unplaced scaffolds into chromosome-sized super-scaffolds for use with GATK Haplotype Caller. Often, when a reference FASTA file contains too many unplaced scaffolds, Haplotype Caller is unable to handle the number of sequences. Stitching scaffolds together, separated by sufficiently long strings of Ns so that reads don't map across multiple scaffolds, circumvents this known issue.

# Installation
ScaffoldStitcher is a Python script that requires Python 3 to run. The latest version of Python can be downloaded at https://www.python.org/downloads/. No other software is required to use ScaffoldStitcher.

# Inputs and outputs
ScaffoldStitcher takes an input FASTA file with all canonical chromosomes listed first, followed by scaffold sequences, and outputs a FASTA file in which the scaffold sequences have been concatenated together, separated by a specified number of Ns so that no reads map across more than one scaffold.

**Required inputs**

*-fasta*: Path to input FASTA file.

*-identifier*: String unique to the headers of scaffold sequences, but not found in chromosome sequence headers (for instance, "Scaffold" or "NW"). Does not require quotation marks.

**Optional inputs**

*-short*: Minimum allowable length of scaffolds; scaffolds below the specified length will not be included in the final output FASTA file. (Default = 0.)

*-nlength*: Length of spacer between scaffolds, should be longer than your longest sample read length. (Default = 1000.)

*-maxlength*: Desired length of concatenated scaffold strings, ideally approximately the size of a regular chromosome. (Default = 200,000,000.)

**Outputs**

ScaffoldStitcher produces two outputs:

1. A scaffold index file, automatically generated and written to the same folder containing your input FASTA file. This is a tab-delimited .txt file of the original scaffold names, with their position in the newly generated concatenated scaffolds. 
2. Your new FASTA with original chromosomes left intact, followed by concatenated scaffolds. This is written to stdout, so it is recommended that you specify an output file path.

A progress report prints to stderr.

#How to run ScaffoldStitcher
ScaffoldStitcher runs in the command line, and only requires that Python3 be installed. If you have more than one version of Python installed, you may need to specify "python3" in order to run the tool. There are no other dependencies.

```$ python [path to ScaffoldStitcher.py] -fasta [path to FASTA file] -identifier [string unique to scaffold headers] *-options* > [path to output file]```

For a more detailed description of how to use ScaffoldStitcher, please see the quick start guide.
