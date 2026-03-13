################################################################################
################################################################################

### Overordnet sett gjøres følgende operasjoner i dette scriptet:

# Vask og forberedelse av datasettet for artsobservasjoner - Punkter 
# Vask og forberedelse av datasettet for artsobservasjoner - Flater
# Sammenslåing av kartlagene ovenfor til verdikategoriserte kartlag
# Oppdeling av naturtyper til 6 verdikategorier
# Sammenslåing av verdikategoriserte naturtyper og arter til 6 kartlag 

#==============================================================================#

### Metode og preferanser for arealregnskap for naturmangfold:

# I dette scriptet gjøres det valg som medfører at flere registrerte naturverdier
# fjernes og ikke blir representert i det endelige produktet. Dette kan ha 
# negative konsekvenser for naturmangfoldet, og valgene gjort beskrives derfor
# nedenfor. Fjerning av data er nødvendig for å tilpasse dataene et arealregnskap,
# slik at arealregnskapet får høy nok presisjon og troverdighet til å være nyttig
# i arealforvaltningen. 

#🟩# Hvorfor kategoriseres ask og alm fra punktlaget kun som potensielle verdier:
# Ask og alm kategoriseres som potensielle verdier, selv om de begge er sterkt truet, 
# fordi det er hovedsakelig de eldre individene som er av forvaltningsinteresse.
# Yngre individer er nokså vanlige, og det er svært mange observasjoner av disse. 
# Siden alder kun oppgis i noen få observasjoner, må alle behandles på denne måten.
# Om ask og alm behandles på lik linje som andre sterkt truede arter, vil dette
# reduserer kvaliteten på arealregnskapet. Ask og alm fra flaterlaget beholdes
# og kategoriseres som svært stor verdi på antagelsen om at større flater 
# består helt eller delvis av eldre indivder. 

#🟩# Hvorfor 25m buffer for arter (punkter):
# Buffer brukes for å gjøre om punkter til flater slik at de får et areal, og for at 
# området rundt observasjonen blir inkludert for å representere artens habitat. Dette
# tar også høyde for eventuell lav geografisk presisjon for observasjonen. 25 meter er 
# valgt basert på tidligere erfaringer, men er noe tilfeldig. 

#🟩# Hvorfor 150m geografisk presisjon for artsobservasjoner (punkter):
# 150m er valgt med utgangspunkt i artsobservasjonene for Ringerike, hvor vi ser at 
# de eller fleste observasjoner har presisjon <150m. 150m er valgt for å beholde så mye
# data som mulig samtidig som vi øker presisjonen til datasettet så mye som mulig. 

#🟩# Hvorfor 5000m geografisk presisjon for artsobservasjoner (flater):
# Det er vanskelig å vurdere geografisk presisjon for flatene til artsobservasjoner.
# Flere flater for artsobs.er svært store og grove, og ødeleggende for arealregnskap.
# 5000m ser vi at rydder godt nok opp i dataene for Ringerike kommune, men må 
# trolig revurderes ved bruk andre steder. 

#🟩# Hvorfor år 1990 som cut-off for artsobservasjoner:
# Artsobservasjoner fra før år 1990 er fjernet for å øke kvaliteten. Gamle observasjoner
# er ofte mindre nøyaktige, og det er mindre sannsynlig at forekomstene fortsatt finnes.
# Rundt 1990 begynt ting å bli digitalisert, og de aller fleste observasjonene er fra
# etter 1990. 

#🟩# Hvorfor NiN-lokaliteter prioriteres og DN13 lokaliteter fjernes hvor disse overlapper:
# NiN etter Miljødirektoratets instruks er en bedre og mer troverdig metodikk enn
# DN13, og NiN-lokalitetene er i de fleste tilfeller nyere. Naturtyper av 
# forvaltningsinteresse registrert etter DN13 skal også ha blitt registrert ved
# senere NiN-kartlegging, og det virker trygt å fjerne DN13 lokaliteter hvor disse
# overlapper med NiN. Overlapp er ikke ønskelig fordi det gir inntrykk av dobbel
# verdi i en arealanalyse, da arealet fra begge lokalitetene vil bli inkludert. 

#🟩# Hvorfor fjernes fugler og pattedyr uten aktivitet = reproduksjon:
# Mange fugleobservasjoner er gjort mens fuglen forflytter seg, og deres verdi 
# kan ikke alltid plasseres geografisk basert på observasjonene. Det er også svært
# mange fugleobservasjoner, og de fleste av artene er rødlistet. I et arealregnskap
# for naturmangfold kan fugleobservasjoner i stor grad redusere presisjonen,
# og redusere synligheten til artene som er sterkt tilknyttet sine arealer.
 # Aktivitet = reproduksjon bidrar til å stedfeste dyrenes verdi. For fugler
# kan denne aktivitet blant annet indikere at observasjonspunktet er en hekkeplass.
# Fugler og pattedyr kan flytte på seg, og blir ikke påvirket av arealbruksendringer 
# på samme måte som karplanter, sopp, lav eller moser. Andre dyr kan også flytte
# på seg, men antall observasjoner av disse er langt færre. Bløtdyr, insekter,
# edderkoppdyr, ambfibier og andre kan også oftere antas å være registrert på 
# steder av betydning for disse artene.

#🟩# Hvorfor bruker vi union-funksjonen på artsobservasjonene:
# I en arealanalyse er det viktig at naturverdiens areal representeres riktig. 
# Union brukes til å slå sammen features av samme art til én feature, slik
# at nærstående punkter for samme art ikke overlapper og gir feilaktig inntrykk
# av at forekomsten dekker et større areal enn den gjør.  

#🟩# Hvorfor verdikategoriseres flere registrerte naturtyper som "potensiell verdi":
# Noen naturtyper hentet fra kartlaget "Naturtyper - Verdsatte" har verdikategori
# "Vurderes per lokalitet/naturtype". Disse blir her kategorisert som potensielt 
# verdifulle fordi de ikke er verdivurdert i det opprinnelige kartlaget, og fordi
# naturtypene ikke lenger er ansett som spesielt verdifulle i Miljødirektoratets
# instruks. Enkelte av disse, slik som leirravine, indikerer mulige verdifulle
# naturområder fremfor å være registringer av konkrete verdier. Naturtyper som
# Rik boreal frisk lauvskog er tatt ut av kartleggingsinstruksen. 


