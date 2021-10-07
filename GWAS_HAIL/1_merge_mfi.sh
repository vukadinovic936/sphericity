#!/bin/bash

for i in {1..22}
do
	echo $i
	awk -v chr=$i 'BEGIN {FS="\t"; OFS="\t"} {print chr,$0}' "data/ukb_mfi_chr${i}_v3.txt" >> ukb_mfi_v3.tsv
done
gzip ukb_mfi_v3.tsv

