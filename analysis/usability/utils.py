from pathlib import Path
import json

import pandas as pd


K = {"item1", "item6", "item11"}
Z = {"item2", "item7", "item12"}
L = {"item3", "item8", "item13"}
V = {"item4", "item9", "item14"}
Fe = {"item5", "item10"}


def read_survey(filepath: Path):
    with filepath.open("r", encoding="utf-8") as survey:
        answers = pd.Series(json.load(survey))
        answers.name = filepath.stem
        if "nasa" in answers.name or "quesi" in answers.name:
            answers = answers.drop("website")
            answers = answers.apply(int)
        return answers


def process_surveys(directory: Path, suffix: str):
    for file in directory.glob(f"*{suffix}"):
        yield read_survey(file)


def read_logfile(filepath: Path):
    try:
        logs = pd.read_csv(filepath, sep=";", header=None, encoding="utf-8")
    except pd.errors.EmptyDataError:
        logs = pd.DataFrame(columns=[0, 1])
    logs.name = filepath.stem
    return logs


def process_logfiles(directory: Path, suffix: str):
    for file in directory.glob(f"*{suffix}"):
        yield read_logfile(file)
