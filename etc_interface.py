import numpy as np
import os
import matplotlib.pyplot as plt

class moons_etc:
    def __init__(self, etc_path=None):

        self.etc_path = etc_path

        if self.etc_path is None:
            if "MOONS_ETC_PATH" in list(os.environ):
                self.etc_path = os.environ["MOONS_ETC_PATH"]

            else:
                self.etc_path = "./moons_etc"

        if not os.path.exists(etc_path):
                raise ValueError("Could not find the ETC at " + self.etc_path
                                 + ", either set the location with the " \
                                 "MOONS_ETC_PATH environment variable, or " \
                                 "pass the location with the etc_path " \
                                 "keyword argument.")

    def run(self, template, resolution="LR", channel="RI", mag=20, system="AB",
            atm_corr=1.2, extended=0, emlineW=0, emlineFWHM=0, emlineF=0,
            redshift=0., seeing=0.8, airmass=1.2, stray=1.0, skyres=1.0,
            NDIT=1, DIT=300, clean=False):

        # All of the parameters accepted by the ETC in the correct order
        param = [resolution, channel, atm_corr, mag, system, extended,
                 template, emlineW, emlineFWHM, emlineF, redshift, seeing,
                 airmass, stray, skyres, NDIT, DIT]

        # Build the command string that will run the ETC
        param_string = " ".join([str(par) for par in param])
        command = self.etc_path + " batch " + param_string

        # Run the ETC
        os.system(command)

        # Load ETC results
        sensitivity = np.loadtxt("Sensitivity_table.txt")
        sensitivity[:, 0] *= 10**4

        if clean:
            os.system("rm Sensitivity_table.txt ETC_output.pdf")

        return sensitivity


if __name__ == "__main__":

    etc_path = "/Users/adam/work/moons/moons_etc_v4.3_osx/moons_etc"
    etc = moons_etc(etc_path)

    sensitivity = etc.run("ssp_1.4Gyr.sav", channel="RI", redshift=1.2, mag=21,
                          clean=True)

    figure = plt.figure(figsize=(10, 5))
    ax = plt.subplot()

    ax.plot(sensitivity[:, 0], sensitivity[:, 1])

    plt.show()
