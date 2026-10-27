"""Genera docs/tareas/guia-compraventas-fotos-respondidas.pdf: las 3 fotos respondidas y, después, los cálculos.
Uso: python3 -m ejemplos.pdf_fotos_guia_compraventas   (antes: python3 -m ejemplos.pdf_guia_compraventas y python3 -m ejemplos.fotos_guia_compraventas)"""
import pymupdf

CARPETA = "docs/tareas/imagenes/respondidas/"
SALIDA = "docs/tareas/guia-compraventas-fotos-respondidas.pdf"
FOTOS = [("compraventas-hoja2-respondida.jpg", "Hoja 2: compras, crédito fiscal, impuesto retenido y asiento"),
         ("compraventas-hoja3-respondida.jpg", "Hoja 3: ventas, débito fiscal y PPM"),
         ("compraventas-hoja4-respondida.jpg", "Hoja 4: impuesto único de segunda categoría (dos trabajadores)")]

pdf = pymupdf.open()
for archivo, titulo in FOTOS:
    pagina = pdf.new_page(width=595, height=842)
    pagina.insert_text((40, 30), titulo, fontsize=11, color=(0.08, 0.27, 0.42))
    pagina.insert_image(pymupdf.Rect(40, 40, 555, 40 + 515 * 4 / 3), filename=CARPETA + archivo)
    pagina.insert_text((40, 40 + 515 * 4 / 3 + 14), "Alumno: Joaquín Verdejo · 4.° C · Cálculo y registro de impuestos (Juan Castillo Araya) · septiembre 2026 · PPM 0,55 %",
                       fontsize=7, color=(0.3, 0.3, 0.3))
pdf.insert_pdf(pymupdf.open("docs/tareas/guia-compraventas-respuestas.pdf"))
pdf.save(SALIDA)
print("PDF listo:", SALIDA, len(pdf), "páginas")
