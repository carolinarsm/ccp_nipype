# 3dmerge -1blur_fwhm 5 -doall -session . -prefix run_1_vr_lp_5mm run_1_vr_lp+orig
# See coments about spatial filtering here: http://brainimaging.waisman.wisc.edu/~tjohnstone/AFNI_I.html#_3._Slice_timing

from nipype.interfaces import afni as afni
blur = afni.Merge()
blur.inputs.in_files = ['functional.nii', 'functional2.nii']
blur.inputs.blurfwhm = 4
blur.inputs.doall = True
blur.inputs.out_file = 'e7.nii.gz'


res = blur.run()