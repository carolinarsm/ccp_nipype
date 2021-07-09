# Step 4: functionals MEAN IMAGE
# 3dTstat -prefix run001_mean.nii.gz run001.nii.gz
# 3dTstat -prefix run002_mean.nii.gz run002.nii.gz


from nipype.interfaces import afni as afni

mean = afni.TStat()
mean.inputs.in_file = '/home/brain/nipype/GLM_afni/run002.nii.gz'
#orient.inputs.args = ''
mean.inputs.out_file = '/home/brain/nipype/GLM_afni/run002_mean.nii.gz'

res = mean.run()