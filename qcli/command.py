#!/usr/bin/env python
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from numpy import inf
from datetime import datetime
from sys import stderr
import sys
from optparse import (OptionParser, OptionGroup, Option, 
                      OptionValueError, OptionError)
from qcli.option_parsing import make_option
from qcli.log import StdErrLogger

def clmain(cmd_constructor, local_argv):
    logger = logger_constructor()
    cmd = cmd_constructor()
    try:
        result = cmd(local_argv[1:])
    except Exception, e:
        # Possibly do *something*
        raise e
    #else:
    #    output_mapping = cmd.getOutputFilepaths(result, kwargs)
#
#        for k, v in result.items():
#            v.write(output_mapping[k])
#
    return 0

# def argv_to_kwargs(cmd, argv):
#     pass

class Parameter(object):
    
    def __init__(self,
                 Type,
                 Help,
                 Name,
                 Required=False,
                 Default=None,
                 DefaultDescription=None):
        self.Type = Type
        self.Help = Help
        self.Default = Default
        self.Name = Name
        self.Required = Required
        self.DefaultDescription = DefaultDescription

        if self.Required and self.Default is not None:
            raise IncompetentDeveloperError("Required parameters cannot have defaults, idiot!!!")

class CLOption(Parameter):
    
    def __init__(self, Type, Help, Name, LongName, CLType, CLAction='store',
                 Required=False, Default=None, DefaultDescription=None,
                 ShortName=None):
        self.LongName = LongName
        self.CLType = CLType
        self.CLAction = CLAction
        self.ShortName = ShortName
        
        super(CLOption,self).__init__(Type=Type,Help=Help,Name=Name,Required=Required,Default=Default,DefaultDescription=DefaultDescription)
        
        if LongName != self.Name:
            self.DepWarn = "parameter %s will be renamed %s in QIIME 2.0.0" % (self.LongName, self.Name)
        else:
            self.DepWarn = ""

    def __str__(self):
        return '-%s/--%s' % (self.ShortName, self.LongName)
        
    @classmethod
    def fromParameter(cls, parameter, LongName, CLType, CLAction='store',
                      ShortName=None):
        result = cls(Type=parameter.Type,
                     Help=parameter.Help,
                     Name=parameter.Name,
                     Required=parameter.Required,
                     LongName=LongName,
                     CLType=CLType,
                     CLAction=CLAction,
                     Default=parameter.Default,
                     DefaultDescription=parameter.DefaultDescription,
                     ShortName=ShortName)
        return result

class CommandError(Exception):
    pass

class IncompetentDeveloperError(CommandError):
    pass

class InvalidReturnTypeError(IncompetentDeveloperError):
    pass

class Command(object):
    """ Base class for abstracted command
    """
    _logger = None
    BriefDescription = ''
    LongDescription = ''

    def __init__(self, **kwargs):
        """ """
        self._logger = StdErrLogger
        self.Parameters = []
        self.Parameters.extend(self._get_default_parameters())
        self.Parameters.extend(self._get_parameters())

    def __call__(self, **kwargs):
        """
        """
        self_str = str(self.__class__)
        self._logger.info('Starting command: %s' % self_str)
        try:
            result = self.run(**kwargs)
        except Exception, e:
            self._logger.fatal('Shit went down: %s' % self_str)
            raise e
        else:
            self._logger.info('Completed command: %s' % self_str)
        
        if not isinstance(result, dict):
            self._logger.fatal('Shit went wrong: %s' % self_str)
            raise InvalidReturnTypeError("Unexpected return type!")

        return result

    def run(self, **kwargs):
        raise NotImplementedError("All subclasses must implement run.")
    
    def _get_default_parameters(self):
        return [Parameter(Type=bool,
                          Help='Print information during execution -- useful for debugging',
                          Name='verbose',
                          Required=False,
                          Default=False)]

    def _get_parameters(self):
        raise NotImplementedError("All subclasses must implement _get_parameters")

