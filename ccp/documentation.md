AFNI analysis (WORKFLOW)

SUBJECT LEVEL



### PREPARE DATA ###

INPUTS
    - subj          : subject ID            (ex: ST015 )
    - runs          : runs ID               (ex: (01 02 03 04) )
    - stimfiles     : list of stim files    (ex: (ts_CONGRUENT.txt ts_INCONGRUENT.txt ts_PC50_C.txt ts_PC50_I.txt) )
    - anatfile      : anatomical image      (ex: anat+tlrc )
    - tr_counts     : TRs per run           (ex: (952 932 932 945 ) )
    - moveregfile   : motion regressors     (ex: Movement_Regressors_ALL.txt)


OUTPUTS:
    - output_dir    : ./subj.results        (ex: ST015.results)         --> created in working directory
    - stimuli       : ./subj.results/stimuli(ex: ST015.results/stimuli) --> created
    - copied stimuli, mov regressors and anatomical files into above directories


FUNCTIONS/SCRIPTS
    - 3dcopy        (in nipype.interfaces.afni.preprocess as Copy)
    - 3dTcat        (in nipype.interfaces.afni.preprocess as TCat)
    - 1dtool.py     TO DO wrap -> as a literal command only?
    - 3dAutomask    (in nipype.interfaces.afni.preprocess as Automask)
    - 3dmask_tool   TO DO wrap -> as a literal command only?
    - 3dTstat       (in nipype.interfaces.afni.preprocess as TStat)
    - 3dcalc        (in nipype.interfaces.afni.preprocess as Calc)



### RUN GLM ###

INPUTS
    -


OUTPUTS
    -


FUNCTION/SCRIPTS
    - 3dDeconvolve
    - 3dREMLfit


#############################

 01_prepare_data.script
#!/bin/tcsh -xef

set subj = ST015
set runs = (01 02 03 04)
set stimfiles = (ts_CONGRUENT.txt ts_INCONGRUENT.txt ts_PC50_C.txt ts_PC50_I.txt)
set anatfile = anat+tlrc
set tr_counts = ( 952 932 932 945 )
set movregfile = Movement_Regressors_ALL.txt
# ============================ output directory ============================

# assign output directory name
set output_dir = $subj.results

# verify that the results directory does not yet exist
if ( -d $output_dir ) then
    echo output dir "$subj.results" already exists
    exit
endif

mkdir $output_dir
mkdir $output_dir/stimuli



# copy stim files into stimulus directory
#cp LWMC.txt LWMI.txt $output_dir/stimuli
cp $stimfiles $output_dir/stimuli

# copy anatomy to results dir
# 3dcopy anat+tlrc $output_dir/anat
3dcopy $anatfile $output_dir/anat

# Movement Regressors
# cp Movement_Regressors_ALL.txt $output_dir
cp $movregfile $output_dir



# ============================ auto block: tcat ============================
# apply 3dTcat to copy input dsets to results dir, while
# removing the first 0 TRs
3dTcat -prefix $output_dir/pb00.$subj.r01.tcat run001+tlrc'[0..$]'
3dTcat -prefix $output_dir/pb00.$subj.r02.tcat run002+tlrc'[0..$]'
3dTcat -prefix $output_dir/pb00.$subj.r03.tcat run003+tlrc'[0..$]'
3dTcat -prefix $output_dir/pb00.$subj.r04.tcat run004+tlrc'[0..$]'


# ============================ move to resutls directory ============================
# ============================ move to resutls directory ============================

cd $output_dir

# compute motion magnitude time series: the Euclidean norm
# (sqrt(sum squares)) of the motion parameter derivatives
1d_tool.py -infile $movregfile         	                         \
           -set_run_lengths $tr_counts	                         \
           -derivative  -collapse_cols euclidean_norm            \
           -write motion_${subj}_enorm.1D


# create an anat_final dataset, aligned with stats
3dcopy $anatfile anat_final.$subj


