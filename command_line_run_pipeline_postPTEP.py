#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for calling run0_simulations.detect_sources from command line

   Usage: run_IFCAPOL_on_postPTEP <chan_number> <sim_number>

   Both chan_number and sim_number are integers
   chan_number runs between 0 and the maximum number of channels in
   LiteBIRD (currently 22) minus one.
   sim_number runs between 0 and the maximum number of simulations
   (currently 200) minus one.

   Args:
       chan_number (int): The channel number to run the simulation on.
       sim_number (int): The simulation number to run the detection on.

   Returns:
       None

   Raises:
       ValueError: If the channel number or simulation number is out of range.

   Author: herranz
"""

import os
import sys
import run_pipeline_postPTEP as postPTEP

from time import time

args = sys.argv
L = len(args)
p1 = L-2
p2 = L-1

t0 = time()

chan_number = int(sys.argv[p1])
sim_number = int(sys.argv[p2])

nmax    = len(postPTEP.survey.LB_channels)

snr_cut = 3.5

if chan_number < nmax:

    chan_name = postPTEP.survey.LB_channels[chan_number]

    if sim_number < 100:

        fname = postPTEP.cleaned_catalogue_name(sim_number,
                                       chan_name,
                                       snrcut=snr_cut)
        if os.path.isfile(fname):

            print(' Output catalogue already exists for sim {0} in {1}'.format(
                sim_number,chan_name))
        else:

            print(' IFCAPOL detecting in sim {0} in {1}'.format(sim_number,
                                                                chan_name))

            try:
                dicia = postPTEP.detect_source_pipeline(sim_number,
                                                        chan_name,
                                                        count_time=True)

                print('IFCAPOL detection successful for sim {0} in {1}'.format(
                    sim_number, chan_name))

            except Exception as e:

                print('IFCAPOL detection failed for sim {0} in {1}: {2}'.format(
                    sim_number, chan_name, e))
    else:
        raise ValueError('Wrong simulation number')
else:
    raise ValueError('Wrong channel number')

t1 = time()

print(' ')
print(' Execution time: ',t1-t0)


