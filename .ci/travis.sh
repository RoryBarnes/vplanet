# Miniconda (cached)
export PATH="$HOME/miniconda/bin:$PATH"
if ! command -v conda > /dev/null; then
      wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
      bash miniconda.sh -b -p $HOME/miniconda -u;
      conda config --add channels conda-forge;
      conda config --set always_yes yes;
      conda update --all;
      conda create --yes -n test python=$PYTHON_VERSION
      conda activate test
      conda install tectonic;
      conda install -c conda-forge numpy=$NUMPY_VERSION scipy matplotlib setuptools pytest pytest-cov pip;
fi

# Display some info
#conda info -a

# Install docs stuff
pip install sphinx==2.3.1
pip install breathe==4.14.1
pip install sphinxcontrib-bibtex

# Install coverage stuff
pip install coverage==4.5.4


# Install vplot
pip install git+git://github.com/VirtualPlanetaryLaboratory/vplot.git

#install BigPlanet
pip install h5py
cd bigplanet/
python setup.py install
cd ../

# Build vplanet
export PATH="$TRAVIS_BUILD_DIR:$PATH"
cd $TRAVIS_BUILD_DIR
gcc-4.8 -o vplanet src/*.c -lm -O3 -DGITVERSION=\"Travis-CI\"
sudo mv vplanet /usr/local/bin/vplanet
