import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_severity(data):
    # absolute
    plt.figure()
    a = data.plot.barh(figsize=(7.7, 2.4),
                       width=.95,
                       color=("#BABDB6", "#8AE234", "#FCE94F", "#F57900", "#EF2929"))
    a.set_xlabel("Absolute Häufigkeit")
    a.set_ylabel("Website")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title="Schweregrad")
    plt.tight_layout()
    plt.show()
    
    # rel
    plt.figure()
    r = data.div(data.sum(axis=1), axis=0).plot.barh(stacked=True,
                                                     figsize=(7.7, 1.9),
                                                     width=.4,
                                                     color=("#BABDB6", "#8AE234", "#FCE94F", "#F57900", "#EF2929"))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=None, borderaxespad=0., title="Schweregrad")
    r.set_xlabel("Relative Häufigkeit")
    r.set_ylabel("Website")
    plt.tight_layout()
    plt.show()


def plot_problems(data):
    ax = data.plot.box(vert=False,
                       figsize=(6, 2.5),
                       widths=[.45, .45],
                       color={"whiskers": "black", "boxes": "black", 'medians': '#D62728'}, 
                       medianprops={'linewidth': 2.8})
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Website")
    plt.tight_layout()
    plt.show()
    

def plot_concordance(data):
    data["Sum"] = data.sum(axis=1)
    data = data.sort_values("Sum")
    data = pd.DataFrame([data["Irrelevant"],
                         data["Irrelevant_S"],
                         data["Kosmetisch"], 
                         data["Kosmetisch_S"],
                         data["Gering"],
                         data["Gering_S"],
                         data["Bedeutend"],
                         data["Bedeutend_S"],
                         data["Katastrophe"],
                         data["Katastrophe_S"]]).T
    color = ("#3465A4","#3465A4",
             "#BABDB6","#8AE234",
             "#888A85","#FCE94F",
             "#4E4E4E","#F57900",
             "#000000", "#EF2929")
    # absolute
    a = data.plot.barh(stacked=True, color=color, figsize=(7.7, 3.5))
    plt.legend(bbox_to_anchor=(1.05, 1),
               loc=None,
               borderaxespad=0.,
               title="Sym. Differenz:\nSchweregrad")
    a.set_xlabel("Absolute Häufigkeit")
    plt.tight_layout()
    plt.show()
    
    # relative
    r = data.div(data.sum(axis=1), axis=0).plot.barh(stacked=True, color=color, figsize=(7.7, 3.5))
    plt.legend(bbox_to_anchor=(1.05, 1),
               loc=None,
               borderaxespad=0.,
               title="Schweregrad")

    r.set_xlabel("Relative Häufigkeit")
    plt.tight_layout()
    plt.show()
    

def plot_experience(sample):
    ax = sample.pre["vorkenntnisse"].replace("n. a.", "Keine Angabe").replace("spreadshirt.de", "Spreadshirt").replace("nein", "Keine").value_counts().sort_values().plot.barh(color="#555753", figsize=(6, 2.3))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Vorkenntnisse")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    

def plot_gender(sample):
    ax = sample.pre["geschlecht"].apply(lambda x: x.title()).value_counts().sort_values().plot.barh(color="#555753", figsize=(6, 2))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Geschlecht")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    

def plot_education(sample):
    ax = sample.pre["bildungsabschluss"].value_counts().sort_values().plot.barh(color="#555753", figsize=(7.7, 2.3))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Höchster\nBildungsabschluss")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    
def plot_occupation(sample):
    occupation = sample.pre["beschäftigung"].replace("MCS", "Student (Mensch-Computer-Systeme)")
    occupation = occupation.replace("Mensch-Computer-Systeme", "Student (Mensch-Computer-Systeme)")
    occupation = occupation.replace("Mensch-Computer-Systeme (Student)", "Student (Mensch-Computer-Systeme)")
    occupation = occupation.replace("Chemie Bachelor", "Student (Chemie)")
    occupation = occupation.replace("digital humanities", "Student (Digital Humanities)")
    occupation = occupation.replace("Physik", "Student (Physik)")
    occupation = occupation.replace("digital humanities", "Student (Digital Humanities)")
    occupation = occupation.replace("Mensch-Computer-Systeme Student", "Student (Mensch-Computer-Systeme)")
    occupation = occupation.replace("digital humanities".title(), "Student (Digital Humanities)")
    occupation = occupation.replace("Student MCS", "Student (Mensch-Computer-Systeme)")
    ax = occupation.value_counts().sort_values().plot.barh(color="#555753", figsize=(7.7, 3.5))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Beschäftigung")
    plt.tight_layout()
    plt.show()
    
    
def plot_age(sample):
    age = sample.pre["alter"].apply(lambda x: int(x))
    age.name = "Alter"
    ax = age.plot.box(vert=False,
                      figsize=(6, 2),
                      widths=.45,
                      color={"whiskers": "black", "boxes": "black", 'medians': '#D62728'}, 
                      medianprops={'linewidth': 2.8})
    ax.set_xlabel("Alter, in Jahren")
    ax.set_yticklabels("")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    