#==============================================================================#
# 🟧 KRAV TIL KARTLAG (LES FØRST)🟧
# Følgende kartlag må lastes ned for ønsket område og
# legges til prosjektet.
#
# a00000009 — Naturtyper_ku_verdi_xxxx_kommune
# a0000000a — artnasjonal_punkt
# a00000009 — artnasjonal_omr

# Scriptet vil forsøke å endre navn på kartlagene for deg. Om dette feiler, endre navn manuelt på kartlag som følger:

# Arter av nasjonal forvaltningsinteresse: Punktlag "a0000000a — artnasjonal_punkt" = "Arter_punkter"
# Arter av nasjonal forvaltningsinteresse: Polygon "a00000009 — artnasjonal_omr" = "Arter_flater"
# Naturtyper - Verdsatte: "a00000009 — Naturtyper_ku_verdi_xxxx_kommune" = "Naturtyper"

# Scriptet funker ikke om navnene på kartlagene ikke er nøyaktig som beskrevet.

#==============================================================================#
# 🟧 FORHÅNDSREGEL - FULLFØR OG LAGRE TIDLIGERE ARBEID FØR SCRIPTET KJØRES 🟧
# Som del av scriptet blir redigering skrudd av for alle kartlag, og de fleste kartlag
# som ligger i minnet blir slettet. Gjør deg ferdig med tidligere arbeid før 
# scriptet kjøres. Lagre tidligere arbeid som du ønsker å beholde. 

################################################################################
################################################################################

# Arealregnskap - behandling av naturdata
# Forutsetter QGIS 3.x med Processing aktivert

import processing

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsFeatureRequest
)

project = QgsProject.instance()

from PyQt5.QtCore import QVariant

################################################################################

### Her endres navnene på kartlagene til de navnene som brukes i scriptet

# Eksakte navn → nytt navn
rename_map = {
    "a0000000a — artnasjonal_punkt": "Arter_punkter",
    "a00000009 — artnasjonal_omr": "Arter_flater"
}

# Prefix-baserte navn
NATUR_PREFIX = "a00000009 — Naturtyper_ku_verdi"

found_layers = {}

# Samle alle lag
for layer in project.mapLayers().values():
    found_layers[layer.name()] = layer


# -----------------------
# Finn prefix-baserte lag
# -----------------------

naturtyper_layer = None

for name, layer in found_layers.items():

    if name.startswith(NATUR_PREFIX):
        naturtyper_layer = layer


# -----------------------
# Feilmeldinger
# -----------------------

if not naturtyper_layer:
    print('Kartlaget for naturtyper ble ikke funnet 😿 Akkurat dette feilmeldingen kan i seg selv være feil. Lav prioritet å fikse.')

missing = False

for old_name in rename_map:
    if old_name not in found_layers:
        missing = True

if missing:
    print('Feil 😿 Sjekk at nødvendige kartlag er lagt til og har korrekt navn.')


# -----------------------
# Endre navn (prefix-lag først)
# -----------------------

if naturtyper_layer:
    old_name = naturtyper_layer.name()
    naturtyper_layer.setName("Naturtyper")
    print(f'Endret: "{old_name}" → "Naturtyper"')

# -----------------------
# Endre eksakte navn
# -----------------------

for old_name, new_name in rename_map.items():

    if old_name in found_layers:
        layer = found_layers[old_name]
        layer.setName(new_name)
        print(f'Endret: "{old_name}" → "{new_name}"')


print("Ferdig med endring av navn 🌳.")


################################################################################

### Her vaskes og forberedes datasettet for artsobservasjoner - Punkter 

# 1: Fjerner flere fugler og pattedyr. Kun de med sikker reproduktiv aktivitet beholdes - kan stedfestes 
# 2: Fjerner fremmede arter
# 3: Fjerner observasjoner fra før år 1990 
# 4: Fjerner artsobservasjoner med nøyaktighet over 150m
# 5: Skiller ut ask og alm til eget kartlag for potensielle verdier
# 6: Deler datasettet til flere datasett basert på verdivurdering, legger på buffer og smelter sammen obs. av samme art (union)

################################################################################


#🟩# 1: Fjerner flere fugler og pattedyr. Kun de med sikker reproduktiv aktivitet beholdes - kan stedfestes


layer = QgsProject.instance().mapLayersByName("Arter_punkter")[0]

layer.startEditing()

# Fjerner pattedyr uten sikker reproduktiv aktivitet 

pattedyrslette = []

for f in layer.getFeatures():

    artsgruppe = f["artsgruppe"]
    aktivitet = f["aktivitet"]

    if artsgruppe == "Pattedyr":

        if not aktivitet:
            pattedyrslette.append(f.id())

        elif aktivitet != "Reproduksjon":
            pattedyrslette.append(f.id())

if pattedyrslette:
    layer.deleteFeatures(pattedyrslette)


# Fjerner fugler uten sikker reproduktiv aktivitet 


fuglerslette = []

for f in layer.getFeatures():

    artsgruppe = f["artsgruppe"]
    aktivitet = f["aktivitet"]

    if artsgruppe == "Fugler":

        if not aktivitet:
            fuglerslette.append(f.id())

        elif aktivitet != "Reproduksjon":
            fuglerslette.append(f.id())

if fuglerslette:
    layer.deleteFeatures(fuglerslette)


#🟩# 2: Fjerner fremmede arter


FA_slettes = ["Fremmedart"]

fyfyslettes = []

for f in layer.getFeatures():
    if f["utvalgskriterier"] in FA_slettes:
        fyfyslettes.append(f.id())

if fyfyslettes:
    layer.deleteFeatures(fyfyslettes)


#🟩# 3: Fjerner observasjoner fra før år 1990


gamleslette = []

for f in layer.getFeatures():
    dato = f["datoFra"]

    if dato is not None:
        try:
            if int(dato) < 19900000:
                gamleslette.append(f.id())
        except (ValueError, TypeError):
            pass  # ignorer hvis ikke tall

if gamleslette:
    layer.deleteFeatures(gamleslette)

if layer.commitChanges():
    print(
        f"Slettingen av følgende er lagret:\n"
        f"{len(fuglerslette)} fugleobservasjoner og {len(pattedyrslette)} pattedyrobservasjoner uten reproduksjon\n"
        f"{len(fyfyslettes)} observasjoner av fremmede arter 🌳\n"
        f"{len(gamleslette)} registreringer fra før 1990"
    )
