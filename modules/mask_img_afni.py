# Step 5: functional MASK IMAGE
# 3dAutomask -prefix run001_mask.nii.gz run001_mean.nii.gz -apply_prefix run001_brain.nii.gz
# 3dAutomask -prefix run002_mask.nii.gz run002_mean.nii.gz -apply_prefix run002_brain.nii.gz

from nipype.interfaces import afni as afni

mask = afni.Automask()
mask.inputs.in_file = '/home/brain/nipype/GLM_afni/run002_mean.nii.gz'
#orient.inputs.args = ''
mask.inputs.out_file = '/home/brain/nipype/GLM_afni/run002_mask.nii.gz'
mask.inputs.outputtype = 'NIFTI_GZ'
mask.inputs.brain_file = '/home/brain/nipype/GLM_afni/run002_brain.nii.gz'
res = mask.run()