#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 20:23:55 2022

@author: herranz
"""

import PTEP_simulations as simuls
import sys

chan_name    = 'LB_LFT_40'
print('Argument List:', str(sys.argv))


# simnum = 10
# diccio = simuls.PTEP_simulated_maps(simnum,chan_name)

# simstr = '{0:04d}'.format(simnum)

# outdir = survey.map_dir+simstr+'/'
# if not os.path.isdir(outdir):
#     os.mkdir(outdir)

# diccio['TOTAL'].write(outdir+'total_'+chan_name+'_'+simstr+'.fits')

# simuls.detect_sources(10,chan_name)