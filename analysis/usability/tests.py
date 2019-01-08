import numpy as np
import matplotlib.pyplot as plt
import scipy
from statsmodels.stats.power import TTestIndPower


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
    return results


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
    return results


def t_test(x, y, alpha):
    stat, p = scipy.stats.ttest_rel(x, y)
    equal = True if p > alpha else False
    return {"stat": round(stat, 3),
            "p": round(p, 3),
            "equal": equal}


def mann_whitney_u(x, y, alpha):
    stat, p = scipy.stats.mannwhitneyu(x, y)
    equal = True if p > alpha else False
    return {"stat": round(stat, 3),
            "p": round(p, 3),
            "equal": equal}


def tost(x, y, lower, upper, alpha):
    t1, pv1 = scipy.stats.ttest_1samp(x - y, lower)
    t2, pv2 = scipy.stats.ttest_1samp(x - y, upper)
    equivalent = True if max(pv1, pv2) < alpha else False
    return {"upper": {"t": round(t1, 3), "p": pv1},
            "lower": {"t": round(t2, 3), "p": pv2},
            "equivalent": equivalent}
