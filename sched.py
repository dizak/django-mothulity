#! /usr/bin/ env python


import schedule
import subprocess as sp
from mothulity import models


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
    return int(s_line[0].split()[3])


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
