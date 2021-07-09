# Step 10: align functional to anatomy
# With script: lpc_align.py -epi run001_mean.nii.gz -anat T1_LPI_crop.nii.gz -strip_anat_skull no -suffix -coreg
# WIth 3dAllineate (not sure about this):


from nipype.interfaces import afni as afni

epi2anat = afni.Allineate()
epi2anat.inputs.in_file = '/home/brain/nipype/GLM_afni/run002_coreg.nii.gz'
epi2anat.inputs.reference = '/home/brain/nipype/GLM_afni/anat_RPI_crop.nii.gz'
epi2anat.inputs.args = ''
epi2anat.inputs.epi = True
epi2anat.inputs.outputtype = "NIFTI_GZ"
epi2anat.inputs.out_file = "/home/brain/nipype/GLM_afni/run002_coreg_aligned2epi.nii.gz"


res = epi2anat.run()

