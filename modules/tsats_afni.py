from nipype.interfaces import afni

tstat = afni.TStat()
tstat.inputs.in_file = '/home/brain/nipype/nipype_tutorial/data/temp_sub001/struct4d.nii'
tstat.inputs.args = '-mean'
tstat.inputs.out_file = "stats"

#tstat.cmdline
#'3dTstat -mean -prefix stats struct4d.nii'
res = tstat.run()