def plot_nasa_tlx(sample):
    df = pd.DataFrame(columns=["Shirtinator", "Spreadshirt"])
    df.loc[:, "Spreadshirt"] = sample.nasa[sample.nasa["website"] == "spreadshirt"]["score"].values
    df.loc[:, "Shirtinator"] = sample.nasa[sample.nasa["website"] == "shirtinator"]["score"].values
    ax = df.plot.box(vert=False, 
                     figsize=(6, 2.5),
                     widths=[.45, .45],
                     color={"whiskers": "black", "boxes": "black", 'medians': '#D62728'}, 
                     medianprops={'linewidth': 2.8})
    ax.set_xlabel("NASA-TLX Score")
    plt.tight_layout()
    plt.show()
    
    
def plot_quesi(sample):
    df = pd.DataFrame(columns=["Shirtinator", "Spreadshirt"])
    df.loc[:, "Spreadshirt"] = sample.quesi[sample.quesi["website"] == "spreadshirt"]["score"].values
    df.loc[:, "Shirtinator"] = sample.quesi[sample.quesi["website"] == "shirtinator"]["score"].values

    ax = df.plot.box(vert=False,
                     figsize=(6, 2.5),
                     widths=[.45, .45],
                     color={"whiskers": "black", "boxes": "black", 'medians': '#D62728'}, 
                     medianprops={'linewidth': 2.8})
    ax.set_xlabel("QUESI Score")
    plt.tight_layout()
    plt.show()
    
    
def plot_feedback(sample):
    df = pd.DataFrame(columns=["Shirtinator", "Spreadshirt"])
    df.loc[:, "Spreadshirt"] = sample.quesi[sample.quesi["website"] == "spreadshirt"]["score"].values
    df.loc[:, "Shirtinator"] = sample.quesi[sample.quesi["website"] == "shirtinator"]["score"].values

    ax = df.plot.box(vert=False,
                     figsize=(6, 2.5),
                     widths=[.45, .45],
                     color={"whiskers": "black", "boxes": "black", 'medians': '#D62728'}, 
                     medianprops={'linewidth': 2.8})
    ax.set_xlabel("positiv : negativ")
    plt.tight_layout()
    plt.show()
    
    
def plot_clicks(sample):
    df = pd.DataFrame(columns=["Shirtinator", "Spreadshirt"])
    df.loc[:, "Spreadshirt"] = sample.mouse[sample.mouse["website"] == "spreadshirt"]["clicks"].values
    df.loc[:, "Shirtinator"] = sample.mouse[sample.mouse["website"] == "shirtinator"]["clicks"].values

    ax = df.plot.box(vert=False,
                     figsize=(6, 2.5),
                     widths=[.45, .45],
                     color={"whiskers": "black", "boxes": "black", 'medians': '#D62728'}, 
                     medianprops={'linewidth': 2.8})
    ax.set_xlabel("Absolute Häufigkiet")
    plt.tight_layout()
    plt.show()
    
    
def plot_choice(sample):
    choice = sample.post.besser.value_counts()
    choice.index = ["Shirtinator besser", "Spreadshirt besser", "Beide gleich gut"]

    ax = choice.sort_values().plot.barh(color="#555753", figsize=(7.7, 2.3))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Bewertung")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    
def plot_assistance(sample):
    df = pd.DataFrame(columns=["Shirtinator", "Spreadshirt"])
    df.loc[:, "Spreadshirt"] = sample.assistance[sample.assistance["website"] == "spreadshirt"]["n"].values
    df.loc[:, "Shirtinator"] = sample.assistance[sample.assistance["website"] == "shirtinator"]["n"].values
    assistance = pd.DataFrame({"Shirtinator": df["Shirtinator"].value_counts(),
                               "Spreadshirt": df["Spreadshirt"].value_counts()})
    ax = assistance.plot.barh(figsize=(7.7, 2.4), color=("#D3D7CF", "grey"))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Anzahl Hilfestellungen")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title="Website")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    
def plot_mistakes(sample):
    df = pd.DataFrame(columns=["Shirtinator", "Spreadshirt"])
    df.loc[:, "Spreadshirt"] = sample.mistakes[sample.mistakes["website"] == "spreadshirt"]["n"].values
    df.loc[:, "Shirtinator"] = sample.mistakes[sample.mistakes["website"] == "shirtinator"]["n"].values
    mistakes = pd.DataFrame({"Shirtinator": df["Shirtinator"].value_counts(),
                             "Spreadshirt": df["Spreadshirt"].value_counts()})
    ax = mistakes.plot.barh(figsize=(7.7, 2.4), color=("#D3D7CF", "grey"))
    ax.set_xlabel("Absolute Häufigkeit")
    ax.set_ylabel("Anzahl Fehler")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title="Website")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()