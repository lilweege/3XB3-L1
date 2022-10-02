## Header information:

  - Author #1: Luigi Quattrociocchi (quattrl@mcmaster.ca)
  - Author #2: Dennis Fong (fongd1@mcmaster.ca)
  - Gitlab URL: http://gitlab.cas.mcmaster.ca/quattrl/l1-graph-lab
  - Avenue to Learn group name: Graph 42

## Running instructions

### Setup
- Clone the repository and change directory to the newly created folder.
- Run the command `pipenv install --dev`.

### Notebook
To run the notebook: `pipenv run python -m jupyter lab graph_lab.ipynb`

### Testing
To run the tests, execute the following commands:
- `pipenv run python -m coverage run -m pytest -v tests/test_*.py`
- `pipenv run python -m coverage report`


### Benchmarking
- If it exists, delete the file `outputs/pyperf_measurements.json`
- To run the benchmark: `pipenv run python benchmark.py -o outputs/pyperf_measurements.json`
- To plot the results: `python -m pyperf hist outputs/pyperf_measurements.json`
