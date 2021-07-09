# Step 2 : orient Anatomical
# Example: 3dresample -orient RPI -prefix T1_RPI.nii.gz -inset struct.nii.gz
# Step 8: orient cropped structural
# 3dresample -orient RPI -prefix anat_RPI_crop.nii.gz -inset T1_001_crop.nii.gz)
from nipype.interfaces import afni as afni

orient = afni.Resample()
orient.inputs.in_file = '/home/brain/nipype/GLM_afni/T1_RPI_crop.nii.gz'
#orient.inputs.args = ''
orient.inputs.orientation = 'RPI'
orient.inputs.out_file = '/home/brain/nipype/GLM_afni/anat_RPI_crop.nii.gz'
orient.inputs.outputtype = 'NIFTI_GZ'

res = orient.run()
