## Setting up Hail from source
I found that the easiest way to allow hail to use more memory is to build it from the source. I'll describe the process, but you can also take a look at the docs here : https://hail.is/docs/0.2/getting_started_developing.html.  To install hail you will need the following:N

* Unix based system
* Java 8 JDK 
* Python > 3.6
* Scala 2.12
* Spark 3.1.1
* A recent C and a C++ compiler, GCC 5.0, LLVM 3.4, or later versions of either suffice.
* BLAS and LAPACK.
* The LZ4 library

Note: The instructions were tested on Ubuntu 20.04 and WSL for Windows running Ubuntu 20.04.

To install all the previously mentioned dependencies:

	apt-get update
	apt-get install \
	scala \
    openjdk-8-jdk-headless \
    g++ \
    python3 python3-pip \
    libopenblas-dev liblapack-dev \
    liblz4-dev

Set JAVA_HOME:

	export JAVA_HOME=/usr/java/<your version>

Mine was 
	export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/
 
Next clone the hail official repo:

	git clone https://github.com/hail-is/hail

If maintainers changed things, and syntax is different, for this repo to work clone the commit: #11043 

Then:

	cd hail/hail
	make install-on-cluster HAIL_COMPILE_NATIVES=1

You should be ready to go with the code, for any additional errors, consult the documentation or raise the issue here.

Now you want to spark-submit your hail code with more memory.
Go to the file gwas.rc and set HAIL_HOME the path to your build/libs folder (the one from cloned repo)
For example mine is:

	HAIL_HOME="/mnt/d/hail/hail/build/libs"

## Run GWAS
Follow the steps 1-8
1_merge_mfi.sh - Merges mfi files accross chromosomes that contain Imputation MAF+info. 
2_fam_sqc_merge.R - merges quality check files
3_make_sample_qc_table.py - make a hail table pull important columns
4_build_pipelines.py - build a pipeline from phenotype data
5_make_variant_annotation_vds.py - filter snps
7_run_linreg3.py - run gwas, generate manhattan and qqplot, and save results
8_export_results.py - export results to tsv file with the following columns:
locus,alleles_n, sum_x, y_transpose_x, beta, standard_error, t_stat, p_value, v, chr, rsid, pos, ref, alt, maf, info
