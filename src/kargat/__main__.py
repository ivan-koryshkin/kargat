import argparse
from kargat import pm
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    'init', 
    metavar='init', 
    type=str, 
    nargs='+', 
    help="Init Kargat project"
)

parser.add_argument(
    'install', 
    metavar='install', 
    type=str, 
    nargs='+', 
    help="Install package `install <package>` or `install` to install all from yaml"
)
parser.add_argument(
    'uninstall', 
    metavar='uninstall', 
    type=str, nargs='+', 
    help="Uninstall package `unnstall <package>` or `uninstall` to uninstall all from yaml")

parser.add_argument('run', metavar='run', type=str, nargs='+', help="run <command> from yaml")
parser.add_argument(
    '-m',
    '--mode',
    default="dev",
    help='Application mode, default mode "dev"'
)

args = parser.parse_args()
print(args)

pm.ConfigManger(args.command).run()