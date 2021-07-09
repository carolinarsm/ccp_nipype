# REFIT anatomical
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen sub001/struct.nii.gz

# RESAMPLE anatomical (reorient) LPI: neurological view
# 3dresample -orient LPI -prefix T1_reoriented.nii.gz -inset T1_resampled.nii.gz

# REFIT functionals
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen run001.nii.gz
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen run002.nii.gz

# DO NOT RESAMPLE functioanls now
# NOTE: If you would like to do slice-time correction, applying the 3dresample command as
# described above will ERASE some of the slice time information in your file header that
# you provided through to3d. This will cause AFNI to think the file has already been slice-time corrected.
# Thus, if you ask it to slice-time correct a file after applying 3dresample
# (e.g., through afni_proc, 3dTshift or as part of 3dvolreg), it will simply make a file labeled as
# "slice-time corrected" that is in actual fact a

# [Ideal] Do not use the 3dresample command until after slice-time correcting in your processing stream.
# First off, you may not need this command if you are not using coordinates from an atlas/interacting with another imaging program.
# Even if you are, many processing streams will not require that you use a 3dresample command at all,
# especially if you have already changed your anatomical to RPI convention: if you align your EPI to your anatomical,
# AFNI will modify the EPI to match the handedness information in the anatomical.

# MEAN IMAGE
# 3dTstat -prefix run001_mean.nii.gz run001.nii.gz
# 3dTstat -prefix run002_mean.nii.gz run002.nii.gz

# MASK IMAGE
# 3dAutomask -prefix run001_mask.nii.gz run001_mean.nii.gz
# 3dAutomask -prefix run002_mask.nii.gz run002_mean.nii.gz

# REMOVE NECK of anatomicals
# 3dZcutup -keep 80 240 -prefix T1_crop.nii.gz T1_resampled.nii.gz
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen T1_001_crop.nii.gz
# 3dresample -orient RPI -prefix T1_LPI_crop.nii.gz -inset T1_001_crop.nii.gz

# SLICE TIME CORRECTION/ VOLUME REGISTRATION
# 3dvolreg -twodup -verbose -tshift 0 -base run001_mean.nii.gz -maxdisp1D run001_md.txt -1Dfile run001_motion.txt -prefix run001_coreg.nii.gz run001.nii.gz
# 3dvolreg -twodup -verbose -tshift 0 -base run002_mean.nii.gz -maxdisp1D run002_md.txt -1Dfile run002_motion.txt -prefix run002_coreg.nii.gz run002.nii.gz

# plot motion
# 1dplot -volreg -png run001_motion run001_motion.txt
# 1dplot -volreg -png run002_motion run002_motion.txt


# ======================================================================================================
# ======================================================================================================
# ANATOMICAL ALIGNMENT TO EPI
# align_epi_anat.py -anat anat+orig -epi epi+orig -epi_base 5
# lpc_align.py -epi run001_mean.nii.gz -anat T1_LPI_crop.nii.gz -strip_anat_skull no -suffix -coreg

# ===========================================================================
#    This script is superceded by align_epi_anat.py.
#    Please use that program instead.
#    ===========================================================================

# align_api_anat.py -epi run001_mean.nii.gz -anat T1_LPI_crop.nii.gz -anat_has_skull yes
# align_epi_anat.py -anat T1_LPI_crop.nii.gz -epi run001.nii.gz -epi_base mean -epi2anat -anat_has_skull yes -suffix epi2anat.nii.gz
# ======================================================================================================
# ======================================================================================================


#### GLM
# shell command for now
3dDeconvolve -input run001_coreg_aligned2epi.nii.gz run002_coreg_aligned2epi.nii.gz \
-nfirst 0 \
-num_stimts 2 \
-basis_normall 1 \
-stim_times 1 cond001_onset.1D 'GAM' \
-stim_label 1 cond1 \
-stim_times 2 cond003_onset.1D 'GAM' \
-stim_label 2 cond3 \
-num_glt 2 \
-glt_label 1 cond3_cond1_diff \
-gltsym 'SYM: +cond3 -cond1' \
-glt_label 2 average \
-gltsym 'SYM: +0.5*cond1 +0.5*cond3' \
-fitts fit_ts -errts error_ts \
-xjpeg glm_matrix.jpg -tout -fout -bucket glm_out