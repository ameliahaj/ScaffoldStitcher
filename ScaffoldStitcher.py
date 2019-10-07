import subprocess
import sys
import os.path
import textwrap
import argparse

#The ReadFasta class was created by Michael Graham, 10/1/2014
class ReadFasta():
    """
    Fasta reader utility class
    """
    
    def __init__(self,filename,identifier):
        """
        Constructor
        """
        self.filename = filename
        self.identifier = identifier
    
    def writeChromosomes(self):
        """
        Writes canonical chromosomes to stdout.
        """
        fastaFile = open(self.filename,'r')
        print('Writing chromosomes to output...', file=sys.stderr)
        for line in fastaFile:
            if self.identifier not in line:
                sys.stdout.write(line)
            else:
                break
        
    def openFasta(self):
        """
        Open fasta file. Returns Dictionary object of fasta entries.
        """
        
        self.writeChromosomes()
        
        self.fastaList = {}
        with open(self.filename) as fp:
            for name, seq in self.read_fasta(fp):
                if self.identifier in name:
                    self.fastaList[name] = seq
                else:
                    continue
        return self.fastaList

    def read_fasta(self,fp):
        """
        Read file line by line and separate sequences and headers
        """
        name, seq = None, []
        for line in fp:
            line = line.rstrip()
            if line.startswith(">"):
                if name: yield (name, ''.join(seq))
                name, seq = line, []
            else:
                seq.append(line)
        if name: yield (name, ''.join(seq))

