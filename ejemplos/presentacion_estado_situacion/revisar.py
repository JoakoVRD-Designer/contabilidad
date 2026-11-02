#!/usr/bin/env python3
"""Revisión estricta del .pptx animado: ids únicos, cada animación apunta a un objeto que existe,
ids de la línea de tiempo únicos, bldP solo para formas, sonido presente y con su relación,
notas del orador presentes y que python-pptx lo abra."""
import re, sys, zipfile
from lxml import etree

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
ruta = sys.argv[1]
z = zipfile.ZipFile(ruta)
nombres = set(z.namelist())
ct = z.read("[Content_Types].xml").decode()
assert 'Extension="wav"' in ct, "falta el tipo de contenido wav"
errores = []
for n in range(1, 8):
    raiz = etree.fromstring(z.read(f"ppt/slides/slide{n}.xml"))
    ids = [int(c.get("id")) for c in raiz.iter("{%s}cNvPr" % NS["p"])]
    if len(ids) != len(set(ids)):
        errores.append(f"{n}: ids de objetos repetidos")
    arbol = raiz.find("p:cSld/p:spTree", NS)
    tipo_por_id = {int(el.find(".//p:cNvPr", NS).get("id")): etree.QName(el).localname for el in arbol if etree.QName(el).localname in ("sp", "pic", "graphicFrame")}
    spids = [int(t.get("spid")) for t in raiz.iter("{%s}spTgt" % NS["p"])]
    faltan = sorted(set(spids) - set(tipo_por_id))
    if faltan:
        errores.append(f"{n}: animaciones apuntan a ids inexistentes {faltan}")
    ctn = [int(c.get("id")) for c in raiz.iter("{%s}cTn" % NS["p"])]
    if len(ctn) != len(set(ctn)):
        errores.append(f"{n}: ids de cTn repetidos")
    for bp in raiz.iter("{%s}bldP" % NS["p"]):
        if tipo_por_id.get(int(bp.get("spid"))) != "sp":
            errores.append(f"{n}: bldP para un objeto que no es forma ({bp.get('spid')})")
    hijos = [etree.QName(h).localname for h in raiz]
    if hijos != ["cSld", "clrMapOvr", "transition", "timing"]:
        errores.append(f"{n}: orden de elementos {hijos}")
    snd = raiz.find(".//p:transition/p:sndAc/p:stSnd/p:snd", NS)
    rid = snd.get("{%s}embed" % NS["r"])
    rels = etree.fromstring(z.read(f"ppt/slides/_rels/slide{n}.xml.rels"))
    destino = [r.get("Target") for r in rels if r.get("Id") == rid]
    if len(destino) != 1 or "ppt/media/" + destino[0].split("/")[-1] not in nombres:
        errores.append(f"{n}: sonido sin archivo")
    efectos = [c for c in raiz.iter("{%s}cTn" % NS["p"]) if c.get("presetClass") == "entr"]
    animados = len(set(spids))
    notas = [r for r in rels if r.get("Type").endswith("/notesSlide")]
    texto_notas = "".join(etree.fromstring(z.read("ppt/" + notas[0].get("Target").replace("../", ""))).itertext()) if notas else ""
    print(f"diapositiva {n}: {len(efectos)} efectos sobre {animados} objetos · sonido {destino[0].split('/')[-1]} · notas {len(texto_notas.split())} palabras")
from pptx import Presentation
prs = Presentation(ruta)
print("python-pptx abre el archivo:", len(prs.slides), "diapositivas")
print("ERRORES:" if errores else "Sin errores.", *errores, sep="\n")
sys.exit(1 if errores else 0)
