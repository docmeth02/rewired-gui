from distutils.core import setup
import py2exe
import glob, sys, os

# returns a list of all the files in a directory tree
def walk_dir(dirname):
  files = []
  ret = [ (dirname, files) ]
  for name in os.listdir(dirname):
    fullname = os.path.join(dirname, name)
    if os.path.isdir(fullname):
      ret.extend(walk_dir(fullname))
    else:
      files.append(fullname)
  return ret

includes = []
excludes = []
packages = []
dll_excludes = []

setup(
    name="reWired Server",
    version="0.1",
    description="A re:invented wired server",
    author_email="docmeth02@googlemail.com",
    maintainer="docmeth02",
    maintainer_email="docmeth02@googlemail.com",
    url="http://rewired.info",
    author="re-wired.info",
    windows=[{"script": "rewired server.py",
                "icon_resources": [(1, "re-wired.ico")]}],
    data_files=[],
    options={"py2exe": {"compressed": 2,
                        "optimize": 2,
                        "includes": includes,
                        "excludes": excludes,
                        "packages": packages,
                        "dll_excludes": dll_excludes,
                        "bundle_files": 3,
                        "dist_dir": "windist",
                        "xref": False,
                        "skip_archive": False,
                        "ascii": False,
                        "custom_boot_script": '',
        }
    }
)




"""
setup(
    options = {"py2exe": {"compressed": 2,
                        'name':'reWired Server',
                        'version':'20130402A2',
                        'description':'A re:invented wired server',
                        "optimize": 2,
                        "includes": includes,
                        "excludes": excludes,
                        "packages": packages,
                        "dll_excludes": dll_excludes,
                        "bundle_files": 3,
                        "dist_dir": "windist",
                        "xref": False,
                        "skip_archive": False,
                        "ascii": False,
                        "custom_boot_script": '',
                         }
              },
    windows = [{"script": "rewired server.py",
                "icon_resources": [(1, "re-wired.ico")]}]

)
"""
