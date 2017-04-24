# Base Image
FROM amazonlinux:latest

# Metadata
LABEL version="1"
LABEL software="NCBI BLAST+"
LABEL software.version="2.2.31"
LABEL description="basic local alignment search tool"
LABEL website="http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastHome"
LABEL documentation="http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastHome"
LABEL license="http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastHome"
LABEL tags="Genomics"

# Maintainer
MAINTAINER Saulo Alves Aflitos <sauloal@gmail.com>

RUN yum -y install which unzip aws-cli wget bzip2 libgomp

RUN wget http://repo.continuum.io/miniconda/Miniconda3-3.7.0-Linux-x86_64.sh -O miniconda.sh

RUN bash miniconda.sh -b -p /tmp/miniconda3

RUN /tmp/miniconda3/bin/conda install --yes -c bioconda blast=2.2.31

ADD run.sh /data/run.sh

USER nobody

ENTRYPOINT ["/data/run.sh"]