else:
    print("Å nei 😿 Noe gikk galt ved lagring etter steg 3:", layer.commitErrors())
    

#🟩# 4: Fjerner artsobservasjoner med geografisk nøyaktighet over 150m


## Gjør om "tall" om geografisk presisjon til faktiske tall
# Lager først nytt field: geo_pres


if "geo_pres" not in [f.name() for f in layer.fields()]:
    layer.startEditing()
    layer.addAttribute(QgsField("geo_pres", QVariant.Int))
    layer.commitChanges()


# Fyller nytt field med tall


layer.startEditing()

provider = layer.dataProvider()

# Finn indeks til geo_pres-feltet
idx_geo_pres = layer.fields().indexFromName("geo_pres")

if idx_geo_pres == -1:
    raise Exception("Feltet 'geo_pres' finnes ikke i laget.")


updates = {}
features_slette = []

count = 0


# Les gjennom alle features én gang
for f in layer.getFeatures():

    try:
        verdi = int(f["geografiskPresisjon"])

        # Lagre for batch-oppdatering
        updates[f.id()] = {
            idx_geo_pres: verdi
        }

        count += 1

        # Sjekk sletting samtidig
        if verdi > 150:
            features_slette.append(f.id())

    except (ValueError, TypeError):
        pass


print(f"Gjort om geografisk presisjon til tall for {count} features.")


if updates:
    provider.changeAttributeValues(updates)
    print(f"Oppdatert geo_pres for {len(updates)} features.")


# Slett hvis nødvendig
if features_slette:
    layer.deleteFeatures(features_slette)
    print(f"Merket {len(features_slette)} features for sletting (geo_pres > 150).")
else:
    print("Ingen features med geo_pres > 150.")


if layer.commitChanges():
    print("Endringer lagret.")
else:
    print("Feil: endringer ble ikke lagret.")
    layer.rollBack()


#🟩#5: Skiller ut ask og alm til eget kartlag for potensielle verdier + buffer og union


idx_navn = layer.fields().indexFromName("norskNavn")

if idx_navn == -1:
    raise Exception("Feltet 'norskNavn' finnes ikke i Arter_punkter.")


arter_pot = ["ask", "alm"]


crs = layer.crs().authid()
geom_type = layer.wkbType()

new_layer = QgsVectorLayer(
    f"{QgsWkbTypes.displayString(geom_type)}?crs={crs}",
    "Arter_potverdi",
    "memory"
)

new_provider = new_layer.dataProvider()


new_provider.addAttributes(layer.fields())
new_layer.updateFields()


nye_features = []
slette_ids = []


for f in layer.getFeatures():

    navn = f[idx_navn]

    if navn and navn.lower() in arter_pot:

        # Kopier feature
        new_f = QgsFeature(new_layer.fields())
        new_f.setGeometry(f.geometry())
        new_f.setAttributes(f.attributes())

        nye_features.append(new_f)

        # Merk for sletting
        slette_ids.append(f.id())


print(f"Fant {len(nye_features)} Ask/Alm-features.")


layer.startEditing()


if nye_features:
    new_provider.addFeatures(nye_features)
    new_layer.updateExtents()


# Slett fra original
if slette_ids:
    layer.deleteFeatures(slette_ids)


if layer.commitChanges():
    print("Endringer lagret i Arter_punkter.")
else:
    print("Feil ved lagring – ruller tilbake.")
    layer.rollBack()


# Legg nytt lag i prosjektet
project.addMapLayer(new_layer)

print("Nytt lag 'Arter_potverdi' opprettet.")


# Oppretter buffer med r = 25m og Union obs. av samme art 


layers = project.mapLayersByName("Arter_potverdi")

if not layers:
    raise Exception("Fant ikke laget 'Arter_potverdi'.")

layer = layers[0]


BUFFER_RADIUS = 25
ARTFELT = "norskNavn"


# Finn indeks
idx_art = layer.fields().indexFromName(ARTFELT)

if idx_art == -1:
    raise Exception("Fant ikke feltet 'norskNavn'.")


# Samle geometrier
ask_geoms = []
alm_geoms = []


for f in layer.getFeatures():

    art = f[idx_art]

    if not art:
        continue

    geom = f.geometry().buffer(BUFFER_RADIUS, 12)

    if art.lower() == "ask":
        ask_geoms.append(geom)

    elif art.lower() == "alm":
        alm_geoms.append(geom)


print(f"Ask-punkter: {len(ask_geoms)}")
print(f"Alm-punkter: {len(alm_geoms)}")


# Union-funksjon
def make_union(geoms):

    if not geoms:
        return None

    if len(geoms) == 1:
        return geoms[0]

    return QgsGeometry.unaryUnion(geoms)


ask_union = make_union(ask_geoms)
alm_union = make_union(alm_geoms)


# Opprett nytt polygonlag
crs = layer.crs().authid()

new_layer = QgsVectorLayer(
    f"Polygon?crs={crs}",
    "Arter_potverdi_poly",
    "memory"
)

prov = new_layer.dataProvider()

# Felter
prov.addAttributes([
    layer.fields().field(idx_art)
])

new_layer.updateFields()


# Lag features
features = []


def add_feature(geom, navn):

    if geom is None:
        return

    f = QgsFeature(new_layer.fields())
    f.setGeometry(geom)
    f.setAttribute(ARTFELT, navn)

    features.append(f)


add_feature(ask_union, "Ask")
add_feature(alm_union, "Alm")


# Legg til
if features:
    prov.addFeatures(features)
    new_layer.updateExtents()


# Legg i prosjekt
project.addMapLayer(new_layer)

print("Ferdig: Arter_potverdi_poly opprettet.")


#🟩# 6: Deler datasettet til flere datasett basert på verdivurdering, legger på buffer og smelter sammen obs. av samme art (union)


# Prioriterte og freda arter får sin egen verdikategori som overskriver den gamle: "høyesteVerdi"


layer_name = "Arter_punkter"
field_check = "utvalgskriterier"
field_update = "verdikategori"

new_value = "høyesteVerdi"

# Hent laget
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Start redigering
if not layer.isEditable():
    layer.startEditing()

# Finn feltindekser
idx_check = layer.fields().indexOf(field_check)
idx_update = layer.fields().indexOf(field_update)

if idx_check == -1 or idx_update == -1:
    raise Exception("Fant ikke nødvendige felt")

updates = {}

