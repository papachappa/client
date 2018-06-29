import os
import signal
import subprocess


def terminate_processes(proc_list):
    for p in proc_list:
        if isinstance(p, subprocess.Popen):
            p = p.pid
        elif not isinstance(p, int):
            raise TypeError('process type not recognized')
        try:
            os.kill(p, signal.SIGTERM)
        except:
            pass


def start_popen(cmd, logfile, stdin=None):
    try:
        p = subprocess.Popen(cmd, stdout=logfile, stderr=logfile, stdin=stdin)
    except Exception as e:
        raise RuntimeError(*e.args)
    else:
        return p
