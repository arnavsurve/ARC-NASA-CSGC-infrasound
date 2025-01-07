# ARC-NASA-CSGC-infrasound

## Please refer to the [dataset-testing](https://github.com/arnavsurve/ARC-NASA-CSGC-infrasound/tree/dataset-testing) branch to view current development progress.

Research under Professor [Paulo Afonso](https://losrios.edu/about-los-rios/contact-us/employee-directory/employee?xid=x76049&id=1085001) at [AMERICAN RIVER COLLEGE (ARC)](https://arc.losrios.edu/) funded by [NASA California Space Grant Consortium (CSGC)](https://casgc.ucsd.edu/) to study infrasound collection and analysis.

Datasets used, sourced from the Boise State University Infrasound Data Repository:

- [Data for Forecasting the Eruption of an Open-vent Volcano Using Resonant Infrasound Tones (Boise State ScholarWorks)](https://scholarworks.boisestate.edu/infrasound_data/1/)
    - Jeffery Johnson, Leighton M. Watson, Jose L. Palma, Eric M. Dunham, Jacob F. Anderson
    - DOI: https://doi.org/10.18122/B21B0C

- [Dataset for Whitewater Sound Dependence on Discharge and Wave Configuration at an Adjustable Wave Feature](https://scholarworks.boisestate.edu/infrasound_data/11/)
    - Taylor Tatum, Jacob Anderson
    - DOI: https://doi.org/10.18122/infrasound_data.11.boisestate


Please create a new directory `/datasets` in the root of the project and download the datasets from the links above. The datasets are too large to be included in the repository and as such are included in the `.gitignore` file to be ignored by git.


## Libraries

Currently, the model requires ObsPy, SciKit-Learn, and NumPy to run. The following instructions will guide you through installing the required libraries.

### Creating and configuring the environment

It is recommended to create a virtual environment to install the required libraries. This will prevent any conflicts with other projects you may be working on. To create and activate a virtual environment using venv, run the following commands:

It is recommended to use `virtualenv` instead of `venv` as it is more reliable.

```bash
python -m pip install --user virtualenv
```

```bash
python3 -m virtualenv venv
source venv/bin/activate
```

After creating and activating the virtual environment, install the required libraries with:

```bash 
pip install -r requirements.txt
```

To deactivate the virtual environment, run:

```bash
deactivate
```

## Running the model

To run the model, execute `python main.py` in the root of the project.
=======
Please create a new directory /datasets in the root of the project and download the datasets from the links above. The datasets are too large to be included in the repository and as such are included in the .gitignore file and are ignored by git.