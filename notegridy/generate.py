import subprocess
from os import path
from os.path import abspath, dirname

CODE = path.join(abspath(dirname(__file__)), "injected-code")


def generate_phar(dest: str):
    generate_script = path.join(abspath(dirname(__file__)), "generate.php")
    command = f"php -d phar.readonly=off -d phar.require_hash=off {generate_script} {CODE} {dest}"
    subprocess.run(command.split(" "))
