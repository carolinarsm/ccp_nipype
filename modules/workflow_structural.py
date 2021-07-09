import os                                    # system functions
from nipype import config
#config.enable_provenance()
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pipeline engine
from nipype.interfaces import afni as afni

## data
data_dir = os.path.abspath('data')
print data_dir

subject_list = ['sub001', 'sub002', 'sub003', 'sub004']
info = dict(struct=[['subject_id', 'struct']])
infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="infosource")
infosource.iterables = ('subject_id', subject_list)

# ===========================================================================================================
# Create an nipype,interface.io.DataSource object
datasource=pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                             outfields=['struct']),
                   name= 'datasource')


datasource.inputs.base_directory = data_dir
datasource.inputs.template = '%s/%s.nii.gz'
datasource.inputs.template_args = info
datasource.inputs.sort_filelist = True


# motion outliers node
#motion_outliers = pe.MapNode(interface=fsl.MotionOutliers(),
#                             iterfield= 'in_file',
#                             name="motion_outliers")
#motion_outliers.inputs.in_file = '/home/brain/nipype/outliers_workflow/data/sub001/run001.nii.gz'
#metric_list = ['fd', 'dvars']
#motion_outliers.iterables = ('metric', metric_list)

# ======= REFIT
# 3drefit -deoblique -xorigin cen -yorigin cen -zorigin cen sub001/struct.nii.gz

refit = pe.MapNode(interface=afni.Refit(),
                   iterfield='in_file',
                   name='refit')
#refit.inputs.in_file   = '/home/brain/nipype/GLM_afni/T1_RPI_crop.nii.gz'
refit.inputs.deoblique = True
refit.inputs.xorigin = 'cen'
refit.inputs.yorigin = 'cen'
refit.inputs.zorigin = 'cen'
#res =refit.run()

# ======= RESAMPLE
# 3dresample -orient RPI -prefix T1_resampled.nii.gz -inset struct.nii.gz

resample = pe.MapNode(interface=afni.Resample(),
                      iterfield='in_file',
                      name='resample')


resample.inputs.orientation = 'RPI'
resample.inputs.out_file = 'T1_RPI'
resample.inputs.outputtype = 'NIFTI_GZ'


