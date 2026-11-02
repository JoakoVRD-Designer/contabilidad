#!/usr/bin/env python3
"""Agrega a la presentación: transición «Desvanecer» con sonido en cada diapositiva y una sola secuencia
de entrada por diapositiva (todo automático: un clic = una diapositiva).

Uso: animar.py base.pptx anim.json salida.pptx

- Renumera los id de los objetos de cada diapositiva (pptxgenjs repite ids en tablas) para que cada
  animación apunte a un objeto único.
- Efectos de entrada nativos de PowerPoint: Desvanecer (10), Flotar hacia dentro (42), Barrido desde la
  izquierda (22/8) y Zoom (53/16), con "Con la anterior" + retraso, en orden de lectura.
- Sonidos propios (sintetizados): entrada.wav (portada), pasar.wav (cambio), logro.wav (estado armado).
"""
import json, os, re, sys, zipfile
from lxml import etree

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"p": P, "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
REL_AUDIO = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio"
DIR = os.path.dirname(os.path.abspath(__file__))

SONIDOS = {1: "entrada.wav", 2: "pasar.wav", 3: "pasar.wav", 4: "pasar.wav", 5: "logro.wav", 6: "pasar.wav", 7: "pasar.wav"}
PRESET = {"fade": (10, 0), "sube": (42, 0), "barre": (22, 8), "zoom": (53, 16)}
DUR = {"fade": 500, "sube": 600, "barre": 600, "zoom": 500}


class Ids:
    def __init__(self, inicio):
        self.n = inicio - 1

    def __call__(self):
        self.n += 1
        return self.n


def tgt(spid):
    return f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'


def set_visible(ids, spid):
    return (f'<p:set><p:cBhvr><p:cTn id="{ids()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'{tgt(spid)}<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
            f'<p:to><p:strVal val="visible"/></p:to></p:set>')


def anim_effect(ids, spid, dur, filtro):
    return f'<p:animEffect transition="in" filter="{filtro}"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}"/>{tgt(spid)}</p:cBhvr></p:animEffect>'


def anim_num(ids, spid, dur, attr, desde, hasta):
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}" decel="100000" fill="hold"/>{tgt(spid)}'
            f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr>'
            f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="{desde}"/></p:val></p:tav>'
            f'<p:tav tm="100000"><p:val><p:strVal val="{hasta}"/></p:val></p:tav></p:tavLst></p:anim>')


def efecto(ids, spid, ef, retraso, tipo_nodo, con_grupo):
    cid = ids()
    pid, sub = PRESET[ef]
    dur = DUR[ef]
    cuerpo = set_visible(ids, spid)
    if ef == "fade":
        cuerpo += anim_effect(ids, spid, dur, "fade")
    elif ef == "sube":
        cuerpo += anim_effect(ids, spid, dur, "fade") + anim_num(ids, spid, dur, "ppt_y", "#ppt_y+.035", "#ppt_y")
    elif ef == "barre":
        cuerpo += anim_effect(ids, spid, dur, "wipe(left)")
    elif ef == "zoom":
        cuerpo += (anim_num(ids, spid, dur, "ppt_w", "#ppt_w*0.70", "#ppt_w") + anim_num(ids, spid, dur, "ppt_h", "#ppt_h*0.70", "#ppt_h")
                   + anim_effect(ids, spid, dur, "fade"))
    else:
        raise ValueError(ef)
    grp = ' grpId="0"' if con_grupo else ""
    return (f'<p:par><p:cTn id="{cid}" presetID="{pid}" presetClass="entr" presetSubtype="{sub}" fill="hold"{grp} nodeType="{tipo_nodo}">'
            f'<p:stCondLst><p:cond delay="{retraso}"/></p:stCondLst><p:childTnLst>{cuerpo}</p:childTnLst></p:cTn></p:par>')


def timing(efectos, bld):
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
            '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + efectos +
            '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
            '</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
            '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>'
            + (f"<p:bldLst>{bld}</p:bldLst>" if bld else "") + "</p:timing>")


def renumerar(xml):
    cont = [0]

    def rep(_m):
        cont[0] += 1
        return f'<p:cNvPr id="{cont[0]}"'
    return re.sub(r'<p:cNvPr id="\d+"', rep, xml)