# ================================== mask ==================================
# create 'full_mask' dataset (union mask)
foreach run ( $runs )
    3dAutomask -dilate 1 -prefix rm.mask_r$run pb00.$subj.r$run.tcat+tlrc
end


# create union of inputs, output type is byte
3dmask_tool -inputs rm.mask_r*+tlrc.HEAD -union -prefix full_mask.$subj


# ================================= scale ==================================
# scale each voxel time series to have a mean of 100
# (be sure no negatives creep in)
# (subject to a range of [0,200])
foreach run ( $runs )
    3dTstat -prefix rm.mean_r$run pb00.$subj.r$run.tcat+tlrc
    3dcalc -a pb00.$subj.r$run.tcat+tlrc -b rm.mean_r$run+tlrc \
           -expr 'min(200, a/b*100)*step(a)*step(b)'           \
           -prefix pb01.$subj.r$run.scale
end

# ================================ regress =================================

# compute de-meaned motion parameters (for use in regression)
1d_tool.py -infile $movregfile -set_run_lengths $tr_counts        \
           -demean -write motion_demean.1D

# compute motion parameter derivatives (just to have)
1d_tool.py -infile $movregfile -set_run_lengths $tr_counts        \
           -derivative -demean -write motion_deriv.1D





foreach run ( $runs )

    echo "3dTstat -prefix rm.mean_r$run pb00.$subj.r$run.tcat+tlrc" >> $batchjob
    echo "3dcalc -a pb00.$subj.r$run.tcat+tlrc -b rm.mean_r$run+tlrc \\
           -expr 'min(200, a/b*100)*step(a)*step(b)'           \\
           -prefix pb01.$subj.r$run.scale" >> $batchjob
end



echo "Preparing data ended."



02_run_glm_8reg.script
#!/bin/tcsh -xef

set subj = ST015
set runs = ( 01 02 03 04 )
set stimfiles = ( LWMC_CONGRUENT.txt LWMC_INCONGRUENT.txt LWMC_PC50_C.txt LWMC_PC50_I.txt LWMI_CONGRUENT.txt LWMI_INCONGRUENT.txt LWMI_PC50_C.txt LWMI_PC50_I.txt)
set anatfile = anat+tlrc
set tr_counts = ( 952 932 932 945 )
set movregfile = Movement_Regressors_ALL.txt
# ============================ output directory ============================

# assign output directory name
set output_dir = $subj.results

# ============================ move to resutls directory ============================

cd $output_dir

# ------------------------------
# run the regression analysis

3dDeconvolve -input pb01.$subj.r*.scale+tlrc.HEAD                       \
    -polort 5 -float                                                    \
    -num_stimts 8                                                       \
    -stim_times 1 stimuli/LWMC_CONGRUENT.txt 'BLOCK(0.72,1)'       	\
    -stim_label 1 lwmc_c                                             	\
    -stim_times 2 stimuli/LWMC_INCONGRUENT.txt 'BLOCK(0.72,1)'          \
    -stim_label 2 lwmc_i                                             	\
    -stim_times 3 stimuli/LWMC_PC50_C.txt 'BLOCK(0.72,1)'               \
    -stim_label 3 lwmc_pc50c                                            \
    -stim_times 4 stimuli/LWMC_PC50_I.txt 'BLOCK(0.72,1)'               \
    -stim_label 4 lwmc_pc50i                                            \
    -stim_times 5 stimuli/LWMI_CONGRUENT.txt 'BLOCK(0.72,1)'            \
    -stim_label 5 lwmi_c                                             	\
    -stim_times 6 stimuli/LWMI_INCONGRUENT.txt 'BLOCK(0.72,1)'          \
    -stim_label 6 lwmi_i                                             	\
    -stim_times 7 stimuli/LWMI_PC50_C.txt 'BLOCK(0.72,1)'               \
    -stim_label 7 lwmi_pc50c                                            \
    -stim_times 8 stimuli/LWMI_PC50_I.txt 'BLOCK(0.72,1)'               \
    -stim_label 8 lwmi_pc50i 	                                        \
    -ortvec motion_demean.1D mov_reg					\
    -gltsym 'SYM: +lwmc_i -lwmc_c' -glt_label 1 LWMC_I-C		\
    -gltsym 'SYM: +lwmi_i -lwmi_c' -glt_label 2 LWMI_I-C       		\
    -gltsym 'SYM: +lwmc_pc50i -lwmc_pc50c' -glt_label 3 LWMC_PC50_I-C   \
    -gltsym 'SYM: +lwmi_pc50i -lwmi_pc50c' -glt_label 4 LWMI_PC50_I-C   \
    -fout -tout -x1D X.xmat.1D -xjpeg X.jpg                            	\
    -errts errts.${subj}                                               	\
    -bucket stats.$subj




