import os
import subprocess
import glob


def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode())
    return result

def clean():
    makefile_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(makefile_dir)
    for file in glob.glob("*.pyc"):
        os.remove(file)
    gen_path = os.path.join(makefile_dir, "generation")
    if os.path.exists(gen_path):
        for file in glob.glob(os.path.join(gen_path, "*.pyc")):
            os.remove(file)

def ensure_generation_dir():
    makefile_dir = os.path.dirname(os.path.realpath(__file__))
    generation_dir = os.path.join(makefile_dir, "generation")
    if not os.path.exists(generation_dir):
        os.makedirs(generation_dir)

def compile_files():
    makefile_dir = os.path.dirname(os.path.realpath(__file__))
    for py_file in glob.glob(os.path.join(makefile_dir, "*.py")):
        run_command(f"python -m py_compile {py_file}")

def move_files():
    makefile_dir = os.path.dirname(os.path.realpath(__file__))
    generation_dir = os.path.join(makefile_dir, "generation")
    for pyc_file in glob.glob(os.path.join(makefile_dir, "__pycache__", "*.pyc")):
        os.rename(pyc_file, os.path.join(generation_dir, os.path.basename(pyc_file)))

if __name__ == "__main__":
    ensure_generation_dir()
    clean()
    compile_files()
    move_files()