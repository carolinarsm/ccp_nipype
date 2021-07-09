from nipype.interfaces import afni as afni

refit = afni.Refit()
refit.inputs.in_file   = '/home/brain/nipype/GLM_afni/T1_RPI_crop.nii.gz'
#orient.inputs.args      = ''
refit.inputs.deoblique = True
refit.inputs.xorigin = 'cen'
refit.inputs.yorigin = 'cen'
refit.inputs.zorigin = 'cen'

###
#
#3dDeconvolve -input run001_coreg_aligned2epi.nii.gz run002_coreg_aligned2epi.nii.gz \
#-nfirst 0 \
#-num_stimts 2 \
#-basis_normall 1 \
#-stim_times 1 cond001_onset.1D 'GAM' \
#-stim_label 1 cond1 \
#-stim_times 2 cond003_onset.1D 'GAM' \
#-stim_label 2 cond3 \
#-num_glt 2 \
#-glt_label 1 cond3_cond1_diff \
#-gltsym 'SYM: +cond3 -cond1' \
#-glt_label 2 average \
#-gltsym 'SYM: +0.5*cond1 +0.5*cond3' \
#-fitts fit_ts -errts error_ts \
#-xjpeg glm_matrix.jpg -tout -fout -bucket glm_out