class ScaffoldStitcher():
    """
    ScaffoldStitcher utility class.
    """
    def __init__(self,filename,identifier,minReadLength,nLength,maxLength):
        """
        Constructor
        """
        self.filename = filename
        self.identifier = identifier        
        self.minReadLength = minReadLength
        self.nLength = nLength
        self.maxLength = maxLength
    
    def concatenateScaffolds(self):
        """
        Concatenates unplaced scaffolds, separated by strings of Ns.
        """
    
        #Open file containing chromosomes + unplaced scaffolds. 
        #Run through the ReadFasta class in order to print out canonical chromosomes and generate a dictionary of scaffold sequences.
        print('Generating scaffold dictionary, please be patient...', file=sys.stderr)
        reader = ReadFasta(self.filename, self.identifier)
        inputFasta = reader.openFasta()
        
        #Create separate file to index scaffolds for later reference. File will be located in the same directory as the input file.
        outputPath = os.path.splitext(self.filename)[0]
        scaffoldIndex = open(outputPath + '_scaffold_index.txt', 'w')
        
        #Determine the number of scaffolds present in the input file
        lastOne = len(inputFasta)
        print('Scaffold count is...' + str(lastOne), file = sys.stderr)
        
        #Define an empty fakeChromString (scaffolds and N-strings will be added to this string)
        fakeChromString = ''
        #Define an empty list into which the headers for scaffolds shorter than the specified length will be placed
        eliminatedList = []
        
        #Generate scaffold spacer of specified length
        nString = ''
        x = 1
        while x <= self.nLength:
            nString += 'N'
            x+=1 
        print('Generated scaffold spacer...', file = sys.stderr)
               
        i = 0 #super-scaffold number
        j = 0 #position of unplaced scaffold in fake chromosome
        k = 0 #counter to know when we've hit the last scaffold in the dictionary
    
        for header in inputFasta:
        
            seq = inputFasta[header] #establish that the sequence is the value for each header in the dictionary
            k += 1 #increase scaffold number count by 1
            
            #If the scaffold sequence length is shorter than the specified minimum length, exclude it from the final output
            if len(seq) < int(self.minReadLength):
                print(header + ' was below the scaffold size cutoff...', file=sys.stderr)
                eliminatedList.append(header) #add header to list of eliminated scaffolds
                continue
                        
            else: 
                #Print progress to stderr
                print('Running for ' + header + ' (' + str(k) + ' of ' + str(lastOne) + ' scaffolds complete...)', file = sys.stderr)
                
                #If we're on the last scaffold and the super-scaffold is shorter than the max length...
                if k == lastOne and len(fakeChromString) + self.nLength + len(seq) < self.maxLength: 
                    scaffoldIndex.write('>Super_Scaffold' + str(i) + '\t' + str(j) + '\t' + header + '\n')
                    fakeChromString += nString + seq
                    
                    #Print super-scaffold to stdout as-is
                    sys.stdout.write('\n>Super_Scaffold' + str(i))
                    sys.stdout.write('\n' + fakeChromString)
                
                #If we're on the last scaffold and it would push the super-scaffold over the cutoff length...
                elif k == lastOne and len(fakeChromString) + self.nLength + len(seq) >= self.maxLength:
                    #Print existing super-scaffold to stdout
                    sys.stdout.write('\n>Super_Scaffold' + str(i))
                    sys.stdout.write('\n' + fakeChromString)
                
                    i += 1 #increase stitched scaffold number by 1
                    j = 0
                    
                    #Index this last scaffold
                    scaffoldIndex.write('>Super_Scaffold' + str(i) + '\t' + str(j) + '\t' + header + '\n')
                    
                    #Start a new super-scaffold containing only the last scaffold and then print it to stdout
                    fakeChromString = seq
                    sys.stdout.write('\n>Super_Scaffold' + str(i))
                    sys.stdout.write('\n' + fakeChromString)
                
                #If it's not the last scaffold and adding it to our super-scaffold would not push it over the max length...    
                elif len(fakeChromString) + self.nLength + len(seq) < self.maxLength :
                    if fakeChromString != '':
                        fakeChromString += nString #If the fake chromosome is empty, we don't need an N string
                    
                    #Add scaffold to super-scaffold
                    fakeChromString += seq
                
                    scaffoldIndex.write('>Super_Scaffold' + str(i) + '\t' + str(j) + '\t' + header + '\n')
                    j += 1
                
                #If it's not the last scaffold and adding it to our super-scaffold would push it over the max length...
                elif len(fakeChromString) + self.nLength + len(seq) >= self.maxLength:
                    #Print the existing super-scaffold to stdout
                    sys.stdout.write('\n>Super_Scaffold' + str(i))
                    sys.stdout.write('\n' + fakeChromString) #Print fake chromosome number
                
                    i += 1 #Increase super-scaffold number by 1
                    j = 0 #Reset position
                    scaffoldIndex.write('>Super_Scaffold' + str(i) + '\t' + str(j) + '\t' + header + '\n') #This will be the beginning of the next fake chromosome
                    
                    fakeChromString = seq #Instead of appending the scaffold to the super-scaffold, let this be the beginning of a new super-scaffold
                    j += 1
        
        #If any scaffolds were too short and were eliminated, indicate this in the scaffold index file:
        if len(eliminatedList) > 0:
            scaffoldIndex.write('\nScaffolds eliminated due to length shorter than ' + str(self.nLength) + ':')
        
        for item in eliminatedList:
            scaffoldIndex.write('\n' + item)
        
        print('Process complete.', file=sys.stderr)
        print('Your scaffold index file can be found at ' + outputPath + '_scaffold_index.txt.', file=sys.stderr)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Program to concatenate unplaced scaffolds.')
    parser.add_argument('-fasta', type=str, help='Input genome FASTA', required=True)
    parser.add_argument('-identifier', type=str, help='Scaffold string', required=True)
    parser.add_argument('-nlength', type=int, help='Length of scaffold spacer', required=False, default=1000)
    parser.add_argument('-maxlength', type=int, help='Maximum acceptable scaffold contig length', required=False, default=1500)
    parser.add_argument('-short', type=int, help='Minimum acceptable scaffold length', required=False, default=0)
    args = parser.parse_args()
    
    testClassObject = ScaffoldStitcher(args.fasta, args.identifier, args.short, args.nlength, args.maxlength)
    testClassObject.concatenateScaffolds()