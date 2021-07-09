# Customized 3dDeconvolve interface

import os
import re
import string
from nipype.interfaces.afni.base import AFNICommand, AFNICommandInputSpec, AFNICommandOutputSpec
from nipype.interfaces.base import CommandLineInputSpec, CommandLine, StdOutCommandLine, StdOutCommandLineInputSpec, \
    traits, TraitedSpec, File, InputMultiPath, isdefined, Directory, Undefined, BaseInterfaceInputSpec, \
    BaseInterface


# Used?
# from nipype.utils.filemanip import load_json, save_json, split_filename, fname_presuffix
# all of afni library form nipype's afni interfaces, including AFNI input specs
# os.chdir(datadir)

# defining input and output specs?
# class CCPCommandInputSpec(AFNICommandInputSpec):
# class CCPCommandOutputSpec(TraitedSpec):
# class CCPCommand(AFNICommand)


# AFNI's 3dDeconvolve command ("reduced" version)
# as outputs list stats files to pass to 3ttsat++

class CCPDeconvolveInputSpec(AFNICommandInputSpec):
    in_file = traits.List(File(exists=True),
                          minlen=1,
                          sep=' ',
                          argstr='-input \'%s\'',
                          position=2,
                          mandatory=True,
                          desc="Input(s) file(s) to 3dDeconvolve.",
                          copyfile=False)

    options = traits.Str(desc="options that go before input files",
                         argstr='%s',
                         position=1)

    mask = File(desc="Input mask image.",
                argstr='-mask %s',
                exists=True)

    polort = traits.Int(desc="High pass filter parameter.",
                        argstr='-polort %s',
                        position=3,
                        mandatory=True)

    num_stimts = traits.Int(desc="Number of stimulus time series.",
                            argstr='-num_stimts %s',
                            position=4,
                            mandatory=True)

    motion_regs = File(desc="file with the motion regressors, concatenated for all runs",
                       exists=True,
                       argstr='-ortvec %s mov_reg')

    # STIMULUS lines: -stim_times 1 stimuli/LWMC_CONGRUENT.txt 'BLOCK(0.72,1)' -stim_label 1 lwmc_c
    stim_times = traits.List(File(exists=True),
                             desc="Files with time series, in AFNI format.",
                             mandatory=True,
                             copyfile=False)

    stim_labels = traits.List(traits.Str(),
                              desc="Stimulus labels.",
                              mandatory=True)

    # in the future we can make the format string also an input?
    stimulus = traits.Bool(desc="Stimulus files and labels",
                           mandatory=True,
                           argstr='-stim_times %s %s \'%s\' -stim_label %s %s',
                           position=5)

    # GLMs
    glm_contrasts = traits.List(traits.Str(),
                                desc="List of contrast strings, made from the stim_labels inputs.")

    glm_labels = traits.List(traits.Str(),
                             desc="Contrast labels")

    glms = traits.Bool(desc="Generate contrast specifications?",
                       #                   mandatory=True,
                       argstr='-gltsym \'SYM: %s\' -glt_label %s %s',
                       position=5)

    censor_list = File(desc="1D file containing the censored points",
                       argstr='-censor %s',
                       exists=True)

    model = traits.Either((traits.Enum('BLOCK', 'GAM', 'SPLINE'), traits.Str()),
                          #                    argstr='-gltsym %s',
                          mandatory=True,
                          desc="Response model")

    # out_file = traits.Str(name_template="%s.xmat.1D",
    #                      desc="name for design matrix",
    #                      mandatory=True,
    #                      argstr='-x1D %s')
    out_file = File(name_template="%s.xmat.1D",
                    desc='output design matrix file',
                    argstr='-x1D %s',
                    name_source="in_file")

    bucket = File(desc="output stats",
		  argstr="-bucket %s")


#    img_file = File(name_template="%s.png",
#                    desc='output design matrix file',
#                    argstr='-xjpeg %s',
#                    name_source="in_file")

    xmat_only = traits.Bool(desc="Generate the design matrix X, without running the GLM analysis.",
                            argstr='-x1D_stop')

    output_prefix = traits.Str(desc="Output statistics files prefix",
                               argstr='-prefix %s')

    # results_dir = Directory('results',
    #                        argstr='-rn %s',
    #                        usedefault=True,
    #                        desc='directory to store results in')




class CCPDeconvolveOutputSpec(TraitedSpec):
    out_file = File(exists=True,
                    desc='Design Matrix.')
    
    bucket = File(desc='Output stats bucket.') 


#    img_file = File(desc='Design Matrix image.')

    # results_dir = Directory(desc='directory storing model estimation output')

    # md1d_file = File(desc='max displacement info file', exists=True)
    # oned_file = File(desc='movement parameters info file', exists=True)
    # oned_matrix_save = File(desc='matrix transformation from base to input', exists=True)


