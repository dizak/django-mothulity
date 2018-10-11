import subprocess as sp
from glob import glob
import subprocess as sp
from skbio.io import sniff
import Bio.SeqIO as sio
import math


class ParserError(Exception):
    """
    Inappropriate structure passed to parser.
    """
    pass


def write_file(input_file,
               path,
               chunk_size=8192):
    """
    Saves file from the forms.FileFieldForm to desired path in chunks.

    Parameters
    -------
    input_file: django.core.files.uploadedfile.UploadedFile
        File to be saved.
    path: str
        Path to file save.
    chunk: int, default <8192>
        Size of chunk the stream is divided to.
    """
    with open("/{}/{}".format(path, input_file), "wb+") as fout:
        for chunk in input_file.chunks(chunk_size=chunk_size):
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
    sp.check_output("chmod {} {}".format(mod,
                                         input_file),
                    shell=True)


def convert_size(size_bytes):
    """
    Returns human-readable file size from input in bytes.

    Parameters
    -------
    size_bytes: int
        File size in bytes

    Returns
    -------
    int
        Size in human-readable format.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "{}{}".format(s, size_name[i])


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
                                     shell=True).decode('utf-8').split()[::2]
    else:
        md5_output = sp.check_output("md5sum {}".format(input_file),
                                     shell=True).decode('utf-8').split()[::2]
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
    input_str: str
        Output of the sinfo command.
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
    if len(s_line) > 1:
        raise ParserError("""Found more than one line matching. Check if sinfo
              command output has not been changed.""")
    elif len(s_line) == 0:
        return None
    try:
        return int(s_line[0].split()[3])
    except IndexError:
        return None


def parse_squeue(input_str,
                 slurm_id,
                 key="ST"):
    """
    Parse squeue command output and return desired information.

    Parameters
    -------
    input_str: str
        Output of the squeue command.
    slurm_id: str or int
        slurm's ID of submitted job.
    key: str or int
        Desired value of squeue line to return

    Returns
    -------
    str or int
        Desired value of selected column and row from squeue command.
    None
        Returns None if record not found.
    """
    s_line = [i for i in input_str.split("\n") if str(slurm_id) in i]
    if len(s_line) > 1:
        raise ParserError("""Found more than one line matching. Check if squeue
              command output has not been changed.""")
    elif len(s_line) == 0:
        return None
    cols_vals = {"JOBID": int(s_line[0].split()[0]),
                 "PARTITION": str(s_line[0].split()[1]),
                 "NAME": str(s_line[0].split()[2]),
                 "USER": str(s_line[0].split()[3]),
                 "ST": str(s_line[0].split()[4]),
                 "TIME": str(s_line[0].split()[5]),
                 "NODES": int(s_line[0].split()[6])}
    if cols_vals["JOBID"] == int(slurm_id):
        return cols_vals[key]


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
    return sp.check_output(cmd, shell=True).decode('utf-8').strip()


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
    """
    Return number of all reads in the files.

    Parameters
    -------
    input_file: str
        Path to input files.
    file_format: str
        Format of input files.

    Returns
    -------
    int
        Sum of reads in input files.
    """
    input_glob = glob(input_files)
    seqs = [sio.parse(i,
                      file_format) for i in input_glob]
    return sum([len(list(i)) for i in seqs])


def render_moth_cmd(moth_exec="mothulity",
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
    moth_exec: str, default <mothulity>
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
    moth_opts["output-dir"] = moth_files
    moth_opt_str = " ".join(["--{} {}".format(k.replace("_", "-"), v)
                             for k, v in list(moth_opts.items())])
    return "{} {} {}".format(moth_exec,
                             moth_files,
                             moth_opt_str)
