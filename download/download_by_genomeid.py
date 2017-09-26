"""Download PATRIC genome files to directory

Example:
	$ python download/download_by_genomeid.py file directory/


patric_tools: A Python package to download data from the PATRIC database
Copyright (C) 2017 Alexandre Drouin
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""

import os
import sys
sys.path.insert(0, os.getcwd())

import argparse
from joblib import Parallel, delayed
from patric_tools.genomes import download_genome_contigs
import pandas as pd


def download_genome(g_id, output_directory):
    print("...... Isolate: {0!s} -> {1!s}/{0!s}.fna".format(g_id, output_directory))
    download_genome_contigs(g_id, output_directory)
    

def download_genomes(genome_file, output_directory):
	"""Download PATRIC genome ids in file


	"""

	# Load genome id file
	genome_ids = pd.read_table(genome_file,header=None,names=['id'],converters={'id': str})

	print("... Genomes: {}".format(len(genome_ids)))

	print("... Fetching genome sequences:")
	
	# Download 4 genomes in parallel
	Parallel(n_jobs=4)(delayed(download_genome)(g_id, output_directory) for g_id in genome_ids['id'])
	print("Done.")


def main():
   
    parser = argparse.ArgumentParser()
    parser.add_argument("genome_file")
    parser.add_argument("output_directory")
    args = parser.parse_args()

    download_genomes(args.genome_file, args.output_directory)


if __name__ == "__main__":
    main()
    