import shutil, os, subprocess
import site, sys
from importlib import util
from distutils.core import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
   def run(self):
       install.run(self)
       # Post-installation routine
       ANARCI_LOC = os.path.join(site.getsitepackages()[0], 'anarci') # site-packages/ folder
       ANARCI_BIN = sys.executable.split('python')[0] # bin/ folder
       print(f"{sys.executable=}, {ANARCI_BIN=}")

       shutil.copy('bin/ANARCI', ANARCI_BIN) # copy ANARCI executable
       print("INFO: ANARCI lives in: ", ANARCI_LOC) 

       # Build HMMs from IMGT germlines
       os.chdir("build_pipeline")
       # Judge if Dir HMMs is not empty
       if not os.path.exists("./HMMs") or len(os.listdir("./HMMs")) == 0:
        print('INFO: Downloading germlines from IMGT and building HMMs...')
        print("INFO: running 'RUN_pipeline.sh', this will take a couple a minutes.")
        proc = subprocess.Popen(["bash", "RUN_pipeline.sh"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        o, e = proc.communicate()

        print(o.decode())
        print(e.decode())
       
       # Copy HMMs where ANARCI can find them
       shutil.copy( "curated_alignments/germlines.py", ANARCI_LOC )
       os.mkdir(os.path.join(ANARCI_LOC, "dat"))
       shutil.copytree( "HMMs", os.path.join(ANARCI_LOC, "dat/HMMs/") )

setup(name='anarci',
     version='1.3',
     description='Antibody Numbering and Receptor ClassIfication',
     author='James Dunbar',
     author_email='opig@stats.ox.ac.uk',
     url='http://opig.stats.ox.ac.uk/webapps/ANARCI',
     packages=['anarci'],
     package_dir={'anarci': 'lib/python/anarci'},
     data_files = [ ('bin', ['bin/muscle', 'bin/muscle_macOS', 'bin/ANARCI']) ],
     include_package_data = True,
     scripts=['bin/ANARCI'],
     cmdclass={"install": CustomInstallCommand, }, # Run post-installation routine
    )
