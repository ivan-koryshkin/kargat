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
positional arguments:
  init                  Init Kargat project
  install               Install package `install <package>` or `install` to install all from yaml
  uninstall             Uninstall package `unnstall <package>` or `uninstall` to uninstall all from yaml
  run                   run <command> from yaml

options:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Application mode, default mode "dev"
```