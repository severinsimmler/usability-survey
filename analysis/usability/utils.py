from pathlib import Path
import json

import numpy as np
import pandas as pd
from statsmodels.stats.power import TTestIndPower


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


def cohen_d(x, y):
    size_x = len(x)
    size_y = len(y)
    dof = size_x + size_y - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((size_x - 1) * np.std(x, ddof=1) ** 2 + (size_y - 1) * np.std(y, ddof=1) ** 2) / dof)


class TTestIndPower(TTestIndPower):
    def plot_power(self, dep_var='nobs', nobs=None, effect_size=None,
                   alpha=0.05, ax=None, title=None, plt_kwds=None, figsize=(10, 8), 
                   colors=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33'], **kwds):
        #if pwr_kwds is None:
        #    pwr_kwds = {}
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=figsize)
        plt_alpha = 1 #0.75
        lw = 2
        if dep_var == 'nobs':
            for ii, es in enumerate(effect_size):
                data, es = es
                power = self.power(es, nobs, alpha, **kwds)
                ax.plot(nobs, power, lw=1.5, color=colors[ii], label=data + " (" + r"$d = {}$".format('%4.2F' % es) + ")")
                xlabel = 'Stichprobengröße'
                ylabel = 'Trennschärfe'
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        return fig