for feature in layer.getFeatures():

    text = feature[idx_check]

    if text is None:
        continue

    text_lower = text.lower()

    if "fredet" in text_lower or "prioritert" in text_lower:

        updates[feature.id()] = {
            idx_update: new_value
        }

# Utfør batch-oppdatering
layer.dataProvider().changeAttributeValues(updates)

# Lagre endringer
layer.commitChanges()

print(f"Oppdatert {len(updates)} objekter.")


# Deler opp til flere nye punktlag etter verdikategori


try: 
    
    layer.startEditing()

    verdikategorier = ["storVerdi", "noeVerdi", "sværtStorVerdi", "middelsVerdi", "høyesteVerdi"]
    layers_split = {}

    for verdi in verdikategorier:

        expr = f'"verdikategori" = \'{verdi}\''

        request = QgsFeatureRequest().setFilterExpression(expr)


        mem_layer = QgsVectorLayer(
            f"Point?crs={layer.crs().authid()}",
            f"Punkter_{verdi}",
            "memory"
        )

        mem_layer_data = mem_layer.dataProvider()


        # Kopier felter
        mem_layer_data.addAttributes(layer.fields())
        mem_layer.updateFields()


        feats_to_add = []

        for f in layer.getFeatures(request):

            new_feat = QgsFeature()
            new_feat.setGeometry(f.geometry())
            new_feat.setAttributes(f.attributes())

            feats_to_add.append(new_feat)


        mem_layer_data.addFeatures(feats_to_add)

        QgsProject.instance().addMapLayer(mem_layer)

        layers_split[verdi] = mem_layer

        
        
    # Legger på buffer rundt punktene for å få areal - bruker 25m radius 


    buffer_layers = {}

    for verdi, l in layers_split.items():

        buffer_layer = QgsVectorLayer(
            "Polygon?crs=" + l.crs().authid(),
            f"Buffer_{verdi}",
            "memory"
        )

        buffer_layer_data = buffer_layer.dataProvider()


        # KOPIER FELTER FØRST
        buffer_layer_data.addAttributes(l.fields())
        buffer_layer.updateFields()


        feats_to_add = []

        for f in l.getFeatures():

            geom = f.geometry()
            buffer_geom = geom.buffer(25, 20)

            new_feat = QgsFeature()
            new_feat.setGeometry(buffer_geom)
            new_feat.setAttributes(f.attributes())

            feats_to_add.append(new_feat)


        buffer_layer_data.addFeatures(feats_to_add)

        QgsProject.instance().addMapLayer(buffer_layer)

        buffer_layers[verdi] = buffer_layer
        
        
# Om samme art: Slå sammen overlappende polygoner med union


    union_layers = {}

    for verdi, bl in buffer_layers.items():

        grupper = {}   # {vitenskapeligNavn: [geom, geom, ...]}


        # Samle geometrier per vitenskapeligNavn
        for f in bl.getFeatures():

            navn = f["vitenskapeligNavn"]
            geom = f.geometry()

            if not geom or geom.isEmpty():
                continue

            if navn not in grupper:
                grupper[navn] = []

            grupper[navn].append(geom)


        # Opprett ett output-lag per kategori
        out_layer = QgsVectorLayer(
            "Polygon?crs=" + bl.crs().authid(),
            f"Union_{verdi}",
            "memory"
        )

        prov = out_layer.dataProvider()

        # Kopier alle felt
        prov.addAttributes(bl.fields())
        out_layer.updateFields()

        out_layer.startEditing()


        # Union per art innen kategorien
        for navn, geoms in grupper.items():

            union_geom = QgsGeometry.unaryUnion(geoms)

            if not union_geom or union_geom.isEmpty():
                continue

            feat = QgsFeature(out_layer.fields())
            feat.setGeometry(union_geom)

            # Kopier attributter (bruk første feature som mal)
            for f in bl.getFeatures():
                if f["vitenskapeligNavn"] == navn:
                    feat.setAttributes(f.attributes())
                    break

            out_layer.addFeature(feat)


        out_layer.commitChanges()

        QgsProject.instance().addMapLayer(out_layer)

        union_layers[verdi] = out_layer

            
        print("Success! Punktlag for Artsobservasjoner ble oppdelt til fire verdikategoriserte kartlag, buffered med radius på 25m ble lagt til og polygonene er slått sammen med union.")

except Exception as e:
    print("Uff da. Noe gikk galt under kjøringen av oppdeling av punktkartlag, buffer og union")
    print("Feilmelding:", e)
    

################################################################################

### Her vaskes og forberedes datasettet for artsobservasjoner - Flater 

# 1b: Fjerner flere fugler og pattedyr. De med sikker reproduktiv aktivitet beholdes
# 2b: Fjerner IKKE ask og alm. MERKNAD: Gjøres ikke for flater fordi vi antar at flater for ask og alm delvis består av eldre trær som er verdifulle
# 3b: Fjerner fremmede arter
# 4b: Fjerner observasjoner fra før år 1990 
# 5b: Fjerner artsobservasjoner med nøyaktighet over 5000m
# 6b: Deler datasettet til flere datasett basert på verdivurdering
# 7b: Slår sammen begge kartlagene for artsobservasjoner. Features av samme art slås sammen med union

################################################################################


# Hent laget
layer = QgsProject.instance().mapLayersByName("Arter_flater")[0]


#🟩# 1b: Fjerner flere fugler og pattedyr. De med sikker reproduksjon beholdes


# Fjerner pattedyr først


ids_to_delete = []

for f in layer.getFeatures():

    artsgruppe = f["artsgruppe"]
    aktivitet = f["aktivitet"]

    if artsgruppe == "Pattedyr":

        if not aktivitet:
            ids_to_delete.append(f.id())

        elif aktivitet != "Reproduksjon":
            ids_to_delete.append(f.id())

if ids_to_delete:
    layer.startEditing()
    layer.deleteFeatures(ids_to_delete)

    if layer.commitChanges():
        print(f"Slettet {len(ids_to_delete)} pattedyrobservasjoner uten reproduksjon.")
    else:
        print("Noe gikk galt ved lagring.")
else:
    print("Alle pattedyrobservasjoner har reproduksjon – ingenting slettet.")


# Fjerner fugler uten sikker reproduktiv aktivitet 


ids_to_delete = []

for f in layer.getFeatures():

    artsgruppe = f["artsgruppe"]
    aktivitet = f["aktivitet"]

    if artsgruppe == "Fugler":

        if not aktivitet:
            ids_to_delete.append(f.id())

        elif aktivitet != "Reproduksjon":
            ids_to_delete.append(f.id())

