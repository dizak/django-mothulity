import os
from glob import glob
from skbio.io import sniff, read


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
               file_format="fastq",
               phred_offset=33):
    input_glob = glob(input_files)
    seqs = [read(i,
                 file_format,
                 phred_offset=phred_offset) for i in input_glob]
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
