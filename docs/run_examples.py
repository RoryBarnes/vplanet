import pathlib
import glob
import os
from importlib.util import spec_from_file_location, module_from_spec

# Path to this directory
path = pathlib.Path(__file__).parents[0].absolute()

# gets the list of examples
example_list = glob.glob(str(path.parents[0] / "examples" / "*" / "makeplot.py"))

# list of examples that should not be ran in the test
no_fly_list = ["AbioticO2", "ChaoticResonances", "DampedCBP", "TidalEarth", "SS_NBody"]


for example in example_list:

    # Example name
    name = pathlib.Path(example).parents[0].name

    if name in no_fly_list:

        # Skip
        continue

    else:

        # Run
        spec = spec_from_file_location(name, example)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
