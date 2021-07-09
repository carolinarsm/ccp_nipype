# Step 9: functional slice time correction, volume registration to mean
# Example:
# 3dvolreg -twodup -verbose -tshift 0 -base run001_mean.nii.gz -maxdisp1D run001_md.txt -1Dfile run001_motion.txt -prefix run001_coreg.nii.gz run001.nii.gz
# 3dvolreg -twodup -verbose -tshift 0 -base run002_mean.nii.gz -maxdisp1D run002_md.txt -1Dfile run002_motion.txt -prefix run002_coreg.nii.gz run002.nii.gz

from nipype.interfaces import afni as afni

volreg = afni.Volreg()
volreg.inputs.in_file = '/home/brain/nipype/GLM_afni/sub001/run002.nii.gz' # shpuld use run###_brain.nii.gz?
volreg.inputs.args = '-twodup'
volreg.inputs.timeshift = False
volreg.inputs.basefile = '/home/brain/nipype/GLM_afni/run002_mean.nii.gz'
volreg.inputs.md1d_file = '/home/brain/nipype/GLM_afni/run002_md.txt'
volreg.inputs.oned_file = '/home/brain/nipype/GLM_afni/run002_motion.txt'
volreg.inputs.zpad = 4
volreg.inputs.outputtype = "NIFTI_GZ"
volreg.inputs.out_file = "/home/brain/nipype/GLM_afni/run002_coreg.nii.gz"
volreg.inputs.verbose = True

#1dplot -volreg -png run001_motion run001_motion.txt

res = volreg.run()

# 3dvolreg can handle small motions fairly well, but larger motion (> 1mm) might not be properly corrected.