import os
from glob import glob
import subprocess as sp
from skbio.io import sniff
import Bio.SeqIO as sio


def write_file(input_file,
               path):
    """
    Saves file from the forms.FileFieldForm to desired path in chunks.

    Parameters
    -------
    input_file: str
        Name of the input file.
    path: str
        Path to file save.
    """
    with open("/{}/{}".format(path, input_file), "wb+") as fout:
        for chunk in input_file.chunks():
            fout.write(chunk)


def chmod_file(input_file,
               mod=400):
    """
    Chmods file uploaded with forms.FileFieldForm. It is ment to prevent
    execution of uploaded files.

    Parameters
    -------
    input_file: str
        Path to input file.
    mod: int or str, default <400>
        Desired permissions of the input_file
    """
    os.system("chmod {} {}".format(mod,
                                   input_file))


def md5sum(input_file):
    """
    Generates md5sum of a file usign linux system command.

    Parameters
    -------
    input_file: str
        Path to input file.

    Returns
    -------
    str
        md5sum.
    """
    md5_output = sp.check_output("md5sum {}".format(input_file),
                                 shell=True)
    return str(md5_output.split(" ")[0])


def sniff_file(input_file,
               file_frmt="fastq"):
    """
    Returns bool depepending whether file validates as given type.

    Parameters
    -------
    input_file: str
        Path to input file.
    file_frmt: str, default <fastq>
        File type to be validated as.

    Returns
    ------
    bool
        True if file format matches desired file format or False if it does not.

    """
    try:
        if sniff(input_file)[0] == file_frmt:
            return True
    except Exception as e:
        return False


def count_seqs(input_files,
               file_format="fastq"):
    input_glob = glob(input_files)
    seqs = [sio.parse(i,
                      file_format) for i in input_glob]
    return sum([len(list(i)) for i in seqs])


def render_moth_cmd(moth_exec="mothulity.py",
                    moth_files=None,
                    moth_options=None):
    """
    Returns ready-to-go CLI command for mothulity from dict

    Parameters
    -------
    moth_exec: str, default <mothulity.py>
        Mothulity executable.
    moth_files: str, default <None>
        path/to/input/files.
    moth_options: dict
        Dict of kvals converted to POSIX CLI optional arguments.

    Returns
    -------
    str
        POSIX mothulity command.
    """
    moth_opt_zip = zip(moth_options.keys(),
                       moth_options.values())
    moth_opt_str = " ".join(["--{} {}".format(k, v) for k, v in moth_opt_zip])
    return "{} {} {}".format(moth_exec,
                             moth_files,
                             moth_opt_str)
