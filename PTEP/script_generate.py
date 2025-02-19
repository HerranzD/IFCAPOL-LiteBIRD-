#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 16:20:39 2022

@author: herranz
"""

from myutils import save_ascii_list
import PTEP_simulations as PTEP
import sys
import os

nchans = len(PTEP.LB_channels)
nsims  = 100
Njobs  = nsims

args   = sys.argv
print(args)

def make_job_arrays():
    """
    This routine automatically generates the scripts to run, as a set job arrays
    with 100 elements each (one job per PTEP simulation), the IFCAPOL source
    detection algorithm for all the LiteBIRD channels. A single slurm script
    is generated for each LiteBIRD channel.

    Returns
    -------
    None.

    """

    lsubmits = []

    for ichan in range(nchans):

        job_init = 100
        job_end  = 99

        for isim in range(100):
            chan_name = PTEP.LB_channels[ichan]
            fname     = PTEP.cleaned_catalogue_name(isim,chan_name)
            if not os.path.isfile(fname):
                job_init = isim
                break

        lsta = []

        if job_init <= job_end:

            lsta.append('#!/bin/bash')
            lsta.append('#SBATCH -N 1')
            lsta.append('#SBATCH -C haswell')
            lsta.append('#SBATCH -q regular')
            lsta.append('#SBATCH -J IFCAPOL_array_job_{0}'.format(ichan))
            lsta.append('#SBATCH --mail-user=herranz@ifca.unican.es')
            lsta.append('#SBATCH --mail-type=ALL')
            lsta.append('#SBATCH --account=mp107')
            lsta.append('#SBATCH -t 02:30:00')
            lsta.append('#SBATCH --output={0}Output_Logs/IFCAPOL_nchan{1}_%A.%a.out'.format(PTEP.survey.scriptd,ichan))
            lsta.append('#SBATCH --error={0}Output_Logs/IFCAPOL_nchan{1}_%A.%a.err'.format(PTEP.survey.scriptd,ichan))
            lsta.append('#SBATCH --array={0}-{1}             # job array with index values {2}, ... {3}'.format(job_init,
                                                                                                                job_end,
                                                                                                                job_init,
                                                                                                                job_end))
            lsta.append('#SBATCH --chdir={0}'.format(PTEP.survey.scriptd))
            lsta.append(' ')
            lsta.append('#run the application:')
            lsta.append('module load python')
            lsta.append('source activate pycmb')
            lsta.append('srun python3 $HOME/LiteBIRD/src/run_IFCAPOL.py {0} $SLURM_ARRAY_TASK_ID'.format(ichan))
            lsta.append('conda deactivate')

        macro_name = PTEP.survey.scriptd+'submit_nchan{0}.slurm'.format(ichan)
        save_ascii_list(lsta,macro_name)

        lsubmits.append('sbatch submit_nchan{0}.slurm'.format(ichan))

    save_ascii_list(lsubmits, PTEP.survey.scriptd+'submit_arrays.sh')

def make_scripts():
    """

    (DEPRECATED)

    This routine generates automatically the set of Slurm scritps needed to run
    the IFCAPOL source extraction over all the LiteBIRD PTEP simulations on Cori
    at NERSC. A separated script is generated for any single simulation, which
    results in a huge number of scripts and jobs to queue. A better implementation
    will be attempted in the future.

    Returns
    -------
    None.

    """

    command_list = []

    for ichan in range(nchans):
        for isim in range(nsims):

            lsta = []
            lsta.append('#!/bin/bash')
            lsta.append('#SBATCH -N 1')
            lsta.append('#SBATCH -C haswell')
            lsta.append('#SBATCH -q regular')
            lsta.append('#SBATCH -J IFCAPOL_{0}_{1}'.format(ichan,isim))
            lsta.append('#SBATCH --mail-user=herranz@ifca.unican.es')
            lsta.append('#SBATCH --mail-type=ALL')
            lsta.append('#SBATCH --account=mp107')
            lsta.append('#SBATCH -t 04:30:00')
            lsta.append('#SBATCH --output={0}Output_Logs/IFCAPOL_nchan{1}_nsim{2}.out'.format(PTEP.survey.scriptd,ichan,isim))
            lsta.append('#SBATCH --chdir={0}'.format(PTEP.survey.scriptd))
            lsta.append(' ')
            lsta.append('#run the application:')
            lsta.append('module load python')
            lsta.append('source activate pycmb')
            lsta.append('srun -n 1 -c 1 -t 04:30:00 python3 $HOME/LiteBIRD/src/run_IFCAPOL.py {0} {1}'.format(ichan,isim))
            lsta.append('conda deactivate')

            macro_name = PTEP.survey.scriptd+'submit_nchan{0}_nsim{1}.sh'.format(ichan,isim)
            save_ascii_list(lsta,macro_name)
            command_list.append('sbatch {0}'.format(macro_name))

    for subj in range(nchans*nsims//Njobs):
        fname = PTEP.survey.scriptd+'send_{0}.sh'.format(subj)
        imin = subj*Njobs
        imax = (subj+1)*Njobs
        save_ascii_list(command_list[imin:imax],fname)


def check_outputs():
    """
    This routine checks which Slurm jobs generated by `make_scripts` have failed
    to produce an output. For every failed job a new sbatch command is added
    to a *repesca.sh* script.

    Returns
    -------
    None.

    """

    clean_mode = 'after'

    command_list = []

    for ichan in range(nchans):

        chan_name = PTEP.LB_channels[ichan]

        for sim_number in range(nsims):

            catal_fname = PTEP.detected_catalogue_name(sim_number,chan_name)
            fname    = catal_fname.replace('.fits','_{0}_cleaned.fits'.format(clean_mode))
            if not os.path.isfile(fname):
                macro_name = PTEP.survey.scriptd+'submit_nchan{0}_nsim{1}.sh'.format(ichan,sim_number)
                command_list.append('sbatch {0}'.format(macro_name))

    fname = PTEP.survey.scriptd+'repesca.sh'
    save_ascii_list(command_list,fname)


if 'generate' in args[-1:]:
    print(' Generating the scripts')
    make_job_arrays()
else:
    print('Checking for failed jobs')
    check_outputs()