class FilterSamplesFromOTUTable(Command):
    BriefDescription = "Filters samples from an OTU table on the basis of the number of observations in that sample, or on the basis of sample metadata. Mapping file can also be filtered to the resulting set of sample ids."
    LongDescription = ''

    def __init__(self, **kwargs):
        super(FilterSamplesFromOTUTable, self).__init__(**kwargs)

    def _get_parameters(self):
        return [
                Parameter(Type='biom-table',Help='the input otu table',Name='biom-table', Required=True),
                Parameter(Type=float,Help='the minimum total observation count in a sample for that sample to be retained',Name='min-count', Default=0),
                Parameter(Type=float,Help='the maximum total observation count in a sample for that sample to be retained',Name='max-count', Default=inf,DefaultDescription='infinity')]
    
    def run(self, **kwargs):
        print self.Parameters

class CLCommandParser(object):
    DisallowPositionalArguments = True
    HelpOnNoArguments = True
    OptionalInputLine = '[] indicates optional input (order unimportant)'
    RequiredInputLine = '{} indicates required input (order unimportant)'

    def __init__(self):
        if len(self.UsageExamples) < 1:
            raise IncompetentDeveloperError("How the fuck do I use this "
                                            "command?")

    def getOutputFilepaths(results, **kwargs):
        raise NotImplementedError("All subclasses must implement "
                                  "getOutputFilepaths.")

def build_usage_lines(required_params, usage_examples, optional_input_line, 
                      required_input_line, long_description):
    """ Build the usage string from components """
    line1 = 'usage: %prog [options] ' + '{%s}' %\
     ' '.join(['%s %s' % (str(rp),rp.Name.upper())\
               for rp in required_params])
    
    formatted_usage_examples = []
    for title, description, command in usage_examples:
        title = title.strip(':').strip()
        description = description.strip(':').strip()
        command = command.strip()
        if title:
            formatted_usage_examples.append('%s: %s\n %s' %\
             (title,description,command))
        else:
            formatted_usage_examples.append('%s\n %s' % (description,command))
    
    formatted_usage_examples = '\n\n'.join(formatted_usage_examples)
    
    lines = (line1,
             '', # Blank line
             optional_input_line,
             required_input_line,
             '', # Blank line
             long_description,
             '', # Blank line
             'Example usage: ',\
             'Print help message and exit',
             ' %prog -h\n',
             formatted_usage_examples)
    
    return '\n'.join(lines)

class Interface(object):
    CommandConstructor = None

    def __init__(self, **kwargs):
        """ """
        self.Options = []
        self.CmdInstance = None

        if self.CommandConstructor is None:
            raise IncompetentDeveloperError("I don't have a command constructor, idiot!!!")
        
        self.CmdInstance = self.CommandConstructor(**kwargs)
        for parameter in self.CmdInstance.Parameters:
            option = self._option_factory(parameter)
            self.Options.append(option)
    
    def __call__(self, in_, *args, **kwargs):
        self._the_in_validator(in_)
        parameter_instances = self._input_handler(in_, *args, **kwargs)
        return self._output_handler(self.CmdInstance(parameter_instances))

    def _the_in_validator(self, in_):
        """The job securator"""
        raise NotImplementedError("DO IT!")

    def _option_factory(self):
        raise NotImplementedError("DO IT!")

    def _input_handler(self, in_, *args, **kwargs):
        raise NotImplementedError("DO IT!")

    def _output_handler(self, results):
        raise NotImplementedError("DO IT!")

# an option is interface dependent
# a parameter is interface independent

