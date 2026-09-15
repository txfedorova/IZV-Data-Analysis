# IZV / Data Analysis and Visualization in Python

Individual academic project from the Brno University of Technology course **Data Analysis and Visualization in Python (IZV)**. The project works with traffic accident data and focuses on data preprocessing, analysis, statistical testing, visualization and geospatial processing in Python.

## Course context

The IZV course covers data acquisition, processing, analysis and visualization in Python. The course project is structured around data acquisition, data preprocessing and analysis, and report generation.

Official course page: https://www.vut.cz/en/students/courses/detail/268299

## Project contents

- `doc.py` — preprocessing, aggregation and visualization of traffic accident data, including injury severity and intoxication-related patterns.
- `geo.py` — geospatial processing and visualization with GeoPandas and Contextily, including clustering of accident locations.
- `stat.ipynb` — statistical hypothesis testing in Jupyter Notebook using Pandas and SciPy.
- `doc.pdf` — project report.

The original coursework files are preserved unchanged. The README and `requirements.txt` were added later to make the repository easier to understand and run.

## Analysis

The project includes:

- filtering and preprocessing tabular data;
- grouping and aggregation with Pandas;
- visualization of accident and injury patterns;
- statistical hypothesis testing with the chi-squared test;
- geospatial data conversion and coordinate-system transformation;
- map visualization and clustering of accident locations.

## Requirements

The code was written for Python 3.10.

Install the required libraries with:

```bash
pip install -r requirements.txt
```

## Input data

The scripts expect a dataset named:

```text
accidents.pkl.gz
```

The dataset is not included in this repository.

## Running the project

Open `stat.ipynb` in Jupyter Notebook or JupyterLab for the statistical analysis.

To run the Python scripts, place `accidents.pkl.gz` in the repository root and run:

```bash
python doc.py
python geo.py
```

`doc.py` saves generated figures to the `fig/` directory. `geo.py` generates geospatial visualizations from selected accident data.

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
