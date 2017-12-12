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


def md5sum(input_file,
           remote=False,
           machine="headnode"):
    """
    Generates md5sum of a file usign linux system command.

    Parameters
    -------
    input_file: str
        Path to input file.
    remote: bool, default <False>
        When <True>, uses ssh to check md5sum on remote machine.
    machine: str
        Name of the machine to call md5sum on when remote set to <True>.
    Returns
    -------
    str
        md5sum.
    """
    if remote is True:
        md5_output = sp.check_output("ssh {} md5sum {}".format(machine,
                                                               input_file),
                                     shell=True).split()[::2]
    else:
        md5_output = sp.check_output("md5sum {}".format(input_file),
                                     shell=True).split()[::2]
    if len(md5_output) > 1:
        return md5_output
    else:
        return md5_output[0]


def parse_sinfo(input_str,
                partition,
                state):
    """
    Parse sinfo command output and return desired information.

    Parameters
    -------
    input_file: str
        Path to input file.
    partition: str
        Partition of desired nodes.
    state: str
        State of desired nodes.

    Return
    -------
    int
        Number of nodes in desired state and partition.
    """
    s_line = [i for i in input_str.split("\n") if partition in i and state in i]
    try:
        return int(s_line[0].split()[3])
    except IndexError:
        return None


def ssh_cmd(cmd,
            machine="headnode"):
    """
    Return output of remote command via ssh. Keys are obligatory!

    Parameters
    -------
    cmd: str
        Command to use.
    machine: str, default <headnode>
        Machine name on which command takes place.

    Return
    -------
    str
        Command output if cmd is fruitful function.
    """
    cmd = "ssh {} {}".format(machine, cmd)
    return sp.check_output(cmd, shell=True).strip()


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
                    moth_opts=None,
                    shell="sbatch",
                    remove_spaces=True,
                    pop_elems=["id",
                               "job_id_id",
                               "amplicon_type"]):
    """
    Returns ready-to-go CLI command for mothulity from dict

    Parameters
    -------
    moth_exec: str, default <mothulity.py>
        Mothulity executable.
    moth_files: str, default <None>
        path/to/input/files.
    moth_opts: dict
        Dict of kvals converted to POSIX CLI optional arguments.
    remove_spaces: bool
        Replace whitespaces with underscores in job_name. Default <True>.

    Returns
    -------
    str
        POSIX mothulity command.
    """
    if remove_spaces is True:
        moth_opts["job_name"] = moth_opts["job_name"].replace(" ", "_")
    for i in pop_elems:
        moth_opts.pop(i)
    moth_opts["run"] = shell
    moth_opt_str = " ".join(["--{} {}".format(k.replace("_", "-"), v)
                             for k, v in moth_opts.items()])
    return "{} {} {}".format(moth_exec,
                             moth_files,
                             moth_opt_str)
