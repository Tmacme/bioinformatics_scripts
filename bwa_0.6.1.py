#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os

__author__ = "Raony Guimarães"
__copyright__ = "Copyright 2011, The Exome Pipeline"
__credits__ = ["Raony Guimarães"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Raony Guimarães"
__email__ = "raonyguimaraes@gmail.com"
__status__ = "Production"
		
#run example
#python bwa.py -f reads1.fastq -q reads2.fastq

parser = OptionParser()
usage = "usage: %prog [options] -f reads1.fastq -q reads2.fastq"
parser = OptionParser(usage=usage)

parser.add_option("-f", dest="reads1",
                  help="reads 1 in FASTQ format", metavar="FASTQ")
parser.add_option("-q", dest="reads2",
                  help="reads 2 in FASTQ format", metavar="FASTQ")
#parser.add_option("-l", dest="ill",
                  #help="Illumina", metavar="FASTQ Illumina1.3+")
                  
(options, args) = parser.parse_args()


reads1=options.reads1
reads2=options.reads2
#ill = options.ill


#variables

bwa_dir="/lgc/programs/bwa-0.6.1"
st_dir="/lgc/programs/samtools"
reference="/lgc/datasets/gatk_data/b37/human_g1k_v37.fasta"

class Bwa():
    def __init__(self, reads1, reads2):
      """Returns new Sequence object with specified data, Name, Alphabet.
      Note: if Alphabet is None, performs no validation.
      """
      
      #global fastqx
      
      #fastqx="../../bin/fastqx/bin/"
      
      #create folders
      #os.system("mkdir alignment")
      
      print "Start Analysis..."
      self.alignment()
      self.sai_to_sam()
      self.sam_to_bam()
      #self.clean_files()
      
      
    def alignment(self):
      
      print "Aligning reads..."
      
      command = "%s/bwa aln -t 24 -I %s %s > reads1.sai" % (bwa_dir, reference, reads1)
      os.system(command)
      command = "%s/bwa aln -t 24 -I %s %s > reads2.sai" % (bwa_dir, reference, reads2)
      os.system(command)
      
    def sai_to_sam(self):
      print "Convert Sai to SAM"
      command = """%s/bwa sampe %s -r "@RG\tID:Exome\tLB:Exome\tSM:Exome\tPL:ILLUMINA" reads1.sai reads2.sai %s %s > exome.sam""" % (bwa_dir, reference, reads1, reads2)
      os.system(command)
    def sam_to_bam(self):
      print "Convert SAM to BAM"
      #import BAM
      command = "%s/samtools view -bS exome.sam > exome.bam" % (st_dir)#, reference
      #samtools view -bS sample.sam > sample.bam
      #samtools import %s exome.sam exome.bam
      os.system(command)
      # #Sort BAM
      command = "%s/samtools sort exome.bam exome.sorted" % (st_dir)
      os.system(command)
      # #Index BAM
      command = "%s/samtools index exome.sorted.bam exome.sorted.bam.bai" % (st_dir)
      os.system(command)
      #Calmd
      #command = "%s/samtools calmd -Abr exome.sorted.bam %s > exome.baq.bam" % (st_dir, reference)
      #os.system(command)
      
    def clean_files(self):
      command = "rm exome.sam exome.bam reads1.sai reads2.sai" % (st_dir)
      os.system(command)
      command = "mv exome.sorted.bam exome.bam" % (st_dir)
      os.system(command)
      command = "mv exome.sorted.bam.bai exome.bam.bai" % (st_dir)
      os.system(command)
      

if __name__ == '__main__': 
  Bwa(reads1, reads2)
