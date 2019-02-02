import numpy as np
import matplotlib.pyplot as plt
import scipy
import pandas as pd
from statsmodels.stats.power import TTestIndPower
import warnings
warnings.filterwarnings("ignore")


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
        plt.tight_layout()
        return fig


def normal_distribution(collections, columns, alpha=0.05):
    results = dict()
    for column, data in zip(columns, collections):
        spreadshirt = data[data["website"] == "spreadshirt"][column]
        shirtinator = data[data["website"] == "shirtinator"][column]
        
        # Spreadshirt data
        stat, p = scipy.stats.shapiro(spreadshirt)
        gaussian = True if p > alpha else False

        results[f"{data.name}-spreadshirt-{column}"] = {"stat": round(stat, 3),
                                                        "p": round(p, 3),
                                                        "gaussian": gaussian}
        
        # Shirtinator data
        stat, p = scipy.stats.shapiro(shirtinator)
        gaussian = True if p > alpha else False

        results[f"{data.name}-shirtinator-{column}"] = {"stat": round(stat, 3),
                                                        "p": round(p, 3),
                                                        "gaussian": gaussian}
    return pd.DataFrame(results).T


def variance_homogeneity(collections, columns, alpha=0.05):
    results = dict()
    for column, data in zip(columns, collections):
        spreadshirt = data[data["website"] == "spreadshirt"][column]
        shirtinator = data[data["website"] == "shirtinator"][column]
        
        stat, p = scipy.stats.levene(spreadshirt, shirtinator)
        homogeneous = True if p > alpha else False

        results[f"{data.name}-{column}"] = {"stat": round(stat, 3),
                                            "p": round(p, 3),
                                            "homogeneous": homogeneous}
    return pd.DataFrame(results).T


def t_test(x, y, alpha):
    stat, p = scipy.stats.ttest_rel(x, y)
    equal = True if p > alpha else False
    return pd.DataFrame({"stat": round(stat, 3),
                         "p": round(p, 3),
                         "alpha": alpha,
                         "equal": equal}, index=[0])


def wilcoxon(x, y, alpha):
    stat, p = scipy.stats.wilcoxon(x, y)
    equal = True if p > alpha else False
    return pd.DataFrame({"stat": round(stat, 3),
                         "p": round(p, 3),
                         "alpha": alpha,
                         "equal": equal}, index=[0])
