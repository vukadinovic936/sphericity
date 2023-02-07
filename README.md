# Analyses of cardiac sphericity 
This repository contains the code for analyses performed in [Deep learning enabled analysis of medical images identifies cardiac sphericity as an early marker of cardiomyopathy and related outcomes](TOFILL) by 
Milos Vukadinovic, Alan C. Kwan, Victoria Yuan, Michael Salerno, Daniel C. Lee, Christine M. Albert, Susan Cheng, Debiao Li, David Ouyang*,  Shoa L. Clarke*

## Data
UK Biobank data is availabe upon request at https://www.ukbiobank.ac.uk

## Getting Started

We provide a yaml file to setup a conda environment with all the requirements. 
Run `conda env create -f environment.yml` to get started

ExamplePipeline.ipynb demonstrates all steps necessary to extract sphericity index from long axis cardiac MRI.

After you extract sphericity index for all the subjects in your dataset, you can run downstream statistical analyses: PheWas, Survival Analysis (CoxMethod), GWAS and heritability (LDSC). To learn more about them open the README file in the corresponding folder.

## Inquiries
For inquiries about the repository, please create a GitHub issue or contact milosvuk@ucla.edu. For questions about the manuscript, please reach out to either David Ouyang or Shoa Clarke.

## Citation
If you use this code for your research, please cite our paper.