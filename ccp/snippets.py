# Multiple files input
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from nipype.interfaces.base import InputMultiPath, traits, File, BaseInterfaceInputSpec, BaseInterface, TraitedSpec, \
    Directory

input_files = InputMultiPath(
        traits.Either(traits.List(File(exists=True)), File(exists=True)),
        mandatory=True,
        desc="list of 4D nifti runs per condition",
        copyfile=False)

other_priors = InputMultiPath(
        File(exist=True), desc='alternative prior images',
        argstr='-A %s', minlen=3, maxlen=3)

out_basename = File(desc='base name of output files',
                    argstr='-o %s')  # uses in_file name as basename if none given

# noinspection PyPep8,PyPep8
img_type = traits.Enum((1, 2, 3), desc='int specifying type of image: (1 = T1, 2 = T2, 3 = PD)',
                       argstr='-t %d')



    in_folder = Directory(desc='folder with DICOM images to convert',
                          argstr='%s/*.dcm',
                          position=-1,
                          mandatory=True,
                          exists=True)



    # Non-linear experimental
    _nwarp_types = ['bilinear',
                    'cubic', 'quintic', 'heptic', 'nonic',
                    'poly3', 'poly5', 'poly7', 'poly9']  # same non-hellenistic
    nwarp = traits.Enum(
        *_nwarp_types, argstr='-nwarp %s',
        desc='Experimental nonlinear warping: bilinear or legendre poly.')

    _dirs = ['X', 'Y', 'Z', 'I', 'J', 'K']
    nwarp_fixmot = traits.List(
        traits.Enum(*_dirs),
        argstr='-nwarp_fixmot%s',
        desc='To fix motion along directions.')

    nwarp_fixdep = traits.List(
        traits.Enum(*_dirs),
        argstr='-nwarp_fixdep%s',
        desc='To fix non-linear warp dependency along directions.')




class VolregOutputSpec(TraitedSpec):
    out_file = File(desc='registered file', exists=True)
    md1d_file = File(desc='max displacement info file', exists=True)
    oned_file = File(desc='movement parameters info file', exists=True)
    oned_matrix_save = File(desc='matrix transformation from base to input', exists=True)


EXAMPLES OF METHODS INSIDE 'class INTERFACE(AFNICommand)' DEFINITION

1)
_cmd = '3dAllineate'
    input_spec = AllineateInputSpec
    output_spec = AllineateOutputSpec

    def _format_arg(self, name, trait_spec, value):
        if name == 'nwarp_fixmot' or name == 'nwarp_fixdep':
            arg = ' '.join([trait_spec.argstr % v for v in value])
            return arg
        return super(Allineate, self)._format_arg(name, trait_spec, value)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        if not isdefined(self.inputs.out_file):
            outputs['out_file'] = self._gen_filename(self.inputs.in_file,
                                                     suffix=self.inputs.suffix)
        else:
            outputs['out_file'] = os.path.abspath(self.inputs.out_file)
        return outputs

    def _gen_filename(self, name):
        if name == 'out_file':
            return self._list_outputs()[name]



2)

 _cmd = '3dBrickStat'
    input_spec = BrickStatInputSpec
    output_spec = BrickStatOutputSpec

    def aggregate_outputs(self, runtime=None, needed_outputs=None):

        outputs = self._outputs()

        outfile = os.path.join(os.getcwd(), 'stat_result.json')

        if runtime is None:
            try:
                min_val = load_json(outfile)['stat']
            except IOError:
                return self.run().outputs
        else:
            min_val = []
            for line in runtime.stdout.split('\n'):
                if line:
                    values = line.split()
                    if len(values) > 1:
                        min_val.append([float(val) for val in values])
                    else:
                        min_val.extend([float(val) for val in values])

            if len(min_val) == 1:
                min_val = min_val[0]
            save_json(outfile, dict(stat=min_val))
        outputs.min_val = min_val

        return outputs


3)

    _cmd = '3dcalc'
    input_spec = CalcInputSpec
    output_spec = AFNICommandOutputSpec

    def _format_arg(self, name, trait_spec, value):
        if name == 'in_file_a':
            arg = trait_spec.argstr % value
            if isdefined(self.inputs.start_idx):
                arg += '[%d..%d]' % (self.inputs.start_idx,
                                     self.inputs.stop_idx)
            if isdefined(self.inputs.single_idx):
                arg += '[%d]' % (self.inputs.single_idx)
            return arg
        return super(Calc, self)._format_arg(name, trait_spec, value)

    def _parse_inputs(self, skip=None):
        """Skip the arguments without argstr metadata
        """
        return super(Calc, self)._parse_inputs(
            skip=('start_idx', 'stop_idx', 'other'))


4)
    _cmd = '3dTcorrMap'
    input_spec = TCorrMapInputSpec
    output_spec = TCorrMapOutputSpec
    _additional_metadata = ['suffix']

    def _format_arg(self, name, trait_spec, value):
        if name in self.inputs._thresh_opts:
            return trait_spec.argstr % self.inputs.thresholds + [value]
        elif name in self.inputs._expr_opts:
            return trait_spec.argstr % (self.inputs.expr, value)
        elif name == 'histogram':
            return trait_spec.argstr % (self.inputs.histogram_bin_numbers,
                                        value)
        else:
            return super(TCorrMap, self)._format_arg(name, trait_spec, value)



onset_files = self.inputs.stim_files
for myfile in onset_files:
    do_whatever(myfile)


#############
>>> for i, v in enumerate(['tic', 'tac', 'toe']):
...     print i, v
...
0 tic
1 tac
2 toe


>>> questions = ['name', 'quest', 'favorite color']
>>> answers = ['lancelot', 'the holy grail', 'blue']
>>> for q, a in zip(questions, answers):
...     print 'What is your {0}?  It is {1}.'.format(q, a)
...
What is your name?  It is lancelot.
What is your quest?  It is the holy grail.
What is your favorite color?  It is blue.



def _format_arg(self, name, trait_spec, value):
        if name == 'stim_times':
            num = len(self.inputs.stim_times)
            names = self.inputs.stim_times
            labels = self.inputs.stim_labels
            print num
            print names
            print labels
            i = 1
            mylist = list()

            for n, l in zip(names, labels):
                mylist.append('-stim_times %d ' % i + '{0} -label {1}'.format(n, l))
                i += 1
            s = ' '.join(mylist)
            print s
            print trait_spec.argstr % (self.inputs.stim_times, s)

        else:
             return super(CCPDeconvolve, self)._format_arg(name, trait_spec, value)


        #    timefiles = self.inputs.stim_times
        #    labels = self.inputs.stim_labels

#        for myfile in timefiles:

####

files = ['run01', 'run02', 'run03']
labels = ['L1', 'L2', 'L3']
numbers = [1, 2, 3]

argstr = '-stim_times %s %s -stim_label %s'
' '.join([argstr % x for x in zip(numbers, files, labels)])


# XOR attributes
class SmoothEstimateInputSpec(FSLCommandInputSpec):
    dof = traits.Int(argstr='--dof=%d', mandatory=True,
                     xor=['zstat_file'],
                     desc='number of degrees of freedom')
    mask_file = File(argstr='--mask=%s',
                     exists=True, mandatory=True,
                     desc='brain mask volume')
    residual_fit_file = File(argstr='--res=%s',
                             exists=True, requires=['dof'],
                             desc='residual-fit image file')
    zstat_file = File(argstr='--zstat=%s',
                      exists=True, xor=['dof'],
                      desc='zstat image file')