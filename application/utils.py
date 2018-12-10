from pathlib import Path
import json
import sys

import flask

QUESI = [{"question": "Es gelang mir, das System ohne Nachdenken zu benutzen.", "name": "item1"},
         {"question": "Ich habe erreicht, was ich mit dem System erreichen wollte.", "name": "item2"},
         {"question": "Mir war sofort klar, wie das System funktioniert.", "name": "item3"},
         {"question": "Der Umgang mit dem System erschien mir vertraut.", "name": "item4"},
         {"question": "Bei der Benutzung des Systems sind keine Probleme aufgetreten.", "name": "item5"},
         {"question": "Die Systembenutzung war unkompliziert.", "name": "item6"},
         {"question": "Es gelang mir, meine Ziele so zu erreichen, wie ich es mir vorgestellt habe.", "name": "item7"},
         {"question": "Es fiel mir von Anfang an leicht, das System zu benutzen.", "name": "item8"},
         {"question": "Mir war immer klar, was ich tun musste, um das System zu benutzen.", "name": "item9"},
         {"question": "Die Benutzung des Systems verlief reibungslos.", "name": "item10"},
         {"question": "Ich musste mich kaum auf die Benutzung des Systems konzentrieren.", "name": "item11"},
         {"question": "Das System hat mich dabei unterstützt, meine Ziele vollständig zu erreichen.", "name": "item12"},
         {"question": "Die Benutzung des Systems war mir auf Anhieb klar.", "name": "item13"},
         {"question": "Ich tat immer automatisch das Richtige, um mein Ziel zu erreichen.", "name": "item14"}]

NASA = [{"title": "Geistige Anforderungen",
         "question": """Wie viel geistige Anstrengung war bei der 
                        Informationsaufnahme und -verarbeitung erforderlich (z.B. Denken, Entscheiden, 
                        Rechnen, Erinnern, Hinsehen, Suchen...)? War die Aufgabe leicht oder 
                        anspruchsvoll, einfach oder komplex, erforderte sie hohe Genauigkeit oder war 
                        sie fehlertolerant?""",
         "name": "item1",
         "left": "gering",
         "right": "hoch"},
        {"title": "Körperliche Anforderungen",
         "question": """Wie viel körperliche Aktivität war erforderlich 
                        (z.B. Ziehen, Drücken, Drehen, Steuern, Aktivieren,...)? War die Aufgabe leicht 
                        oder schwer, einfach oder anstrengend, erholsam oder mühselig?""",
         "name": "item2",
         "left": "gering",
         "right": "hoch"},
         {"title": "Zeitliche Anforderungen",
         "question": """Wie viel Zeitdruck empfanden Sie hinsichtlich der 
                        Häufigkeit oder dem Takt, mit dem Aufgaben oder Aufgabenelemente auftraten? War 
                        die Abfolge langsam und geruhsam oder schnell und hektisch?""",
         "name": "item3",
         "left": "gering",
         "right": "hoch"},
         {"title": "Leistung",
         "question": """Wie erfolgreich haben Sie Ihrer Meinung nach die 
                        vom Versuchsleiter (oder Ihnen selbst) gesetzten Ziele erreicht? Wie zufrieden 
                        waren Sie mit Ihrer Leistung bei der Verfolgung dieser Ziele?""",
         "name": "item4",
         "left": "gut",
         "right": "schlecht"},
         {"title": "Anstrengung",
         "question": """Wie hart mussten sie arbeiten, um Ihren Grad an 
                        Aufgabenerfüllung zu erreichen?""",
         "name": "item5",
         "left": "gering",
         "right": "hoch"},
         {"title": "Frustration",
         "question": """Wie unsicher, entmutigt, irritiert, gestresst und 
                        verärgert (versus sicher, bestätigt, zufrieden, entspannt und zufrieden mit 
                        sich selbst) fühlten Sie sich während der Aufgabe?""",
         "name": "item6",
         "left": "gering",
         "right": "hoch"}]


def init_app(name):
    if getattr(sys, "frozen", False):
        resources_root = Path(sys._MEIPASS)
    else:
        resources_root = Path("application")
    return flask.Flask(name,
                       template_folder=Path(resources_root, "templates"),
                       static_folder=Path(resources_root, "static"))


def dump(path, data):
    with path.open("w", encoding="utf-8") as textfile:
        print(f"Dumped data to '{path}'.")
        textfile.write(json.dumps(data, ensure_ascii=False, indent=4))
