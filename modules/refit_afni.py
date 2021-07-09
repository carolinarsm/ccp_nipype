# Step 1 : orient Anatomical
# Step 3 : orient functionals
# Example:
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen sub001/struct.nii.gz
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen run001.nii.gz
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen run002.nii.gz
# Step 7: refit cropped structural
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen T1_001_crop.nii.gz


from nipype.interfaces import afni as afni

refit = afni.Refit()
refit.inputs.in_file   = '/home/brain/nipype/GLM_afni/T1_RPI_crop.nii.gz'
#orient.inputs.args      = ''
refit.inputs.deoblique = True
refit.inputs.xorigin = 'cen'
refit.inputs.yorigin = 'cen'
refit.inputs.zorigin = 'cen'

#orient._outputs.out_file = "/home/brain/nipype/GLM_afni/T1_RPI.nii.gz"


res =refit.run()