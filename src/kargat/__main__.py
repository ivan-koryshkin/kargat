import argparse
from kargat import pm
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    'command',
    metavar='command',
    type=str,
    nargs='+',
    help="Run kargat command"
)
parser.add_argument(
    '-m',
    '--mode',
    default="dev",
    help='Application mode, default mode "dev"'
)

args = parser.parse_args()
print(args)

m = pm.ConfigManger(args.command)
m.run()
