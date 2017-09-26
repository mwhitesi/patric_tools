"""Download PATRIC MIC Values

Functions for obtaining genome sequences and MIC values for a given species
from the PATRIC database

Example:
        $ python mic.py -s species -o 

Todo:
    * 

Previous:

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

import subprocess
import os

from ggplot import *
from tempfile import gettempdir

from .amr import get_latest_metadata


def summarize_species(amr_metadata_file=None):

    if amr_metadata_file is None:
        amr_metadata_file = get_latest_metadata(gettempdir())

    bashCommand = "cut -f2 {} | cut -f1-2 -d' ' | sort | uniq -c | sort -nr".format(os.path.abspath(amr_metadata_file))
  
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    return output.decode("unicode_escape")


def plot_mic_distribution(amrsubset, name):

    amrsubset = amrsubset[['measurement_sign', 'measurement_value', 'resistant_phenotype']]
    amrsubset['measurement_value'] = amrsubset['measurement_value'].astype(float)
    amrsubset = amrsubset.dropna(subset=['measurement_value'])
    p = ggplot(aes(x='measurement_value'), data=amrsubset) + geom_histogram(binwidth=1)
    p.save(name + '.png')


def filter_mics(amr, species=None, drugs=None):

    amr = amr.loc[amr.laboratory_typing_method == "MIC"]

    if species is not None:
        if type(species) == str:
            species = [species]
        species = [s.lower() for s in species]
        amr = amr.loc[[n.lower() in species for n in amr.genome_name]]


    if drugs is not None:
        if type(drugs) == str:
            drugs = [drugs]
        drugs = [s.lower() for s in drugs]
        amr = amr.loc[[n.lower() in drugs for n in amr.antibiotic]]






    return amr
