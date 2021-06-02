import os
import argparse
import subprocess
from phdhelper.helpers.os_shortcuts import get_path, new_path

parser = argparse.ArgumentParser()
parser.add_argument("src_file")
# parser.add_argument("save_file")
args = parser.parse_args()
src_file = os.path.abspath(args.src_file)
# save_file = os.path.abspath(args.save_file)
save_path, save_name = os.path.split(src_file)
save_name = save_name.split(".")[0] + "_output.txt"
save_file = os.path.join(save_path, save_name)


print(f"Reading source file: {src_file}")

with open(src_file, "r") as file:
    src_lines = file.read()

os.system(f"black {src_file}")
run_file = subprocess.Popen(
    ["python", src_file],
    stdout=subprocess.PIPE,
    universal_newlines=True,
)
stdout, _ = run_file.communicate()

output = f"""
```{{python}}
{src_lines}
```

Returns

```
{stdout}```
"""
print(output)

with open(save_file, "w") as file:
    file.write(output)

os.system(f"cat {save_file} | pbcopy")
