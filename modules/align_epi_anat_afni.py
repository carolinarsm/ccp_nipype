from nipype.interfaces.base.import (
    TraitedSpec,
    CommandLineInputSpec,
    CommandLine,
    File
)

import os

class AfniEpi2AnatInputSpec(CommandLineInputSpec):
    epi_file = File(desc = "Epi file", exists = True, mandatory = True,
                      argstr = "%s")

    anat_file = File(desc = "Anatomy File", exists = True, mandatory = True,
                      argstr = "%s")


class AfniEpi2AnatOutputSpec(TraitedSpec):
    output_file = File(desc = "Aligned file", exists = "True")


class AfniEpi2AnatTask(CommandLine):
    input_spec = AfniEpi2AnatInputSpec
    output_spec = AfniEpi2AnatOutputSpec
    cmd = 'align_epi_anat.py'



if __name__== '__main__':
    aligner = AfniEpi2AnatTask(input_file='existing_file')
    print aligner.cmdline
    aligner.run()