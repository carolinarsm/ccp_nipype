from nipype.interfaces import afni as afni

skullstrip = afni.SkullStrip()
skullstrip.inputs.in_file = '/home/brain/nipype/GLM_afni/sub001/struct.nii.gz'
skullstrip.inputs.args = '-push_to_edge'
skullstrip.inputs.out_file = "/home/brain/nipype/GLM_afni/struct_brain.nii.gz"
skullstrip.cmdline
res = skullstrip.run()


# DOESN'T WORK
#skullstrip
# Standard error:
# freeglut (3dSkullStrip): failed to open display ':1'
# Return code: 1
# Interface SkullStrip failed to run

# RuntimeError: Xvfb was not found, X redirection aborted
# Interface SkullStrip failed to run

# Example
# 3dSkullStrip -input /home/brain/nipype/GLM_afni/sub001/struct.nii.gz -push_to_edge -prefix /home/brain/nipype/GLM_afni/struct_brain.nii.gz

#The intensity in the output dataset is a modified version
#of the intensity in the input volume.
#To obtain a masked version of the input with identical values inside
#the brain, you can either use 3dSkullStrip's -orig_vol option
#or run the following command:
#  3dcalc -a /home/brain/nipype/GLM_afni/sub001/struct.nii.gz -b /home/brain/nipype/GLM_afni/struct_brain.nii.gz+orig -expr 'a*step(b)' \
#         -prefix /home/brain/nipype/GLM_afni/struct_brain.nii.gz_orig_vol
#to generate a new masked version of the input.