if ids_to_delete:
    layer.startEditing()
    layer.deleteFeatures(ids_to_delete)

    if layer.commitChanges():
        print(f"Slettet {len(ids_to_delete)} fugleobservasjoner uten reproduksjon.")
    else:
        print("Noe gikk galt ved lagring.")
else:
    print("Alle fugleobservasjoner har reproduksjon – ingenting slettet.")
    

#🟩# 3b: Fjerner fremmede arter


FA_slettes = ["Fremmedart"]

ids_to_delete = []

for f in layer.getFeatures():
    if f["utvalgskriterier"] in FA_slettes:
        ids_to_delete.append(f.id())

if ids_to_delete:

    layer.startEditing()
    layer.deleteFeatures(ids_to_delete)

    if layer.commitChanges():
        print(f"Slettet {len(ids_to_delete)} features (Fremmedarter).")
    else:
        print("Noe gikk galt ved lagring av sletting av fremmede arter.")

else:
    print("Ingen fremmede arter – ingenting slettet.")


#🟩# 4b: Fjerner observasjoner fra før år 1990


ids_to_delete = []

for f in layer.getFeatures():
    dato = f["datoFra"]

    # Pass på at feltet ikke er tomt og at det er et tall
    if dato is not None:
        try:
            if int(dato) < 19900000:
                ids_to_delete.append(f.id())
        except (ValueError, TypeError):
            pass  # ignorer hvis ikke tall

if ids_to_delete:
    layer.startEditing()
    layer.deleteFeatures(ids_to_delete)

    if layer.commitChanges():
        print(f"Slettet {len(ids_to_delete)} features registeringer fra før 1990.")
    else:
        print("Noe gikk galt ved lagring av sletting av datoFra.")
else:
    print("Ingen features med datoFra < 19900000 – ingenting slettet.")
    

#🟩# 5b: Fjerner artsobservasjoner med nøyaktighet over 5000m


## Gjør om "tall" om geografisk presisjon til faktiske tall
# Lager først nytt field: geo_pres


if "geo_pres" not in [f.name() for f in layer.fields()]:
    layer.startEditing()
    layer.addAttribute(QgsField("geo_pres", QVariant.Int))
    layer.commitChanges()


# Fyller nytt field med tall


layer.startEditing()

provider = layer.dataProvider()

# Finn indeks til geo_pres-feltet
idx_geo_pres = layer.fields().indexFromName("geo_pres")

if idx_geo_pres == -1:
    raise Exception("Feltet 'geo_pres' finnes ikke i laget.")


updates = {}
features_slette = []

count = 0


# Les gjennom alle features én gang
for f in layer.getFeatures():

    try:
        verdi = int(f["geografiskPresisjon"])

        # Lagre for batch-oppdatering
        updates[f.id()] = {
            idx_geo_pres: verdi
        }

        count += 1

        # Sjekk sletting samtidig
        if verdi > 5000:
            features_slette.append(f.id())

    except (ValueError, TypeError):
        pass


print(f"Gjort om geografisk presisjon til tall for {count} features.")


if updates:
    provider.changeAttributeValues(updates)
    print(f"Oppdatert geo_pres for {len(updates)} features.")


# Slett hvis nødvendig
if features_slette:
    layer.deleteFeatures(features_slette)
    print(f"Merket {len(features_slette)} features for sletting (geo_pres > 5000).")
else:
    print("Ingen features med geo_pres > 5000.")


if layer.commitChanges():
    print("Endringer lagret.")
else:
    print("Feil: endringer ble ikke lagret.")
    layer.rollBack()





#🟩# 6b: Deler datasettet til flere datasett basert på verdivurdering


# Prioriterte og freda arter får sin egen verdikategori som overskriver den gamle: "høyesteVerdi"

layer_name = "Arter_flater"
field_check = "utvalgskriterier"
field_update = "verdikategori"

new_value = "høyesteVerdi"

# Hent laget
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Start redigering
if not layer.isEditable():
    layer.startEditing()

# Finn feltindekser
idx_check = layer.fields().indexOf(field_check)
idx_update = layer.fields().indexOf(field_update)

if idx_check == -1 or idx_update == -1:
    raise Exception("Fant ikke nødvendige felt")

updates = {}

for feature in layer.getFeatures():

    text = feature[idx_check]

    if text is None:
        continue

    text_lower = text.lower()

    if "fredet" in text_lower or "prioritert" in text_lower:

        updates[feature.id()] = {
            idx_update: new_value
        }

# Utfør batch-oppdatering
layer.dataProvider().changeAttributeValues(updates)

# Lagre endringer
layer.commitChanges()

print(f"Oppdatert {len(updates)} objekter.")


# Deler opp Arter_flater til flere kartlag basert på verdikategori


try: 

    # Parametre
    lag_navn = "Arter_flater"
    verdikategorier = ["storVerdi", "noeVerdi", "sværtStorVerdi", "middelsVerdi", "høyesteVerdi"]

    layers = QgsProject.instance().mapLayersByName(lag_navn)
    if not layers:
        raise ValueError(f"Lag '{lag_navn}' finnes ikke!")
    layer = layers[0]

    layers_split = {}

    # Split
    for verdi in verdikategorier:
        # Lag filter for verdikategori
        expr = f'"verdikategori" = \'{verdi}\''
        request = QgsFeatureRequest().setFilterExpression(expr)
        
        # Opprett nytt memory-lag for denne verdikategorien
        mem_layer = QgsVectorLayer(f"Polygon?crs={layer.crs().authid()}", f"{verdi}", "memory")
        mem_layer_data = mem_layer.dataProvider()
        
        # Kopier alle feltene fra original-laget
        mem_layer_data.addAttributes(layer.fields())
        mem_layer.updateFields()
        
        # Kopier features som matcher filteret
        feats_to_add = []
        for f in layer.getFeatures(request):
            new_feat = QgsFeature()
            new_feat.setGeometry(f.geometry())
            new_feat.setAttributes(f.attributes())
            feats_to_add.append(new_feat)
        
        mem_layer_data.addFeatures(feats_to_add)
        
        # Legg memory-laget til i kartet
        QgsProject.instance().addMapLayer(mem_layer)
        
        # Legg laget i dictionary for senere bruk
        layers_split[verdi] = mem_layer

        
    print("Success! Flater for Artsobservasjoner ble oppdelt til fire verdikategoriserte kartlag.")

