# Course Radar Scripts

This repository contains DevOpt scripts for uwclassmate.com.

Workflows:

* Update the course information from MyPlan: `fill_db.py`
  This script scrapes course information from MyPlan and stores them in a SQLite file `db.db`.

## Set Up

This repository requires Python 3.11.

* Set up virtual environment:
  ```bash
  python -m venv venv
  ```

* Activate the virtual environment
  For Windows:
  ```bash
  ./venv/Scripts/activate.bat
  ```
  For Mac and Linux:
  ```bash
  source ./venv/bin/activate
  ```
* Set up `.env` file
  
