# For STROOP experiments
3dDeconvolve
-input pb01.ST015.r01.scale+tlrc.HEAD pb01.ST015.r02.scale+tlrc.HEAD pb01.ST015.r03.scale+tlrc.HEAD pb01.ST015.r04.scale+tlrc.HEAD
-polort 5
-float
-num_stimts 8
-stim_times 1 stimuli/LWMC_CONGRUENT.txt 'BLOCK(0.72,1)'
-stim_label 1 lwmc_c
-stim_times 2 stimuli/LWMC_INCONGRUENT.txt 'BLOCK(0.72,1)'
-stim_label 2 lwmc_i
-stim_times 3 stimuli/LWMC_PC50_C.txt 'BLOCK(0.72,1)'
-stim_label 3 lwmc_pc50c
-stim_times 4 stimuli/LWMC_PC50_I.txt 'BLOCK(0.72,1)'
-stim_label 4 lwmc_pc50i
-stim_times 5 stimuli/LWMI_CONGRUENT.txt 'BLOCK(0.72,1)'
-stim_label 5 lwmi_c
-stim_times 6 stimuli/LWMI_INCONGRUENT.txt 'BLOCK(0.72,1)'
-stim_label 6 lwmi_i
-stim_times 7 stimuli/LWMI_PC50_C.txt 'BLOCK(0.72,1)'
-stim_label 7 lwmi_pc50c
-stim_times 8 stimuli/LWMI_PC50_I.txt 'BLOCK(0.72,1)'
-stim_label 8 lwmi_pc50i
-ortvec motion_demean.1D mov_reg
-gltsym 'SYM: +lwmc_i -lwmc_c'
-glt_label 1 LWMC_I-C
-gltsym 'SYM: +lwmi_i -lwmi_c'
-glt_label 2 LWMI_I-C
-gltsym 'SYM: +lwmc_pc50i -lwmc_pc50c'
-glt_label 3 LWMC_PC50_I-C
-gltsym 'SYM: +lwmi_pc50i -lwmi_pc50c'
-glt_label 4 LWMI_PC50_I-C
-fout
-tout
-x1D X.xmat.1D
-xjpeg X.jpg
-errts errts.ST015
-bucket stats.ST015


# OR
3dREMLfit
-matrix X.xmat.1D
-input "pb01.ST015.r01.scale+tlrc.HEAD pb01.ST015.r02.scale+tlrc.HEAD pb01.ST015.r03.scale+tlrc.HEAD pb01.ST015.r04.scale+tlrc.HEAD"
-fout
-tout
-Rbuck stats.ST015_REML
-Rvar stats.ST015_REMLvar
-Rerrts errts.ST015_REML -verb $*

_____
### 3dDeconvolve input specs (command line arguments)

in_file         --> '-input'        string/list
mask            --> '-mask'         string
censor_list     --> '-censor'       string
polort          --> '-porlot'       int
num_stimts      --> '-num_stimts'    int
stim_file       --> '-stim_files'   int string (lists? dict?)   # for motion parameters
stim_label      --> '-stim_labels'  string (list?)
stim_times      --> '-stim_times'   int string string
options
    no_data     --> '-nodata'
    global_time
    local_time


Special (examples)
[-stim_times_FSL k tname Rmodel]
[-stim_times_FSL k tname Rmodel]
[-stim_times_FSL k tname Rmodel]


GLT
num_glt
glt_label
gltsym




### 3dttest++ input specs

_______

Check

subject level: 3dDeconvolve
group level: 3dttest++

