from vplot import GetOutput
import subprocess
import numpy as np
import os
cwd = os.path.dirname(os.path.realpath(__file__))


def test_MagmOcEarth():
    """Test magma ocean evolution of Earth."""
    # Remove old log file
    subprocess.run(['rm', 'Solarsystem.log'], cwd=cwd)
    # Run vplanet
    subprocess.run(['vplanet', 'vpl.in', '-q'], cwd=cwd)

    # Grab the output
    output = GetOutput(path=cwd)

    # Primary Variables: Earth -- checks MagmOc parameters
    assert np.isclose(output.log.final.Earth.PotTemp, 2237.880741)
    assert np.isclose(output.log.final.Earth.SurfTemp, 2236.094078)
    assert np.isclose(output.log.final.Earth.SolidRadius, 0.904040)
    assert np.isclose(output.log.final.Earth.WaterMassMOAtm, 4.907582)
    assert np.isclose(output.log.final.Earth.WaterMassSol, 0.086785)
    assert np.isclose(output.log.final.Earth.OxygenMassMOAtm, 1.833603e+18)
    assert np.isclose(output.log.final.Earth.OxygenMassSol, 8.771056e+17)
    assert np.isclose(output.log.final.Earth.HydrogenMassSpace, 8.761559e+17)
    assert np.isclose(output.log.final.Earth.OxygenMassSpace, 4.242889e+18)
    assert np.isclose(output.log.final.Earth.CO2MassMOAtm, 1.753694e-296)
    assert np.isclose(output.log.final.Earth.CO2MassSol, 1.753694e-296)


if __name__ == "__main__":
    test_MagmOcEarth()
