from nipype.interfaces import afni as afni

to_afni = afni.Copy()
to_afni.inputs.in_file = '/home/brain/nipype/GLM_afni/sub001/struct_bet.nii.gz'
to_afni.inputs.out_file = "/home/brain/nipype/GLM_afni/struct_brain"
# to_afni.inputs.args = '-Fourier -twopass'
to_afni.inputs.outputtype = "AFNI"


to_afni.run()