
# coding: utf-8

# In[1]:

import os
import nipype.interfaces.io as nio


# In[2]:

print os.getcwd()
print os.listdir('.')


# In[3]:

dg1 = nio.DataGrabber()
dg1.inputs.base_directory= os.getcwd()
dg1.inputs.sort_filelist = True


# In[4]:

dg1.inputs.template = '*.txt'
#dg.inputs.template_args['outfiles']=[['hola']]
#dg.inputs.template_args['outfiles']=[['*']]


# In[6]:

dg1.run().outputs


# In[ ]:

# Dynamic fields


# In[27]:

dg2 = nio.DataGrabber(infields=['sub_id', 'run_id'], 
                     outfields=['func', 'struct'])


# In[28]:

dg2.inputs.base_directory = os.path.abspath('ds107')


# In[29]:

dg2.inputs.sort_filelist = True


# In[30]:

#dg2.inputs.sub_id = 'sub001'


# In[31]:

dg2.inputs.template = '*'


# In[32]:

dg2.inputs.template_args = {'func': [['sub_id','run_id']],
                           'struct':[['sub_id']]}
dg2.inputs.template_args


# In[41]:

# template for something like (base_dir)/sub001/BOLD/task001_run002/bold.nii.gz
dg2.inputs.field_template = {'func': '%s/BOLD/task001_run%03d/bold.nii.gz',
                            'struct': '%s/anatomy/highres*.nii.gz'}
dg2.inputs.field_template


# In[42]:

# dg2.inputs.template_args['sub_id'] = [['sub001']]
# dg2.inputs.template_args['run_id'] = [[]]
# dg2.inputs.field_template = dict(struct='%s/struct.nii', name=value)


# In[43]:

dg2.inputs.sub_id = ['sub001', 'sub049']
dg2.inputs.run_id = 1


# In[44]:

dg2.run().outputs


# In[45]:

dg2.inputs.sub_id = 'sub001'
dg2.inputs.run_id = [1,2]
dg2.run().outputs


# In[ ]:



