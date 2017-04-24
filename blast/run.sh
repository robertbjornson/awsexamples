#!/bin/sh

cd /tmp
# this is where blast was installed
export PATH=$PATH:/tmp/miniconda3/bin

echo "Trying to get files"
aws s3 cp s3://myblast/P04156.fasta .
aws s3 cp s3://myblast/zebrafish.1.protein.faa .

ls -l 

echo "running makeblastdb"
makeblastdb -in zebrafish.1.protein.faa -dbtype prot
echo "running blastp"
blastp -query P04156.fasta -db zebrafish.1.protein.faa -out results.txt

cat results.txt

ls -l 
aws s3 cp results.txt s3://myblast/results.txt

