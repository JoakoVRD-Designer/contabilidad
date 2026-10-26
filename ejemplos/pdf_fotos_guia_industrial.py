"""Une las fotos respondidas de la guía industrial y las hojas de cálculo en un solo PDF.
Uso: python3 -m ejemplos.pdf_guia_industrial && python3 -m ejemplos.pdf_fotos_guia_industrial"""
import pymupdf

FOTOS = [
    "docs/tareas/imagenes/respondidas/1-detalle-del-gasto-respondido.jpg",
    "docs/tareas/imagenes/respondidas/2-hoja-de-costos-respondida.jpg",
    "docs/tareas/imagenes/respondidas/3-estado-de-resultados-respondido.jpg",
]
CALCULOS = "docs/tareas/guia-industrial-entrega.pdf"
SALIDA = "docs/tareas/guia-industrial-fotos-respondidas.pdf"

doc = pymupdf.open()
for ruta in FOTOS:
    img = pymupdf.open(ruta)
    ancho, alto = img[0].rect.width, img[0].rect.height
    horizontal = ancho > alto
    caja = pymupdf.Rect(0, 0, 842, 595) if horizontal else pymupdf.Rect(0, 0, 595, 842)
    pagina = doc.new_page(width=caja.width, height=caja.height)
    pagina.show_pdf_page(caja + (15, 15, -15, -15), pymupdf.open("pdf", img.convert_to_pdf()), 0)
doc.insert_pdf(pymupdf.open(CALCULOS))
doc.save(SALIDA)
print("PDF listo:", SALIDA, "-", len(doc), "páginas")
