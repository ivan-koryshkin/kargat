import argparse

try:
    import pm
except Exception as ex:
    from . import pm

"""
Install parser
"""
install_parser = argparse.ArgumentParser(add_help=True)
install_parser.add_argument(
    '-i', '--install',
    type=str,
    nargs='*',
    help="Install packages",
    required=False
)
install_parser.add_argument(
    '-u', '--uninstall',
    type=str,
    nargs='*',
    help="Uninstall packages",
    required=False
)

install_parser.add_argument(
    "-U",
    "--upgrade",
    help="Update package if exist on installation step",
    action="store_true",
    default=False,
)
"""
Init parser
"""
init_parser = argparse.ArgumentParser(add_help=False)
init_parser.add_argument(
    "--init",
    help="Init Kargat project",
    action="store_true",
    default=False
)

run_parser = argparse.ArgumentParser(add_help=False)
run_parser.add_argument(
    "-r",
    "--run",
    type=str,
    nargs='*',
    help="Run command from kargat.yaml",
)

mode_parser = argparse.ArgumentParser(add_help=False)
mode_parser.add_argument(
    "-m",
    "--mode",
    type=str,
    nargs=1,
    help="Kargat mode"
)

cmd_parser = argparse.ArgumentParser(
    conflict_handler='resolve',
    parents=[install_parser, init_parser, run_parser, mode_parser],
    usage="""
    Init project
    >: kargat --init

    Install packages
    >: kargat install <package name 0> <package name 1> ... <package name N>
    
    Install package (update if exist)
    >: kargat --install <package name> -U
    >: kargat --install <package name> --prod (install only for prod)
    >: kargat --install <package name> --test (install only for test) 
    
    Install all packages from kargat.yaml
    >: kargat --install
    >: kargat -i
    
    Install or upgrade
    >: kargat --install -U
    >: kargat -i -U
    
    Uninstall package
    >: kargat uninstall <package name> 
        or 
    >: kargat -u <package name>
    
    Uninstall all packages from kargat.yaml
    >: kargat uninstall 
        or
    >: kargat -u 
    """
)

try:
    args = cmd_parser.parse_args()
    cm = pm.ConfigManger(
        init=args.init,
        install=args.install,
        uninstall=args.uninstall,
        run=args.run,
        upgrade=args.upgrade,
        mode=args.mode
    )
    cm.run()
except Exception as ex:
    # cmd_parser.print_help()
    print(ex)
