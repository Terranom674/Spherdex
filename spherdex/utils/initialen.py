@staticmethod
def get_initialen(vorname, nachname):
    kuerzel_liste = []
    #entfernen aller Sonderzeichen
    name = vorname + " " + nachname
    name = name.replace("-", " ")
    name = name.replace("'", "")
    name = name.replace("`", "")
    name = name.replace("´", "")
    name = name.upper()
    namen_liste = name.split()
    
    # Kürzel wird erstellt
    for i in range(0,len(namen_liste)):
      kuerzel_liste.append((namen_liste[i])[0])
      initialen = "".join(kuerzel_liste)
    return initialen