class CCPDeconvolve(AFNICommand):
    """Runs a GLM analysis with a reduced version of AFNI's 3dDeconvolve.
    Only a subset of AFNI's 3dDeconvolve options are available.
    For details, see, the `3dDeconvolve documentation.
    <http://http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDeconvolve.html>`_
    Examples
    ========
    #>>> from ccp.interfaces import CCPDeconvolve
    #>>> deconvolve = CCPDeconvolve()
    #>>> deconvolve.inputs.in_files = ['run001', 'run002']
    #>>> res = deconvolve.run() #
    """
    _cmd = '3dDeconvolve'
    input_spec = CCPDeconvolveInputSpec
    output_spec = CCPDeconvolveOutputSpec

    def _format_arg(self, name, trait_spec, value):
        # if name == 'stim_times':
        #    arg = ' '.join([trait_spec.argstr % v for v in value])
        #    return arg
        if name == 'stimulus':
            n = len(self.inputs.stim_times)
            st = self.inputs.stim_times
            sl = self.inputs.stim_labels
            mod = [self.inputs.model] * n
            num = range(1, n + 1)
            arg = ' '.join([trait_spec.argstr % z for z in zip(num, st, mod, num, sl)])
            return arg

        elif name == 'glms':
            n = len(self.inputs.glm_contrasts)
            gc = self.inputs.glm_contrasts
            gl = self.inputs.glm_labels
            num = range(1, n + 1)
            arg = ' '.join([trait_spec.argstr % z for z in zip(gc, num, gl)])
            return arg

        return super(CCPDeconvolve, self)._format_arg(name, trait_spec, value)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        if not isdefined(self.inputs.out_file):
            outputs['out_file'] = self._gen_filename(self.inputs.out_file)
        else:
            outputs['out_file'] = os.path.abspath(self.inputs.out_file)
#        if isdefined(self.inputs.img_file):
#            outputs['img_file'] = os.path.abspath(self.inputs.img_file)
        if isdefined(self.inputs.bucket):
	    outputs['bucket'] = os.path.abspath(self.inputs.bucket)
	    
        return outputs

    def _gen_filename(self, name):
        if name == 'out_file':
            return self._list_outputs()[name]

            # def aggregate_outputs(self, runtime=None, needed_outputs=None):
            #    outputs = self._outputs()
            #    outfile = os.path.abspath(outputs.out_file + '.xmat.1D')
            #    outputs['out_file'] = outfile

            #    return outputs


# 3dinfo to get number of volumes
# Can I get the stdout as a Str without passing through a file?

class NiiInfoInputSpec(CommandLineInputSpec):
    in_file = File(exists=True,
                   argstr='-nv %s',
                   mandatory=True,
                   position=1,
                   desc="Input file to 3dInfo.",
                   copyfile=False)


class NiiInfoOutputSpec(TraitedSpec):
    # bold_volumes = traits.Str(mandatory=True,
    num_vols = traits.Str("TR number for a bold series.")


class NiiInfo(CommandLine):
    _cmd = '3dinfo'
    input_spec = NiiInfoInputSpec
    output_spec = NiiInfoOutputSpec

    def aggregate_outputs(self, runtime=None, needed_outputs=None):
        outputs = self._outputs()
        num_vols = runtime.stdout
        outputs.num_vols = num_vols

        return outputs
        # outputs.tr_value = runtime.stdout
        #       return self._outputs.tr_value

        #   def _list_outputs(self, runtime):
        #       outputs = self.output_spec().get()
        #       outputs["num_vols"] = runtime.stdout

        #       return outputs


# 1d_tool.py
# running as command line, with the reduced options for GLM analysis only

class OneDToolInputSpec(CommandLineInputSpec):
    in_file = File(exists=True,
                   argstr='-infile %s',
                   position=1,
                   mandatory=True,
                   desc="Movement Regressor Files (concat all runs).",
                   copyfile=False)

    tr_counts = traits.List(traits.Int(),
                            argstr='-set_run_lengths %s',
                            position=2,
                            mandatory=True,
                            desc="List of volumes per run.")

    out_file = File(name_template='%s',
                    desc="Name for output file.",
                    argstr="-write %s",
                    name_source=['in_file'],
                    position=-1)

    collapse_cols = traits.Enum('min', 'max', 'minabs', 'maxabs', 'euclidean_norm', 'weighted_norm',
                                argstring='-collapse_cols -s',
                                desc="Norm applied to collapsing of columns.")


class OneDToolOutputSpec(TraitedSpec):
    out_file = File(exists=True,
                    desc="Output file generated by 1d_tool.py")


class OneDTool(CommandLine):
    _cmd = '1d_tool.py'
    input_spec = OneDToolInputSpec
    output_spec = OneDToolOutputSpec


# 3dMask_tool
# create union of inputs, output type is byte
# 3dmask_tool -inputs rm.mask_r*+tlrc.HEAD -union -prefix full_mask.$subj

class CCPMaskToolInputSpec(AFNICommandInputSpec):
    in_file = traits.List(File(exists=True), minlen=1, sep=' ',
                          argstr='-inputs %s',
                          position=2,
                          mandatory=True,
                          desc="Input(s) file(s) to apply 3dmask_tool.",
                          copyfile=False)

    out_file = File(name_template="%s_union", desc='output image file name',
                    argstr='-prefix %s', name_source="in_file")


class CCPMaskToolOutputSpec(TraitedSpec):
    out_file = File(desc='Union',
                    exists=True)


class CCPMaskTool(AFNICommand):
    _cmd = '3dmask_tool'
    input_spec = CCPMaskToolInputSpec
    output_spec = CCPMaskToolOutputSpec
