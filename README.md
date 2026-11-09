# Analysis of Donors and Creditors of Political Parties and Movements in Slovakia

This project focuses on scraping data from [Transparency International Slovakia](https://volby.transparency.sk/financovanie/darcovia) regarding donations to political parties, comparing the results of the analyses and expanding upon them.

The information in `trescak_project_report.pdf` and `protocol.txt` reflects the version of the website crawled in June 2026. The image exports in `image_exports/` reflect the data available on 9 November 2026.

## Installation
```bash
git clone https://github.com/matejtrescak/analysis_donors.git
cd analysis_donors

# commands to create venv, import libraries
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# create database
sqlite3 db.sqlite3 < create_db.sql 

# run crawling script, the script is well documented in comments. it takes around 10 minutes
python3 crawler.py

# open up the jupyter notebook
jupyter notebook visualisations.ipynb
```

## List of files

Here is an overview of the files and directories included in this repository:

| File / Directory | Description |
| :--- | :--- |
| 📁 **`data_sources/`** | |
| └── 📄 `election_dates.csv` | Dates for parliamentary and presidential elections (2002-2024). |
| 📁 **`image_exports/`** | Contains all images used in the project report. |
| 📊 `visualisations.ipynb` | Jupyter Notebook containing the final analysis and visualizations. |
| 🐍 `crawler.py` | Python script used for crawling the API. |
| 💾 `create_db.sql` | SQL script used to create and initialize the database. |
| 📦 `requirements.txt` | List of required Python libraries and dependencies. |
| 📝 `protocol.txt` | Project protocol document. |
| 💡 `api_row.txt` | Helper text file to understand data indices within the code. |
| 📑 `trescak_project_report.pdf`| The final comprehensive project report (in Slovak). |