except Exception as e:
    print("Uff da. Noe gikk galt under kjøringen av oppdeling av flaterkartlag for arter.")
    print("Feilmelding:", e)
    
    
#🟩# 7b: Her slås sammen begge kartlagene for artsobservasjoner. Features av SAMME ART slås sammen med union


try:

    verdier = ["middelsVerdi", "sværtStorVerdi", "noeVerdi", "storVerdi", "høyesteVerdi"]

    ART_FELT = "vitenskapeligNavn"


    for verdi in verdier:

        flate_navn = verdi
        buffer_navn = f"Union_{verdi}"
        resultat_navn = f"Samlet_{verdi}"


        flater = project.mapLayersByName(flate_navn)
        buffere = project.mapLayersByName(buffer_navn)

        if not flater or not buffere:
            print(f"Mangler lag for {verdi}, hopper over")
            continue


        flate_layer = flater[0]
        buffer_layer = buffere[0]


        # ---------------------------------------
        # Samle geometri + attributter per art
        # ---------------------------------------

        art_data = {}
        # struktur:
        # art_data[art] = {
        #    "geom": QgsGeometry,
        #    "attrs": [attributter]
        # }


        def legg_til(feature):

            art = feature[ART_FELT]

            if not art:
                return


            geom = feature.geometry()


            if art not in art_data:

                # Lagre første feature som "mal"
                art_data[art] = {
                    "geom": geom,
                    "attrs": feature.attributes()
                }

            else:

                art_data[art]["geom"] = art_data[art]["geom"].combine(geom)



        # Flater
        for f in flate_layer.getFeatures():
            legg_til(f)

        # Buffere
        for f in buffer_layer.getFeatures():
            legg_til(f)


        # ---------------------------------------
        # Opprett resultatlag
        # ---------------------------------------

        mem_layer = QgsVectorLayer(
            f"Polygon?crs={flate_layer.crs().authid()}",
            resultat_navn,
            "memory"
        )

        prov = mem_layer.dataProvider()

        # Kopier felter
        prov.addAttributes(flate_layer.fields())
        mem_layer.updateFields()


        # ---------------------------------------
        # Lag features
        # ---------------------------------------

        new_feats = []

        for art, data in art_data.items():

            feat = QgsFeature(mem_layer.fields())

            feat.setGeometry(data["geom"])

            # Kopier ALLE attributter
            feat.setAttributes(data["attrs"])

            new_feats.append(feat)


        prov.addFeatures(new_feats)

        project.addMapLayer(mem_layer)

        print(f"Sammenslått per art: {resultat_navn}")


    print("Alle verdikategorier ferdig behandlet.")


except Exception as e:

    print("Å nei, sammenslåing feilet")
    print(e)


################################################################################

### Her behandles kartlag for Naturtyper og sammenslåingen av dette med kartlag for arter 
# 1: Identifiserer overlapper mellom DN13 og NiN, og fjerner DN13 lokaliteter som overlapper.
# 2: Oppdeling av naturtyper til egne kartlag for verdikategorier
# 3: Merger verdikategoriserte naturtyper og artsobservasjoner sammen
# 4: Lager eget kartlag for naturtyper med verdikategori = vurderes per lokalitet/naturtype og kaller dette "Potensielle verdier"
# 5: Her slås potensielle naturtyper og artsobservasjoner sammen 

################################################################################
    
#🟩# 1: Identifiserer overlapper mellom DN13 og NiN, og fjerner DN13 lokaliteter som overlapper


# Identifiserer overlapp mellom DN13 og NiN


print("Starter overlapp-analyse for Naturtyper")


# ------------------------------------
# Hent prosjekt og lag
# ------------------------------------

project = QgsProject.instance()

layers = project.mapLayersByName("Naturtyper")

if not layers:
    raise ValueError("Fant ikke laget 'Naturtyper'")

layer = layers[0]


# ------------------------------------
# Definer uttrykk
# ------------------------------------

expr_nin = "\"opphav\" = 'Naturtyper på land (NiN)'"
expr_hb13 = "\"opphav\" = 'Naturtyper på land og i ferskvann (HB13)'"


# ------------------------------------
# Lag NiN
# ------------------------------------

nin = processing.run(
    "native:extractbyexpression",
    {
        "INPUT": layer,
        "EXPRESSION": expr_nin,
        "OUTPUT": "memory:"
    }
)["OUTPUT"]

print("NiN-features:", nin.featureCount())


# ------------------------------------
# Lag HB13
# ------------------------------------

hb13 = processing.run(
    "native:extractbyexpression",
    {
        "INPUT": layer,
        "EXPRESSION": expr_hb13,
        "OUTPUT": "memory:"
    }
)["OUTPUT"]

print("HB13-features:", hb13.featureCount())


# ------------------------------------
# CRS-sjekk
# ------------------------------------

if nin.crs() != hb13.crs():

    print("CRS er forskjellig. Reprojiserer HB13")

    hb13 = processing.run(
        "native:reprojectlayer",
        {
            "INPUT": hb13,
            "TARGET_CRS": nin.crs(),
            "OUTPUT": "memory:"
        }
    )["OUTPUT"]


## Fix + Intersection

print("Beregner overlapp")

context = QgsProcessingContext()
feedback = QgsProcessingFeedback()

# Fix input-geometri

nin_fixed = processing.run(
    "native:fixgeometries",
    {
        "INPUT": nin,
        "OUTPUT": "memory:"
    },
    context=context,
    feedback=feedback
)["OUTPUT"]

hb13_fixed = processing.run(
    "native:fixgeometries",
    {
        "INPUT": hb13,
        "OUTPUT": "memory:"
    },
    context=context,
    feedback=feedback
)["OUTPUT"]

print("NiN (fixed):", nin_fixed.featureCount())
print("HB13 (fixed):", hb13_fixed.featureCount())

# Intersection

result = processing.run(
    "native:intersection",
    {
        "INPUT": nin_fixed,
        "OVERLAY": hb13_fixed,
        "OUTPUT": "memory:"
    },
    context=context,
    feedback=feedback
)

if "OUTPUT" not in result:
    raise Exception("Intersection feilet")

overlap = result["OUTPUT"]

# Fix overlap

overlap = processing.run(
    "native:fixgeometries",
    {
        "INPUT": overlap,
        "OUTPUT": "memory:"
    },
    context=context,
    feedback=feedback
)["OUTPUT"]