class CLInterface(Interface):
    DisallowPositionalArguments = True
    HelpOnNoArguments = True 
    OptionalInputLine = '[] indicates optional input (order unimportant)'
    RequiredInputLine = '{} indicates required input (order unimportant)'
    
    def __init__(self, **kwargs):
        self.UsageExamples = []
        self.UsageExamples.extend(self._get_usage_examples())
        
        self.ParameterConversionInfo = {'verbose':{'short-name':'v',
                                                   'long-name':'verbose',
                                                   'cl-type':None,
                                                   'cl-action':'store_true'}}
        
        self.ParameterConversionInfo.update(self._get_param_conv_info())
    
        super(CLInterface, self).__init__(**kwargs)
        
        self.Options.extend(self._get_additional_options())

    def _get_param_conv_info(self):
        raise NotImplementedError("Must define _get_param_conv_info")
    
    def _get_usage_examples(self):
        raise NotImplementedError("Must define _get_usage_examples")
    
    def _get_additional_options(self):
        raise NotImplementedError("Must define _get_additional_options")

    def _the_in_validator(self, in_):
        if not isinstance(in_, list):
            raise IncompetentDeveloperError("The in_ validator is very upset.")

    def _option_factory(self, parameter):
        name = parameter.Name
        if name not in self.ParameterConversionInfo:
            raise IncompetentDeveloperError("YOU IIIIIDDIOT!")

        return CLOption.fromParameter(parameter, 
                     self.ParameterConversionInfo[name]['long-name'],
                     self.ParameterConversionInfo[name]['cl-type'],
                     self.ParameterConversionInfo[name]['short-name'])

    def _input_handler(self, in_, *args, **kwargs):
        """ Constructs the OptionParser object and parses command line arguments
        
            parse_command_line_parameters takes a dict of objects via kwargs which
             it uses to build command line interfaces according to standards 
             developed in the Knight Lab, and enforced in QIIME. The currently 
             supported options are listed below with their default values. If no 
             default is provided, the option is required.
            
            script_description
            script_usage = [("","","")]
            version
            required_options=None
            optional_options=None
            suppress_verbose=False
            disallow_positional_arguments=True
            help_on_no_arguments=True
            optional_input_line = '[] indicates optional input (order unimportant)'
            required_input_line = '{} indicates required input (order unimportant)'
            
           These values can either be passed directly, as:
            parse_command_line_parameters(script_description="My script",\
                                         script_usage=[('Print help','%prog -h','')],\
                                         version=1.0)
                                         
           or they can be passed via a pre-constructed dict, as:
            d = {'script_description':"My script",\
                 'script_usage':[('Print help','%prog -h','')],\
                 'version':1.0}
            parse_command_line_parameters(**d)
        
        """
        # command_line_text will usually be nothing, but can be passed for
        # testing purposes

        # Do we need this? Was used for testing
        #command_line_args = set_parameter('command_line_args',kwargs,None)

        required_opts = [opt for opt in self.Options if opt.Required]
        optional_opts = [opt for opt in self.Options if not opt.Required]
        
        # Build the usage and version strings
        usage = build_usage_lines(required_opts)
        version = 'Version: %prog ' + __version__

        # Instantiate the command line parser object
        parser = OptionParser(usage=usage, version=version)

        # What does this do?
        #parser.exit = set_parameter('exit_func',kwargs,parser.exit)
        
        # If no arguments were provided, print the help string (unless the
        # caller specified not to)

        # Need to figure out what to do with command_line_args
        #if self.HelpOnNoArguments and (not command_line_args) and len(argv) == 1:
        if self.HelpOnNoArguments and len(in_) == 1:
            parser.print_usage()
            return parser.exit(-1)

        # Process the required options
        if required_params:
            # Define an option group so all required options are
            # grouped together, and under a common header
            required = OptionGroup(parser, "REQUIRED options",
                "The following options must be provided under all circumstances.")
            for rp in required_params:
                # if the option doesn't already end with [REQUIRED], 
                # add it.
                if not rp.Help.strip().endswith('[REQUIRED]'):
                    rp.Help += ' [REQUIRED]'

                option = make_option('-' + rp.ShortName, '--' + rp.LongName, type=rp.CLType, help=rp.Help)
                required.add_option(option)
            parser.add_option_group(required)

        # Add the optional options
        for op in optional_params:
            help_text = '%s [default: %s]' % (op.Help, op.DefaultDescription)
            option = make_option('-' + op.ShortName, '--' + op.LongName, type=op.CLType,
                    help=help_text, default=op.Default)
            parser.add_option(option)
        
        # Parse the command line
        # command_line_text will None except in test cases, in which 
        # case sys.argv[1:] will be parsed

        # Need to figure out what to do with command_line_args
        #opts,args = parser.parse_args(command_line_args)
        opts,args = parser.parse_args(in_)
        
        # If positional arguments are not allowed, and any were provided,
        # raise an error.
        if self.DisallowPositionalArguments and len(args) != 0:
            parser.error("Positional argument detected: %s\n" % str(args[0]) +\
             " Be sure all parameters are identified by their option name.\n" +\
             " (e.g.: include the '-i' in '-i INPUT_DIR')")

        # Test that all required options were provided.
        if required_params:
            required_option_ids = [o.dest for o in required.option_list]
            for required_option_id in required_option_ids:
                if getattr(opts,required_option_id) == None:
                    return parser.error('Required option --%s omitted.' \
                                 % required_option_id)
                
        # Return the parser, the options, and the arguments. The parser is returned
        # so users have access to any additional functionality they may want at 
        # this stage -- most commonly, it will be used for doing custom tests of 
        # parameter values.
        return parser, opts, args

    def _output_handler(self, results):
        print results

    def getOutputFilepaths(results, **kwargs):
        mapping = {}

        for k,v in results.items():
            if isinstance(v, FilePath):
                output_fp = str(v)
            else:
                # figure out filepath
                pass

            mapping[k] = output_fp

        return mapping