# if 3dDeconvolve fails, terminate the script
if ( $status != 0 ) then
    echo '---------------------------------------'
    echo '** 3dDeconvolve error, failing...'
    echo '   (consider the file 3dDeconvolve.err)'
    exit
endif


echo 'Finished!'


_________________
GROUP LEVEL

INPUTS:
	- lower level stats
	(check which blocks you want to input to the test)



cmd_001.script
#!/bin/tcsh -xef

# apply any data directories with variables
set data_dir = /scratch/ramirezc/afni_glm_stroop

3dttest++ -prefix LWMC_I-C_group_ttest                                               \
          -setA LWMC_C-I                                                             \
             3                                                                       \
          "$data_dir/ST013/ST013.results/stats.ST013+tlrc.HEAD[LWMC_I-C_GLT#0_Coef]" \
                                                                                     \
             4                                                                       \
          "$data_dir/ST014/ST014.results/stats.ST014+tlrc.HEAD[LWMC_I-C_GLT#0_Coef]" \
                                                                                     \
             5                                                                       \
          "$data_dir/ST015/ST015.results/stats.ST015+tlrc.HEAD[LWMC_I-C_GLT#0_Coef]"








##################
UTILS

3dinfo -nv run001+tlrc

-global_times]
[-local_times]
-num_glt num         num = number of general linear tests (GLTs)
                       (0 <= num)   [default: num = 0]
                  **N.B.: You only need this option if you have
                          more than 10 GLTs specified; the program
                          has built-in space for 10 GLTs, and
                          this option is used to expand that space.
                          If you use this option, you should place
                          it on the command line BEFORE any of the
                          other GLT options.


[-gltsym gltname]    Read the GLT with symbolic names from the file
                       'gltname'; see the document below for details:
  http://afni.nimh.nih.gov/pub/dist/doc/misc/Decon/DeconSummer2004.html


[-sresp k sprefix]   sprefix = prefix of 3D+time output dataset which
                       will contain the standard deviations of the
                       kth impulse response function parameters
[-fitts  fprefix]    fprefix = prefix of 3D+time output dataset which
                       will contain the (full model) time series fit
                       to the input dataJupyter Notebooklist_strings (autosaved)

​

[-errts  eprefix]    eprefix = prefix of 3D+time output dataset which
                       will contain the residual error time series
                       from the full model fit to the input data


[-fout]            Flag to output the F-statistics for each stimulus
                    ** F tests the null hypothesis that each and every
                       beta coefficient in the stimulus set is zero
                    ** If there is only 1 stimulus class, then its
                       '-fout' value is redundant with the Full_Fstat
                       computed for all stimulus coefficients together.
[-rout]            Flag to output the R^2 statistics
[-tout]            Flag to output the t-statistics
                    ** t tests a single beta coefficient against zero
                    ** If a stimulus class has only one regressor, then

                     (AND OTHER OUTPUT OPTIONS!!)

[-xsave]
[-float]            Write output datasets in float format, instead of
                    as scaled shorts [** now the default **]
[-x1D_stop]          Stop running after writing .xmat.1D files.
                     * Useful for testing, or if you are going to
                       run 3dREMLfit instead -- that is, you are just
                       using 3dDeconvolve to set up the matrix file.




####
Useful interfaces

nipype.workflow.misc.uitl --> to get voulme dimensions