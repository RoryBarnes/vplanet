from vplot import GetOutput
import subprocess
import numpy as np
import os
cwd = os.path.dirname(os.path.realpath(__file__))


def test_ApseLock():
    """Test module Eqtide-Distorb coupling."""
    # Remove old log file
    subprocess.run(['rm', 'ApseLock.log'], cwd=cwd)
    # Run vplanet
    subprocess.run(['vplanet', 'vpl.in', '-q'], cwd=cwd)

    # Grab the output
    output = GetOutput(path=cwd)

    # Checks
    # Primary Variables
    assert np.isclose(output.log.final.b.HEcc, -0.042671)
    assert np.isclose(output.log.final.b.KEcc, -0.069231)
    assert np.isclose(output.log.final.b.DHEccDtEqtide, 2.269581e-15)
    assert np.isclose(output.log.final.b.DKEccDtEqtide, 3.682246e-15)
    assert np.isclose(output.log.final.b.DHeccDtDistOrb, -2.488505e-11)
    assert np.isclose(output.log.final.b.DKeccDtDistOrb, -1.344098e-11)
    assert np.isclose(output.log.final.c.SemiMajorAxis, 6.911428e+09)

    # Other Checks
    assert np.isclose(output.log.final.b.Eccentricity, 0.081326)
    assert np.isclose(output.log.final.b.ArgP, 3.693953)
    assert np.isclose(output.log.final.b.SemiMajorAxis, 2.812439e+09)
    assert np.isclose(output.log.final.c.Eccentricity, 0.193811)
    assert np.isclose(output.log.final.c.ArgP, 5.015526)
    assert np.isclose(output.log.final.c.SemiMajorAxis, 6.911428e+09)


if __name__ == "__main__":
    test_ApseLock()
