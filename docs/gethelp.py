import subprocess
BOLD = r"\x1b[1m"
REGULAR = r"\x1b[0m"

proc = subprocess.Popen(['vplanet', '-h'], stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
output = str(proc.stdout.read())
output = output.replace(REGULAR + BOLD, "")
output = output.replace(BOLD, '**')
output = output.replace(REGULAR, '**')
output = output.replace("----- Command Line Options -----",
                        "Command Line Options\\n--------------------")
output = output.replace("----- Input File -----",
                        "Input File\\n----------")
output = output.replace("----- Input Options -----",
                        "Input Options\\n-------------")
output = output.replace("----- Output Options -----",
                        "Output Options\\n--------------")
output = output.split("\\n")[:-1]
tag = False
with open('help.rst', 'w') as f:
    print("Options Lookup", file=f)
    print("==============", file=f)
    print("", file=f)
    print("The contents of this page can be generated by " +
          "typing :code:`vplanet -h` in a terminal.", file=f)
    print("", file=f)
    print(".. todo:: **@rodluger**: Work on the formatting for " +
          ":doc:`this page <help>`, and make these options " +
          "searchable/organized by module.", file=f)
    print("", file=f)
    print(".. contents:: :local:", file=f)
    print("", file=f)
    for line in output:
        if "Command Line Options" in line:
            tag = True
        if tag:
            print(line, file=f)
            if line.startswith('**'):
                print("", file=f)