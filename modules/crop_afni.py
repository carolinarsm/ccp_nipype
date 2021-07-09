# Step 6: REMOVE NECK of anatomicals (match to EPI)
# 3dZcutup -keep 65 190 -prefix T1_crop.nii.gz T1_resampled.nii.gz
# (3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen T1_001_crop.nii.gz)
# (3dresample -orient RPI -prefix T1_RPI_crop.nii.gz -inset T1_001_crop.nii.gz)


from nipype.interfaces import afni as afni

crop = afni.ZCutUp()
crop.inputs.in_file = '/home/brain/nipype/GLM_afni/T1_RPI.nii.gz'
#orient.inputs.args = ''
crop.inputs.keep = '65 190'
crop.inputs.out_file = '/home/brain/nipype/GLM_afni/T1_RPI_crop.nii.gz'
crop.inputs.outputtype = 'NIFTI_GZ'

res = crop.run()