class CLFilterSamplesFromOTUTable(CLInterface):
    CommandConstructor = FilterSamplesFromOTUTable

    def _get_usage_examples(self):
        return [("Abundance filtering (low coverage)","Filter samples with fewer than 150 observations from the otu table.","%prog -i otu_table.biom -o otu_table_no_low_coverage_samples.biom -n 150"),
                ("Abundance filtering (high coverage)","Filter samples with greater than 149 observations from the otu table.","%prog -i otu_table.biom -o otu_table_no_high_coverage_samples.biom -x 149"),
                ("Metadata-based filtering (positive)","Filter samples from the table, keeping samples where the value for 'Treatment' in the mapping file is 'Control'","%prog -i otu_table.biom -o otu_table_control_only.biom -m map.txt -s 'Treatment:Control'"),
                ("Metadata-based filtering (negative)","Filter samples from the table, keeping samples where the value for 'Treatment' in the mapping file is not 'Control'","%prog -i otu_table.biom -o otu_table_not_control.biom -m map.txt -s 'Treatment:*,!Control'"),
                ("List-based filtering","Filter samples where the id is listed in samples_to_keep.txt","%prog -i otu_table.biom -o otu_table_samples_to_keep.biom --sample_id_fp samples_to_keep.txt")]

    def _get_param_conv_info(self):
        return {'biom-table':{'short-name':'i',
                              'long-name':'input_fp',
                              'cl-type':'existing_filepath'},
                'min-count':{'short-name':'n',
                             'long-name':'min_count',
                             'cl-type':float},
                'max-count':{'short-name':'x',
                             'long-name':'max_count',
                             'cl-type':float}}
   
    def _get_additional_options(self):
        return [CLOption(Type='biom-table',
                                        Help='the output otu table',
                                        Name='biom-table',
                                        Required=True,
                                        LongName='output_fp',
                                        CLType='new_filepath',
                                        ShortName='o')]

# ParameterMapping['biom_table'] = make_option('-i','--input_fp',type="existing_filepath", help='the input otu table filepath in biom format')
# ParameterMapping['output_fp'] = make_option('-o','--output_fp',type="new_filepath", help='the output filepath in biom format')
# ParameterMapping['mapping_fp'] = make_option('-m', '--mapping_fp', type='existing_filepath', help='path to the map file [default: %default]')
# ParameterMapping['output_mapping_fp'] = make_option('--output_mapping_fp', type='new_filepath', help='path to write filtered mapping file [default: filtered mapping file is not written]')
# ParameterMapping['sample_id_fp'] = make_option('--sample_id_fp', type='existing_filepath', help='path to file listing sample ids to keep [default: %default]')
# ParameterMapping['valid_states'] = make_option('-s', '--valid_states', type='string', help="string describing valid states (e.g. 'Treatment:Fasting') [default: %default]")
# ParameterMapping['min_count'] = make_option('-n', '--min_count', type='int', default=0, help="the minimum total observation count in a sample for that sample to be retained [default: %default]")
# ParameterMapping['max_count'] = make_option('-x', '--max_count', type='int', default=inf, help="the maximum total observation count in a sample for that sample to be retained [default: infinity]")