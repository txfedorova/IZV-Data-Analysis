# IZV / Python Data Analysis

Academic Python project focused on exploratory data analysis, statistical testing and geospatial analysis of traffic accident data.

## Project overview

The repository contains several parts of the original coursework:

- `doc.py` - data preprocessing, aggregation and visualization of accident severity and intoxication-related patterns using Pandas, Matplotlib and Seaborn.
- `geo.py` - geospatial processing and visualization with GeoPandas and Contextily, including clustering of accident locations with scikit-learn.
- `stat.ipynb` - statistical hypothesis testing in Jupyter Notebook using Pandas and SciPy.
- `doc.pdf` - original project document included with the coursework.

The original coursework files are preserved unchanged. This README and `requirements.txt` were added only to make the project easier to understand and run from GitHub.

## Analysis included

The project demonstrates several data-analysis tasks on traffic accident records:

- cleaning and filtering tabular data;
- mapping coded values to readable categories;
- grouping and aggregation with Pandas;
- comparison of injury severity by intoxication type;
- analysis of intoxication patterns by vehicle brand;
- statistical hypothesis testing using the chi-squared test;
- conversion of tabular coordinates to geospatial data;
- map visualization and coordinate-system transformation;
- clustering of accident locations.

## Requirements

The code was written for Python 3.10 and uses the libraries listed in `requirements.txt`.

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Input data

The scripts expect an input dataset named:

```text
accidents.pkl.gz
```

The dataset itself is not included in this repository.

## Running the project

For the statistical analysis, open:

```text
stat.ipynb
```

in Jupyter Notebook or JupyterLab.

For the Python scripts, place `accidents.pkl.gz` in the repository root and run:

```bash
python doc.py
python geo.py
```

`doc.py` writes generated figures to the `fig/` directory. `geo.py` generates geospatial visualizations of selected accident data.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── doc.py
├── geo.py
├── stat.ipynb
└── doc.pdf
```

## Notes

This repository contains the original academic project files. The portfolio additions are limited to documentation and dependency information; the original source files have not been rewritten for presentation purposes.
