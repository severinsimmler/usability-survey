from dataclasses import dataclass
from pathlib import Path
import json

import pandas as pd
import parse
from statsmodels.stats.power import TTestIndPower

from . import tests
from . import utils


@dataclass
class Sample:
    directory: Path
    pattern: str = "{website}-{collection}"

    @property
    def nasa(self):
        scores = list()
        for proband in self.survey_data:
            for survey in proband["answers"]:
                metadata = parse.parse(self.pattern, survey.name)
                if metadata and metadata["collection"] == "nasa":
                    score = survey * 5
                    score = score.sum() / 6
                    scores.append({"pseudonym": proband["pseudonym"],
                                   "score": score,
                                   "website": metadata["website"],
                                   "survey": metadata["collection"]})
        data = pd.DataFrame(scores)
        data.name = "NASA-TLX"
        return data

    @property
    def quesi(self):
        scores = list()
        for proband in self.survey_data:
            for survey in proband["answers"]:
                metadata = parse.parse(self.pattern, survey.name)
                if metadata and metadata["collection"] == "quesi":
                    survey = survey + 1
                    values = list()
                    k = list()
                    z = list()
                    l = list()
                    v = list()
                    fe = list()
                    for item, value in survey.items():
                        if item in utils.K:
                            k.append(value)
                        elif item in utils.Z:
                            z.append(value)
                        elif item in utils.L:
                            l.append(value)
                        elif item in utils.V:
                            v.append(value)
                        elif item in utils.Fe:
                            fe.append(value)
                    values.append(pd.Series(k).median())
                    values.append(pd.Series(z).median())
                    values.append(pd.Series(l).median())
                    values.append(pd.Series(v).median())
                    values.append(pd.Series(fe).median())
                    score = pd.Series(values).mean()
                    scores.append({"pseudonym": proband["pseudonym"],
                                   "score": score,
                                   "website": metadata["website"],
                                   "survey": metadata["collection"]})
        data = pd.DataFrame(scores)
        data.name = "QUESI"
        return data

    @property
    def pre(self):
        answers = list()
        for proband in self.survey_data:
            for survey in proband["answers"]:
                if survey.name == "pre":
                    answers.append({"pseudonym": proband["pseudonym"],
                                    "geschlecht": survey["Geschlecht"],
                                    "alter": survey["Alter"],
                                    "bildungsabschluss": survey["bildungsabschluss"],
                                    "beschäftigung": survey["Derzeitige Beschäftigung bzw. Studienfach"],
                                    "vorkenntnisse": survey["Websites schon einmal benutzt"]})
        data = pd.DataFrame(answers)
        data.name = "Pre-questionnaire"
        return data

    @property
    def post(self):
        answers = list()
        for proband in self.survey_data:
            for survey in proband["answers"]:
                if survey.name == "post":
                    answers.append({"pseudonym": proband["pseudonym"],
                                    "besser": survey["Bessere Website"],
                                    "positiv shirtinator": survey["Positiv bei shirtinator.de"],
                                    "negativ shirtinator": survey["Negativ bei shirtinator.de"],
                                    "positiv spreadshirt": survey["Positiv bei spreadshirt.de"],
                                    "negativ spreadshirt": survey["Negativ bei spreadshirt.de"]})
        data = pd.DataFrame(answers)
        data.name = "Post-questionnaire"
        return data

    @property
    def feedback(self):
        values = list()
        for proband in self.logfile_data:
            for logfile in proband["logs"]:
                metadata = parse.parse(self.pattern, logfile.name)
                if metadata and metadata["collection"] == "feedback":
                    counts = logfile[1].value_counts()
                    values.append({"pseudonym": proband["pseudonym"],
                                   "positiv": counts["pos"] if "pos" in counts.index else 0,
                                   "negativ": counts["neg"] if "neg" in counts.index else 0,
                                   "website": metadata["website"]})
        data = pd.DataFrame(values)
        # add 1 to avoid zero division error
        data["ratio"] = (data["positiv"] + 1) / (data["negativ"] + 1)
        data.name = "Feedback"
        return data

    @property
    def keyboard(self):
        values = list()
        for proband in self.logfile_data:
            for logfile in proband["logs"]:
                metadata = parse.parse(self.pattern, logfile.name)
                if metadata and metadata["collection"] == "keyboard":
                    counts = logfile[0].count()
                    values.append({"pseudonym": proband["pseudonym"],
                                   "tastenanschläge": counts,
                                   "website": metadata["website"]})
        data = pd.DataFrame(values)
        data.name = "Keyboard"
        return data

    @property
    def mouse(self):
        values = list()
        for proband in self.logfile_data:
            for logfile in proband["logs"]:
                metadata = parse.parse(self.pattern, logfile.name)
                if metadata and metadata["collection"] == "mouse":
                    counts = logfile[0].count()
                    values.append({"pseudonym": proband["pseudonym"],
                                   "clicks": counts,
                                   "website": metadata["website"]})
        data = pd.DataFrame(values)
        data.name = "Mouse"
        return data

    @property
    def survey_data(self):
        for proband in self.directory.glob("*"):
            path = Path(proband, "fragebogen-daten")
            answers = utils.process_surveys(path, ".json")
            yield {"pseudonym": proband.name, "answers": list(answers)}

    @property
    def logfile_data(self):
        for proband in self.directory.glob("*"):
            path = Path(proband, "logfile-daten")
            logs = utils.process_logfiles(path, ".log")
            yield {"pseudonym": proband.name, "logs": list(logs)}

    def optimal_size(self, alpha: float = 0.15, power: float = 0.7):
        sizes = list()
        for effect in self.effects:
            name, effect = effect
            analysis = TTestIndPower()
            result = analysis.solve_power(effect,
                                          power=power,
                                          nobs1=None,
                                          ratio=1.0,
                                          alpha=alpha)
            sizes.append(result)
        return {"sizes": sizes,
                "effects": list(self.effects),
                "median size": pd.Series(sizes).median()}
    
    @property
    def effects(self):
        collections = [("NASA-TLX", {"x": self.nasa[self.nasa["website"] == "spreadshirt"]["score"],
                        "y": self.nasa[self.nasa["website"] == "shirtinator"]["score"]}),
                       ("QUESI", {"x": self.quesi[self.quesi["website"] == "spreadshirt"]["score"],
                        "y": self.quesi[self.quesi["website"] == "shirtinator"]["score"]}),
                       ("Positives Feedback", {"x": self.feedback[self.feedback["website"] == "spreadshirt"]["positiv"],
                        "y": self.feedback[self.feedback["website"] == "shirtinator"]["positiv"]}),
                       ("Negatives Feedback", {"x": self.feedback[self.feedback["website"] == "spreadshirt"]["negativ"],
                        "y": self.feedback[self.feedback["website"] == "shirtinator"]["negativ"]}),
                       ("Tastenanschläge", {"x": self.keyboard[self.keyboard["website"] == "spreadshirt"]["tastenanschläge"],
                        "y": self.keyboard[self.keyboard["website"] == "shirtinator"]["tastenanschläge"]}),
                       ("Mausklicks", {"x": self.mouse[self.mouse["website"] == "spreadshirt"]["clicks"],
                        "y": self.mouse[self.mouse["website"] == "shirtinator"]["clicks"]})]
        collections = [("NASA-TLX", {"x": self.nasa[self.nasa["website"] == "spreadshirt"]["score"],
                        "y": self.nasa[self.nasa["website"] == "shirtinator"]["score"]}),
                       ("QUESI", {"x": self.quesi[self.quesi["website"] == "spreadshirt"]["score"],
                        "y": self.quesi[self.quesi["website"] == "shirtinator"]["score"]}),
                       ("Feedback", {"x": self.feedback[self.feedback["website"] == "spreadshirt"]["ratio"],
                        "y": self.feedback[self.feedback["website"] == "shirtinator"]["ratio"]}),
                       ("Tastenanschläge", {"x": self.keyboard[self.keyboard["website"] == "spreadshirt"]["tastenanschläge"],
                        "y": self.keyboard[self.keyboard["website"] == "shirtinator"]["tastenanschläge"]}),
                       ("Mausklicks", {"x": self.mouse[self.mouse["website"] == "spreadshirt"]["clicks"],
                        "y": self.mouse[self.mouse["website"] == "shirtinator"]["clicks"]})]

        
        for collection in collections:
            name, data = collection
            effect = tests.cohen_d(data["x"], data["y"])
            yield name, effect

    def plot_power(self, alpha, sample_sizes, figsize=(8, 4)):
        effect_sizes = list(self.effects)
        analysis = tests.TTestIndPower()
        return analysis.plot_power(nobs=sample_sizes,
                                   alpha=alpha,
                                   effect_size=effect_sizes,
                                   figsize=figsize)
