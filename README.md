# ARC-NASA-CSGC-infrasound

Research under Professor [Paulo Afonso](https://losrios.edu/about-los-rios/contact-us/employee-directory/employee?xid=x76049&id=1085001) at [AMERICAN RIVER COLLEGE (ARC)](https://arc.losrios.edu/) funded by [NASA California Space Grant Consortium (CSGC)](https://casgc.ucsd.edu/) to study infrasound collection and analysis.

Datasets used, sourced from the Boise State University Infrasound Data Repository:

- [Data for Forecasting the Eruption of an Open-vent Volcano Using Resonant Infrasound Tones (Boise State ScholarWorks)](https://scholarworks.boisestate.edu/infrasound_data/1/)
    - Jeffery Johnson, Leighton M. Watson, Jose L. Palma, Eric M. Dunham, Jacob F. Anderson
    - DOI: https://doi.org/10.18122/B21B0C

- [Dataset for Whitewater Sound Dependence on Discharge and Wave Configuration at an Adjustable Wave Feature](https://scholarworks.boisestate.edu/infrasound_data/11/)
    - Taylor Tatum, Jacob Anderson
    - DOI: https://doi.org/10.18122/infrasound_data.11.boisestate

Please create a new directory /datasets in the root of the project and download the datasets from the links above. The datasets are too large to be included in the repository and as such are included in the .gitignore file and are ignored by git.


## Libraries

Currently, the project requires InfraPy and ObsPy to run. The following instructions will guide you through installing the required libraries.

### Installing conda

InfraPy requires a conda environment to run. To configure the environment, run the following commands:

- First ensure Anaconda or Miniconda is installed on your system. Download [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Example instructions below to install Miniconda on Linux or MacOS.

Linux/WSL:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O  ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

# After installing, initialize Miniconda with one of the following commands depending on if you are using bash or zsh (hint: bash is the default shell for WSL (Ubuntu))
~/miniconda/bin/conda init bash
~/miniconda/bin/conda init zsh

# Close and reopen your terminal to initialize Miniconda. You should see a (base) prefix in your terminal which indicates the base conda environment is automatically initialized. To disable automatically starting conda on terminal startup, run the following command:
conda config --set auto_activate_base false
```

MacOS:

```bash
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

# After installing, initialize Miniconda with one the following command depending on if you are using bash or zsh (hint: zsh is the default shell for MacOS)
~/miniconda/bin/conda init bash
~/miniconda/bin/conda init zsh

# Close and reopen your terminal to initialize Miniconda. You should see a (base) prefix in your terminal which indicates the base conda environment is automatically initialized. To disable automatically starting conda on terminal startup, run the following command:
conda config --set auto_activate_base false
```

### [InfraPy](https://github.com/LANL-Seismoacoustics/infrapy)

After installing conda, follow the instructions [here](https://github.com/LANL-Seismoacoustics/infrapy?tab=readme-ov-file#downloading) to create a new conda environment for InfraPy.

**or**

Run the following commands to create a new conda environment for InfraPy:

```bash
conda create -n infrapy_env python=3.8
conda activate infrapy_env

pip install git+https://github.com/LANL-Seismoacoustics/infrapy.git
```


You can test the installation by trying to import the infrapy module in a Python script or REPL.

```python
import infrapy
```
