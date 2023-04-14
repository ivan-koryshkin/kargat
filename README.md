<h2> Kargat </h2>

---

<h3>Simple Python project management system (alpha)</h3> 

---
  

  Clone repository  
```
git clone https://github.com/ivan-koryshkin/kargat.git
```

Install from build
```
pip3 install build
```

Install kargat from src
```
cd kargat 
python3 -m build
pip3 install ./dist/*.whl
```

Usage

```
usage: 
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
    

options:
  -h, --help            show this help message and exit
  -i [INSTALL ...], --install [INSTALL ...]
                        Install packages
  -u [UNINSTALL ...], --uninstall [UNINSTALL ...]
                        Uninstall packages
  -U, --upgrade         Update package if exist on installation step
  --init                Init Kargat project
  -r [RUN ...], --run [RUN ...]
                        Run command from kargat.yaml
  -m MODE, --mode MODE  Kargat mode

```
