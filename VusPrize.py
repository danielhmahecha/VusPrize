import sys, getopt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
#import matplotlib.pyplot as plt
#import numpy as np
#import math

def main(argv):
    if (argv[0] == '-h'):
        print ('Usage: app.py <inputfile> <outputfile>')
    else:
        
        vepFile = ''
        outFile = ''
        model = load('RF_niu.joblib') 
        vepFile = argv[0]
        outFile = argv[1]
        myvars = pd.read_csv(vepFile, sep='\t')
        ids = myvars.filter(['Location', 'Allele', 'SYMBOL', 'Consequence'])
        myvars_process=processModelVUS(myvars)
        myvars_model=completeColumns(myvars_process)
        result = variantPredictions (myvars_model,ids)
        pd.DataFrame(result).to_csv(outFile, index=False, sep = '\t')



def processModelVUS(df):
    df['codon_degeneracy'] = df['codon_degeneracy'].str.split(',').str[0]
    df['Consequence'] = df['Consequence'].str.split(',').str[0]
    df = df.replace({'codon_degeneracy':'-'},0)
    df=pd.get_dummies(df,columns=['Consequence'])
    df = df.filter(['ada_score','AF','BLOSUM62','CADD_PHRED','codon_degeneracy','Eigen-pred_coding','GERP++_RS', 
              'integrated_fitCons_score','LoFtool','phyloP100way_vertebrate','SIFT', 'Consequence_5_prime_UTR_variant',
              'Consequence_downstream_gene_variant', 'Consequence_frameshift_variant',
              'Consequence_inframe_deletion', 'Consequence_inframe_insertion',
              'Consequence_intron_variant', 'Consequence_missense_variant',
              'Consequence_non_coding_transcript_exon_variant',
              'Consequence_splice_donor_variant', 'Consequence_splice_region_variant',
              'Consequence_start_lost', 'Consequence_stop_gained',
              'Consequence_synonymous_variant', 'Consequence_upstream_gene_variant'])
    df = df.replace({'ada_score': "-", 'AF': "-", 'CADD_PHRED':"-", 'Eigen-pred_coding': '-',
               'integrated_fitCons_score': '-', 'LoFtool': '-', 'phyloP100way_vertebrate':'-',
               'SIFT': '-'}, -1)
    df = df.replace({'BLOSUM62':"-", 'GERP++_RS':'-'}, 0)
    df = df.replace(".",0)   
    df = df.astype(float)
    scaler = MinMaxScaler(feature_range=(0, 1), copy=True)
    scaler.fit (df)
    return df

def completeColumns (df):
    consequences = ['Consequence_3_prime_UTR_variant',
       'Consequence_5_prime_UTR_variant',
       'Consequence_TF_binding_site_variant',
       'Consequence_downstream_gene_variant', 'Consequence_frameshift_variant',
       'Consequence_inframe_deletion', 'Consequence_inframe_insertion',
       'Consequence_intergenic_variant', 'Consequence_intron_variant',
       'Consequence_missense_variant',
       'Consequence_non_coding_transcript_exon_variant',
       'Consequence_protein_altering_variant',
       'Consequence_regulatory_region_variant',
       'Consequence_splice_acceptor_variant',
       'Consequence_splice_donor_variant', 'Consequence_splice_region_variant',
       'Consequence_start_lost', 'Consequence_stop_gained',
       'Consequence_stop_lost', 'Consequence_stop_retained_variant',
       'Consequence_synonymous_variant', 'Consequence_upstream_gene_variant']
    for c in consequences:
        try:
            df[c]
        except:
            df[c] = 0
        
    return df

def variantPredictions(df,ids):
    clf_RF = load('RF_niu.joblib') 
    predicciones = clf_RF.predict(df)
    pd.DataFrame(predicciones).to_csv("predicciones_haplo.csv")
    preds = pd.DataFrame(predicciones, columns=['Prediction'])
    probabilities = clf_RF.predict_proba(df)
    probs = pd.DataFrame(probabilities[:,1], columns = ['Probability'])
    result = pd.concat([ids, preds, probs], axis=1)
    result = result.replace({'Prediction':1}, 'Pathogenic')
    result = result.replace({'Prediction':0}, 'Benign')
    return result

if __name__=="__main__":
    main(sys.argv[1:])
