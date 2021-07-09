import os                                    # system functions
from nipype import config
#config.enable_provenance()
from nipype.interfaces import fsl
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pipeline engine
import nipype.algorithms.rapidart as ra      # artifact detection
import nipype.algorithms.modelgen as model   # model specification
#from nipype.interfaces.fsl import MotionOutliers


## data
data_dir = os.path.abspath('data')
print data_dir

subject_list = ['sub001', 'sub002', 'sub003', 'sub004']
run_list = ['run001', 'run002']
# Map field names to individual subject runs.
info = dict(func=[['subject_id', run_list]])

infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="infosource")

infosource.iterables = ('subject_id', subject_list)

# ===========================================================================================================
# Create an nipype,interface.io.DataSource object
datasource=pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                             outfields=['func']),
                   name= 'datasource')


datasource.inputs.base_directory = data_dir
datasource.inputs.template = '%s/%s.nii.gz'
datasource.inputs.template_args = info
datasource.inputs.sort_filelist = True



# motion outliers node
motion_outliers = pe.MapNode(interface=fsl.MotionOutliers(),
                             iterfield= 'in_file',
                             name="motion_outliers")
#motion_outliers.inputs.in_file = '/home/brain/nipype/outliers_workflow/data/sub001/run001.nii.gz'
metric_list = ['fd', 'dvars']
motion_outliers.iterables = ('metric', metric_list)




# workflow

pipeline2 = pe.Workflow(name="pipeline")
pipeline2.base_dir = os.path.abspath("outliers_outputs")


pipeline2.connect([ (infosource, datasource, [('subject_id', 'subject_id')]),
                   (datasource, motion_outliers, [('func', 'in_file')]),
                   ])

if __name__ == '__main__':
    pipeline2.run()
    pipeline2.write_graph(graph2use='exec')