def objetos(xml):
    """nombre -> lista de (id, tipo, es_cuadro_texto, tipo_ph)"""
    raiz = etree.fromstring(xml.encode("utf-8"))
    arbol = raiz.find("p:cSld/p:spTree", NS)
    res = {}
    for el in arbol:
        tipo = etree.QName(el).localname
        if tipo not in ("sp", "pic", "graphicFrame"):
            continue
        c = el.find(".//p:cNvPr", NS)
        ph = el.find(".//p:nvPr/p:ph", NS)
        csp = el.find(".//p:cNvSpPr", NS)
        info = (int(c.get("id")), tipo, csp is not None and csp.get("txBox") == "1", ph.get("type") if ph is not None else None)
        res.setdefault(c.get("name"), []).append(info)
        if ph is not None:
            res.setdefault("@ph:" + (ph.get("type") or "body"), []).append(info)
    return res


def procesar_diapositiva(n, xml, lista, rid_sonido):
    xml = renumerar(xml)
    ids_vistos = re.findall(r'<p:cNvPr id="(\d+)"', xml)
    assert len(ids_vistos) == len(set(ids_vistos)), f"ids repetidos en la diapositiva {n}"
    mapa = objetos(xml)
    ids = Ids(5)
    efectos, bld, usados = [], [], set()
    orden = sorted(enumerate(lista), key=lambda e: (e[1]["t"], e[0]))
    for k, (_, item) in enumerate(orden):
        encontrados = mapa.get(item["name"], [])
        if len(encontrados) != 1:
            raise SystemExit(f"Diapositiva {n}: «{item['name']}» aparece {len(encontrados)} veces")
        spid, tipo, es_txbox, ph = encontrados[0]
        assert spid not in usados, f"objeto animado dos veces: {item['name']}"
        usados.add(spid)
        con_grupo = tipo == "sp"
        efectos.append(efecto(ids, spid, item["ef"], int(item["t"]), "afterEffect" if k == 0 else "withEffect", con_grupo))
        if con_grupo:
            bld.append(f'<p:bldP spid="{spid}" grpId="0"' + ("" if (es_txbox or ph) else ' animBg="1"') + "/>")
    trans = (f'<p:transition spd="med"><p:fade/><p:sndAc><p:stSnd><p:snd r:embed="{rid_sonido}" name="{SONIDOS[n]}"/></p:stSnd></p:sndAc></p:transition>')
    marca = "</p:clrMapOvr>"
    assert xml.count(marca) == 1 and "<p:timing>" not in xml and "<p:transition" not in xml
    xml = xml.replace(marca, marca + trans + timing("".join(efectos), "".join(bld)))
    etree.fromstring(xml.encode("utf-8"))  # bien formado
    return xml, len(efectos), max(int(i["t"]) + DUR[i["ef"]] for i in lista)


def main(base, manifiesto, salida):
    anim = {int(k): v for k, v in json.load(open(manifiesto, encoding="utf-8")).items()}
    zin = zipfile.ZipFile(base)
    nombres = zin.namelist()
    datos = {nm: zin.read(nm) for nm in nombres}
    resumen = []
    for n, lista in sorted(anim.items()):
        ruta = f"ppt/slides/slide{n}.xml"
        rels = f"ppt/slides/_rels/slide{n}.xml.rels"
        rtexto = datos[rels].decode("utf-8")
        rid = "rIdSonido1"
        assert f'Id="{rid}"' not in rtexto
        # un archivo por diapositiva: LibreOffice pierde el sonido si varias diapositivas comparten el mismo
        archivo = f"sonido-{n}-{SONIDOS[n]}"
        rtexto = rtexto.replace("</Relationships>", f'<Relationship Id="{rid}" Type="{REL_AUDIO}" Target="../media/{archivo}"/></Relationships>')
        destino = f"ppt/media/{archivo}"
        assert destino not in datos
        datos[destino] = open(os.path.join(DIR, SONIDOS[n]), "rb").read()
        nombres.append(destino)
        datos[rels] = rtexto.encode("utf-8")
        xml, cuantos, fin = procesar_diapositiva(n, datos[ruta].decode("utf-8"), lista, rid)
        datos[ruta] = xml.encode("utf-8")
        resumen.append(f"{n}: {cuantos} efectos, se arma en {fin / 1000:.1f} s, sonido {SONIDOS[n]}")
    ct =datos["[Content_Types].xml"].decode("utf-8")
    if 'Extension="wav"' not in ct:
        ct = re.sub(r"(<Types [^>]*>)", r'\1<Default Extension="wav" ContentType="audio/wav"/>', ct, count=1)
    datos["[Content_Types].xml"] = ct.encode("utf-8")
    orden = ["[Content_Types].xml"] + [x for x in nombres if x != "[Content_Types].xml"]
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in orden:
            z.writestr(nm, datos[nm])
    print("\n".join(resumen))
    print("Listo:", salida)


if __name__ == "__main__":
    main(*sys.argv[1:4])
