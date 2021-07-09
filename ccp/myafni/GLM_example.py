
import warnings
import os
import re
import sys
from nipype.interfaces.afni.base import AFNICommand, AFNICommandInputSpec
from nipype.interfaces.base import CommandLineInputSpec, CommandLine, TraitedSpec, traits, File, InputMultiPath,     isdefined
os.getcwd()


wd = os.getcwd()
from interfaces import CCPDeconvolve, OneDTool, NiiInfo
os.chdir('../DATA/sub001/')

glm = CCPDeconvolve()

glm.inputs.in_file = [ 'run001_afni+orig.HEAD' , 'run002_afni+orig.HEAD']
glm.inputs.polort = 5
glm.inputs.num_stimts = 2
glm.inputs.out_file = 'X'
glm.inputs.xmat_only = True
glm.inputs.args = '-GOFORIT 10'
glm.inputs.prefix = 'stats'
glm.inputs.stimulus = True
glm.inputs.stim_times=['onsets_COND001_ALL.txt', 'onsets_COND003_ALL.txt']
glm.inputs.stim_labels=['C1', 'C3']

glm.inputs.glm_contrasts = ['C1 -C3', 'C3 -C1', '0.5*C1 +0.5*C3']
glm.inputs.glm_labels = ['diff_pos', 'diff_neg', 'mean']
glm.inputs.glms = True

glm.inputs.model = 'BLOCK(1,1)'
glm.cmdline


glm.run()

os.chdir(wd)
wd