overlap.setName("Overlapp NiN og DN13")

QgsProject.instance().addMapLayer(overlap)

print("Antall overlapp:", overlap.featureCount())


# ------------------------------------
# Areal
# ------------------------------------

total_area = 0

for f in overlap.getFeatures():
    total_area += f.geometry().area()

print("Totalt overlappareal (m2):", round(total_area, 1))


# Fjerner deler av DN13 som overlapper med NiN polygoner


try:

    FELT = "opphav"
    VERDI = "Naturtyper på land og i ferskvann (HB13)"


    # -------------------------------
    # Slå sammen overlapp
    # -------------------------------

    overlapp_geom = None

    for f in overlap.getFeatures():

        g = f.geometry()

        if overlapp_geom is None:
            overlapp_geom = g
        else:
            overlapp_geom = overlapp_geom.combine(g)


    if overlapp_geom is None:
        raise Exception("Overlapp-laget er tomt")


    # -------------------------------
    # Start redigering
    # -------------------------------

    if not layer.isEditable():
        layer.startEditing()


    slett_ids = []
    oppdater = {}


    # -------------------------------
    # Klipp HB13
    # -------------------------------

    for f in layer.getFeatures():

        if f[FELT] != VERDI:
            continue

        geom = f.geometry()

        ny_geom = geom.difference(overlapp_geom)

        if not ny_geom or ny_geom.isEmpty():

            slett_ids.append(f.id())

        else:

            oppdater[f.id()] = ny_geom


    # -------------------------------
    # Utfør endringer
    # -------------------------------

    if oppdater:
        layer.dataProvider().changeGeometryValues(oppdater)

    if slett_ids:
        layer.dataProvider().deleteFeatures(slett_ids)


    # -------------------------------
    # Lagre
    # -------------------------------

    if layer.commitChanges():
        print("Endringer lagret i Naturtyper")

    else:
        layer.rollBack()
        raise Exception("Commit feilet")


    print(f"Ferdig. Endret {len(oppdater)} features, slettet {len(slett_ids)}.")


except Exception as e:

    print("Feil:")
    print(e)


# Fixer geometrien på Naturtyper og overskriver gammelt lag 


natur_lag_list = project.mapLayersByName("Naturtyper")
if not natur_lag_list:
    raise ValueError("Fant ikke laget 'Naturtyper'")
natur = natur_lag_list[0]

# Fix geometriene og lag nytt memory-lag
natur_fikset = processing.run(
    "native:fixgeometries",
    {
        "INPUT": natur,
        "OUTPUT": "memory:"
    }
)["OUTPUT"]

# Gi det samme navn som originalen
natur_fikset.setName("Naturtyper")

# Fjern original fra prosjektet
project.removeMapLayer(natur.id())

# Legg til fikset lag i prosjektet
project.addMapLayer(natur_fikset)

print("Geometriene i Naturtyper er fikset og laget er klart til videre behandling")


#🟩# 2: Her gjøres det oppdeling av naturtyper til seks verdikategorier


# Utvalgte naturtyper får sin egen verdikategori som overskriver den gamle: "høyesteVerdi"

layer_name = "Naturtyper"
field_check = "opphav"
field_update = "verdikategori"

new_value = "Høyeste verdi"

# Hent laget
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Start redigering
if not layer.isEditable():
    layer.startEditing()

# Finn feltindekser
idx_check = layer.fields().indexOf(field_check)
idx_update = layer.fields().indexOf(field_update)

if idx_check == -1 or idx_update == -1:
    raise Exception("Fant ikke nødvendige felt")

updates = {}

for feature in layer.getFeatures():

    text = feature[idx_check]

    if text is None:
        continue

    text_lower = text.lower()

    if "utvalgte" in text_lower:

        updates[feature.id()] = {
            idx_update: new_value
        }

# Utfør batch-oppdatering
layer.dataProvider().changeAttributeValues(updates)

# Lagre endringer
layer.commitChanges()

print(f"Oppdatert {len(updates)} objekter.")


# Deler opp naturtyper til kategoriserte kartlag

try: 

    # Parametre
    lag_navn = "Naturtyper"
    verdikategorier = ["Vurderes per lokalitet", "Svært stor verdi", "Stor verdi", "Noe verdi", "Middels verdi", "Høyeste verdi"]


    layers = QgsProject.instance().mapLayersByName(lag_navn)
    if not layers:
        raise ValueError(f"Lag '{lag_navn}' finnes ikke!")
    layer = layers[0]

    layers_split = {}

    # Split
    for verdi in verdikategorier:
        # Lag filter for verdikategori
        expr = f'"verdikategori" = \'{verdi}\''
        request = QgsFeatureRequest().setFilterExpression(expr)
        
        # Opprett nytt memory-lag for denne verdikategorien
        mem_layer = QgsVectorLayer(f"Polygon?crs={layer.crs().authid()}", f"{verdi}", "memory")
        mem_layer_data = mem_layer.dataProvider()
        
        # Kopier alle feltene fra original-laget
        mem_layer_data.addAttributes(layer.fields())
        mem_layer.updateFields()
        
        # Kopier features som matcher filteret
        feats_to_add = []
        for f in layer.getFeatures(request):
            new_feat = QgsFeature()
            new_feat.setGeometry(f.geometry())
            new_feat.setAttributes(f.attributes())
            feats_to_add.append(new_feat)
        
        mem_layer_data.addFeatures(feats_to_add)
        
        # Legg memory-laget til i kartet
        QgsProject.instance().addMapLayer(mem_layer)
        
        # Legg laget i dictionary for senere bruk
        layers_split[verdi] = mem_layer

        
    print("Success! Naturtyper ble oppdelt til fire verdikategoriserte kartlag.")

except Exception as e:
    print("Uff da. Noe gikk galt under kjøringen av oppdeling av naturtyper.")
    print("Feilmelding:", e)
    
    
#🟩# 3: Her slås verdikategoriserte naturtyper og artsobservasjoner sammen 


pairs = [
    ("Høyeste verdi", "Samlet_høyesteVerdi", "Arter og naturtyper av høyeste verdi"),
    ("Svært stor verdi", "Samlet_sværtStorVerdi", "Arter og naturtyper av svært stor verdi"),
    ("Stor verdi", "Samlet_storVerdi", "Arter og naturtyper av stor verdi"),
    ("Middels verdi", "Samlet_middelsVerdi", "Arter og naturtyper av middels verdi"),
    ("Noe verdi", "Samlet_noeVerdi", "Arter og naturtyper av noe verdi"),
]

