import subprocess

NO_TYPE = "empty"
NO_CMD = "none"
NO_OUT = "stdout"
NO_IN = "stdin"
NO_OWNER = ""


class Job:

    def __init__(self, number, cmd, data=[], owner=NO_OWNER, type=NO_TYPE, title=""):
        self.data = data
        self.id = number
        self.cmd = cmd
        self.type = type
        self.title = title
        self.owner = owner

    def get_type(self):
        return self.type

    def get_command(self):
        return self.cmd

    def get_data(self):
        return self.data

    def is_complete(self):
        return self.type != NO_TYPE and self.cmd != NO_CMD

    def security_check(self):
        for command in self.cmd:
            for word in command:
                if word == "sudo":
                    print("No sudo for you")
                    return False
                return True

    @property
    def execute(self):
        if self.is_complete() and self.security_check():
            #try:
                result = subprocess.run(self.cmd)
                if result.returncode == 0:
                    return result.stdout
                else:
                    return "ERROR:" + result.stderr.decode("ascii")
            #except:
        else:
                print(f'{self.title} could not be executed')


cmd=["python3", "p.py"]
num=0
type="python"
in_line="best input"
cmd.append(in_line)

job=Job(num,cmd,type=type)
job.execute