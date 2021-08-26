VusPrize - Variants of Uncertain Significance Prioritization Random Forest
Version 0.0.1 (22-11-2020)
===========================================================================

VusPrize provides a random forest model to prioritize variants of uncertain
significance as Pathogenic or Not Pathogenic. VusPrize performs an accurate
prediction of the probability of pathogenicity of a variant for variant 
interpretation pipelines for research purposes. 

Before using VusPrize, you need to process your vcf variants file on the
Ensembl Variant Effect Predictor (VEP) and dowload the results file as a csv
file. 


As an input, you need to provide a tab separated csv file that includes
the following columns: 'Location', 'Allele', 'SYMBOL', 'Consequence',
ada_score','AF','BLOSUM62','CADD_PHRED','codon_degeneracy',
'Eigen-pred_coding','GERP++_RS',  'integrated_fitCons_score', 'LoFtool', 'phyloP100way_vertebrate', 'SIFT'. This file is obtained as the standard 
output from VEP with a txt/csv format.

This file can be generated in the VEP command line tool using the following command:

./vep --af --appris --buffer_size 500 --check_existing --distance 5000 --mane --pick --plugin MaxEntScan,[path_to]/maxentscan --plugin Blosum62 --plugin dbNSFP,[path_to]/dbNSFP4.1a_grch37.gz,codon_degeneracy,Eigen-phred_coding,integrated_fitCons_score,GERP++_RS,phyloP100way_vertebrate --plugin dbscSNV,[path_to]/dbscSNV1.1_GRCh37.txt.gz --plugin LoFtool,[path_to]/LoFtool_scores.txt --plugin CADD,[path_to]/CADD_GRCh37_1.6_whole_genome_SNVs.tsv.gz,[path_to]/CADD_GRCh37_1.6_InDels.tsv.gz --refseq --regulatory --sift p --species homo_sapiens --symbol --transcript_version --tsl --cache --input_file [input_data] --output_file [output_file] --port 3337


The output of the VusPrize tool is a tab separated csv file with the following 
columns: 'Location', 'Allele', 'SYMBOL', 'Consequence', 'Prediction', 
'Probability of Pathogenicity'.
The Probability column states the Probability of Pathogenicity of the variant
from 0 to 1, obtained by the proportion of random forest. The predicted class probabilities of a variant are computed as the mean predicted probabilities of 
the Pathogenic class of the trees in the forest. The class probability of a 
single tree is the fraction of samples of the same class in a leaf.

--------------------
Running VusPrize
--------------------

VusPrize is available as an application on Python 3.7.5 To run it 
succesfully,it is required to have the following libraries installed:
Pandas 0.25.3
Sklearn 0.21.3
Joblib 0.14.0

It is advised to run the python application and the jupyter notebooks of the tool training in a dedicated conda environment.
You can create a dedicated environment from the vusprizecondaenv.yml file.
Go to the directory where you have stored the vusprizecondaenv.yml file. 
Run: conda env create -n vusprize -f vusprizecondaenv.yml
Then: conda activate vusprize


The RF_niu.joblib file is provided and must be located in the same directory as 
the VusPrize.py file.

USAGE:

python VusPrize.py <input_file> <output_file>

--------------------
VCF Benchmark Files
--------------------

The following files are included in the VCF_Files folder:

clinvar_VUS.vcf.gz  Variants classified as VUS in ClinVar on August 08th 2020
clinvar_exVUS_pathogenic.vcf.gz Variants that were VUS but had been reclassified as Pathogenic with at least two gold stars in ClinVar on August 08th 2020
clinvar_exVUS_benign.vcf.gz Variants that were VUS but had been reclassified as Pathogenic with at least two gold stars in ClinVar on August 08th 2020
clinvar_pathogenic.vcf.gz Variants classified as Pathogenic in ClinVar on August 08th 2020
clinvar_benign.vcf.gz Variants classified as Benign in ClinVar on August 08th 2020

--------------------
VEP Annotated Benchmark Files
--------------------

The following CVS files (included in the Training folder) are the Ensembl-VEP annotated versions of the VCF files and were used to train and test the model(s): 

EXVUS_BEN_2020.txt  VEP annotated variants formerly classified as VUS but reclassified as Benign in ClinVar on August 08th 2020 in CSV format
EXVUS_PAT_2020.txt VEP annotated variants formerly classified as VUS but reclassified as Pathogenic in ClinVar on August 08th 2020 in CSV format
BEN_2020.txt  VEP annotated variants classified as Benign in ClinVar on August 08th 2020 in CSV format
PAT_2020.txt  VEP annotated variants classified as Pathogenic in ClinVar on August 08th 2020 in CSV format
VUS_2020.txt  VEP annotated variants classified as VUS in ClinVar on August 08th 2020 in CSV format