project = QgsProject.instance()

for layer1_name, layer2_name, out_name in pairs:

    layers1 = project.mapLayersByName(layer1_name)
    layers2 = project.mapLayersByName(layer2_name)

    if not layers1 or not layers2:
        print(f"Mangler lag: {layer1_name} eller {layer2_name}")
        continue

    layer1 = layers1[0]
    layer2 = layers2[0]

    params = {
        "LAYERS": [layer1, layer2],
        "CRS": layer1.crs(),
        "OUTPUT": "memory:"
    }

    result = processing.run("native:mergevectorlayers", params)

    merged_layer = result["OUTPUT"]
    merged_layer.setName(out_name)

    project.addMapLayer(merged_layer)

    print(f"Ferdig: {out_name}")


#🟩# 4: Legger også til kartlaget "Naturtyper av potensiell verdi" fra Naturtyper: Vurderes per lokalitet og Vurderes per naturtype


# Hent original-laget
layers = project.mapLayersByName("Naturtyper")

if not layers:
    print("Fant ikke laget 'Naturtyper'")
else:
    original_lag = layers[0]

    # Finn geometri-type
    geom_type = QgsWkbTypes.displayString(original_lag.wkbType())

    # Opprett nytt memory-lag
    nytt_lag = QgsVectorLayer(
        f"{geom_type}?crs={original_lag.crs().authid()}",
        "Naturtyper av potensiell verdi",
        "memory"
    )

    prov = nytt_lag.dataProvider()

    # Kopier felter
    prov.addAttributes(original_lag.fields())
    nytt_lag.updateFields()

    # Filter for begge verdier
    expr = (
        "\"verdikategori\" = 'Vurderes per lokalitet' OR "
        "\"verdikategori\" = 'Vurderes per naturtype'"
    )

    request = QgsFeatureRequest().setFilterExpression(expr)

    # Kopier features
    feats = []

    for f in original_lag.getFeatures(request):
        new_f = QgsFeature()
        new_f.setGeometry(f.geometry())
        new_f.setAttributes(f.attributes())
        feats.append(new_f)

    prov.addFeatures(feats)
    nytt_lag.updateExtents()

    # Legg til i prosjektet
    project.addMapLayer(nytt_lag)

    print("Nytt lag med begge vurderingskategorier er opprettet.")


# Fixer geometrien på Naturtyper av pot. verdi og overskriver gammelt lag 


natur_lag_list = project.mapLayersByName("Naturtyper av potensiell verdi")
if not natur_lag_list:
    raise ValueError("Fant ikke laget 'Naturtyper av potensiell verdi'")
natur = natur_lag_list[0]

# Fix geometriene og lag nytt memory-lag
natur_fikset = processing.run(
    "native:fixgeometries",
    {
        "INPUT": natur,
        "OUTPUT": "memory:"
    }
)["OUTPUT"]

# Gi det samme navn som originalen
natur_fikset.setName("Naturtyper av potensiell verdi")

# Fjern original fra prosjektet
project.removeMapLayer(natur.id())

# Legg til fikset lag i prosjektet
project.addMapLayer(natur_fikset)

print("Geometriene i Naturtyper av potensiell verdi er fikset og laget er klart til videre behandling")


#🟩# 5: Her slås potensielle naturtyper og artsobservasjoner sammen 


pairs = [
    ("Naturtyper av potensiell verdi", "Arter_potverdi_poly", "Arter og naturtyper av potensiell verdi"),
]

project = QgsProject.instance()

for layer1_name, layer2_name, out_name in pairs:

    layers1 = project.mapLayersByName(layer1_name)
    layers2 = project.mapLayersByName(layer2_name)

    if not layers1 or not layers2:
        print(f"Mangler lag: {layer1_name} eller {layer2_name}")
        continue

    layer1 = layers1[0]
    layer2 = layers2[0]

    params = {
        "LAYERS": [layer1, layer2],
        "CRS": layer1.crs(),
        "OUTPUT": "memory:"
    }

    result = processing.run("native:mergevectorlayers", params)

    merged_layer = result["OUTPUT"]
    merged_layer.setName(out_name)

    project.addMapLayer(merged_layer)

    print(f"Ferdig: {out_name}")


# Fikser farger 

# Definer lag + farge
layer_styles = {
    "Arter og naturtyper av høyeste verdi": "#8B0000",   # Veldig mørkerød
    "Arter og naturtyper av svært stor verdi": "#E32C07",# Mørkerød
    "Arter og naturtyper av stor verdi": "#FFA500",      # Oransje
    "Arter og naturtyper av middels verdi": "#FFD700",  # Gul
    "Arter og naturtyper av noe verdi": "#228B22",       # Grønn
    "Arter og naturtyper av potensiell verdi": "#808080" # Grå
}

for layer_name, color_hex in layer_styles.items():

    layers = project.mapLayersByName(layer_name)

    if not layers:
        print(f"Fant ikke lag: {layer_name}")
        continue

    layer = layers[0]

    # Lag symbol
    symbol = QgsFillSymbol.createSimple({
        "color": color_hex,
        "outline_color": "#000000",
        "outline_width": "0.3"
    })

    # Sett renderer
    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)

    # Oppdater visning
    layer.triggerRepaint()

    print(f"Stil satt: {layer_name}")

# Sletter tidligere midlertidige kartlag fra minnet 

project = QgsProject.instance()

layers_to_keep = [
    "Arter og naturtyper av høyeste verdi",
    "Arter og naturtyper av svært stor verdi",
    "Arter og naturtyper av stor verdi",
    "Arter og naturtyper av middels verdi",
    "Arter og naturtyper av noe verdi",
    "Arter og naturtyper av potensiell verdi"
]

for layer in list(project.mapLayers().values()):

    # Kun memory-lag som IKKE skal beholdes
    if layer.providerType() == "memory" and layer.name() not in layers_to_keep:

        # Hvis laget står i redigering → stopp uten lagring
        if layer.isEditable():
            layer.rollBack()
            print(f"Rullet tilbake endringer: {layer.name()}")

        print(f"Fjerner midlertidig lag: {layer.name()}")
        project.removeMapLayer(layer.id())

print("Opprydding fullført. Kun ønskede verdilag beholdt.")
