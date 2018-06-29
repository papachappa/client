import subprocess


APP = 'sispmctl'
cmd2flag = {
    "on":     "-o",
    "off":    "-f",
    "status": "-m",
    "toggle": "-t",
}


def execute_command(cmd):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    out, err = proc.communicate()
    if err:
        raise RuntimeError("{}".format(err.decode('utf-8').strip()))

    output = out.decode('utf-8').strip().split('\n')[1]
    output = 'Status of socket:\n{}'.format(output)
    return output


def socket_manipulation(cmd, socket):
    try:
        flag = cmd2flag[cmd]
    except:
        keys = sorted(cmd2flag.keys())
        raise RuntimeError(
            "Available commands are: " + ', '.join(keys)
        )

    cmd = '{} {} {}'.format(APP, flag, socket)

    res = execute_command(cmd)
    return res
