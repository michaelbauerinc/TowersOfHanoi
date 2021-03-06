import cx_Freeze
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable("GameRun.py")]

cx_Freeze.setup(
    name="TowersOfHanoi",
    options={"build_exe": {
        "packages":["pygame"],
        "include_files":[
            "background.png", "bottomdisk.png", "four.png", "middledisk.png", "selecttriangle.png", "thirddisk.png", "three.png", "topdisk.png",
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
        ]
    }
},
    executables = executables,
    version='1.0.0'
)