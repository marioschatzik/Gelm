# GelAnalyzer to Binary Matrix Automation (`gelm.py`)

A Python script designed to automate the conversion of raw gel electrophoresis data exports from **GelAnalyzer 26.1.1** into a clean, analytical binary presence/absence matrix.

## What it does:
* Parses raw single-column comma-separated exports directly from **GelAnalyzer 26.1.1**.
* Cleans and formats lane numbers and molecular weights (MW), automatically handling formatting noise.
* Excludes ladder lanes (e.g., Lane 1) from the final analysis.
* Generates a binary matrix (`1` or `0`) for each sample lane based on reference molecular weight bins using a **±5% tolerance window** to accommodate experimental calibration drift.
* Allows **dynamic user input** during runtime to specify a custom maximum MW limit (e.g., 2200, 2500, 5000 Da).
* Exports the structured result into a ready-to-use Excel file.

## Important Note on GelAnalyzer MW Configuration:
*Currently, reference Molecular Weight (MW) bins and custom thresholds must be manually defined or selected via the script's interactive inputs.* 
*(Note: Future updates will aim to automate or parse reference MW ladders directly from the GelAnalyzer export files).*

## Requirements:
* Python 3.x
* `pandas`
* `numpy`
* `openpyxl`

## Usage:
Run the script from your terminal:
```bash
python gelm.py

## Citation
If you use `gelm.py` in your research or publications, please cite this repository:
> Chatzikostopoulos, M. (2026). *GelAnalyzer to Binary Matrix Automation (`gelm.py`)*. GitHub repository: https://github.com/marioschatzik/Gelm
