# Filter prior to linear model fitting
# Example: 3dFourier -prefix run_1_vr_lp -lowpass 0.05 -retrend run_1_vr+orig
from nipype.interfaces import afni as afni

lpf = afni.Fourier()
lpf.inputs.in_file = '/home/brain/nipype/GLM_afni/reg_run001.nii.gz'
lpf.inputs.args     = '-retrend'
lpf.inputs.lowpass  = 0.0004
lpf.inputs.highpass = 0.00035
lpf.inputs.out_file = "/home/brain/nipype/GLM_afni/lpf_reg_run001.nii.gz"
#volreg.inputs.md1d_file = "/home/brain/nipype/GLM_nifti/run001_maxdisp"

# 1dplot -volreg run001_motion.txt
res = lpf.run()

