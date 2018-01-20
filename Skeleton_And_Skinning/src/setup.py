# BUILD script pre vytvorenie .exe suboru z python scriptov pomocou kniznice cx_Freeze
import sys, os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:\\Python3.5\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\Python3.5\\tcl\\tk8.6'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_options = {"packages" : ["numpy", "wx", "pygame"],
                 "include_files" : ["edit.png", "move.png", "mesh.png"]}

executables = [Executable("__init__.py", base=base)]

setup(name = "SkinAndBone",
      version = "0.1",
      description = "Skeleton and Skinning",
      options = {"build_exe": build_options},
      executables = executables
      )