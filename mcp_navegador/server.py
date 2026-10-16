"""MCP de navegador para estudiar (se ejecuta en TU PC; Claude lo usa a través de un túnel).

Qué hace: abre páginas en una ventana de Chrome/Chromium con perfil propio (tú inicias sesión a mano), lee el texto,
saca capturas y guarda texto de páginas en una carpeta de trabajo. NO escribe en formularios, NO hace clics (salvo que lo actives),
NO ejecuta comandos, NO lee archivos de tu PC. Solo navega por una lista blanca de dominios.

Variables de entorno:
  MCP_SECRETO            (obligatoria) texto largo al azar; va en la URL: https://.../<secreto>/mcp
  DOMINIOS_PERMITIDOS    coma-separados (por defecto: sii.cl, previred.com, afpcapital.cl, cmfchile.cl, classroom.google.com,
                         accounts.google.com, spensiones.cl, bcn.cl, dt.gob.cl)
  CARPETA_TRABAJO        donde se guardan los textos (por defecto ./descargas_mcp)
  PERFIL_NAVEGADOR       carpeta del perfil (por defecto ./perfil_mcp)
  SIN_VENTANA=1          navegador oculto (por defecto se ve la ventana)
  PERMITIR_CLICS=1       activa la herramienta hacer_clic (apagada por defecto)
  NAVEGADOR_EJECUTABLE   ruta de chrome.exe si no usas el Chromium de Playwright (opcional)
  PUERTO                 por defecto 8765
Uso: python mcp_navegador/server.py
"""
import asyncio
import datetime
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP, Image
from playwright.async_api import async_playwright

SECRETO = os.environ.get("MCP_SECRETO", "")
if len(SECRETO) < 24:
    sys.exit("Define MCP_SECRETO con al menos 24 caracteres al azar (ej.: python -c \"import secrets;print(secrets.token_urlsafe(32))\")")
DOMINIOS = [d.strip().lower() for d in os.environ.get(
    "DOMINIOS_PERMITIDOS",
    "sii.cl,previred.com,afpcapital.cl,cmfchile.cl,classroom.google.com,accounts.google.com,spensiones.cl,bcn.cl,dt.gob.cl").split(",") if d.strip()]
CARPETA = Path(os.environ.get("CARPETA_TRABAJO", "descargas_mcp")).resolve()
PERFIL = Path(os.environ.get("PERFIL_NAVEGADOR", "perfil_mcp")).resolve()
CARPETA.mkdir(parents=True, exist_ok=True)
LOG = CARPETA / "registro.log"

mcp = FastMCP("navegador-estudio", host="127.0.0.1", port=int(os.environ.get("PUERTO", "8765")),
              streamable_http_path=f"/{SECRETO}/mcp")
_estado = {}
_cerrojo = asyncio.Lock()


def registrar(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} {msg}\n")


def permitido(url):
    host = (urlparse(url).hostname or "").lower()
    return urlparse(url).scheme in ("http", "https") and any(host == d or host.endswith("." + d) for d in DOMINIOS)


async def pagina():
    async with _cerrojo:
        if "ctx" not in _estado:
            _estado["pw"] = await async_playwright().start()
            _estado["ctx"] = await _estado["pw"].chromium.launch_persistent_context(
                str(PERFIL), headless=bool(os.environ.get("SIN_VENTANA")), accept_downloads=False,
                executable_path=os.environ.get("NAVEGADOR_EJECUTABLE") or None,
                args=["--no-sandbox"] if os.environ.get("SIN_SANDBOX") else [])
            _estado["page"] = _estado["ctx"].pages[0] if _estado["ctx"].pages else await _estado["ctx"].new_page()
        return _estado["page"]


async def verificar_destino(p):
    if p.url != "about:blank" and not permitido(p.url):
        destino = p.url
        await p.goto("about:blank")
        registrar(f"BLOQUEADO redirección a {destino}")
        raise ValueError("La página terminó en un dominio fuera de la lista blanca; la cerré.")


@mcp.tool()
async def abrir_url(url: str) -> str:
    """Abre una URL (solo dominios de la lista blanca) y devuelve título y dirección final."""
    if not permitido(url):
        registrar(f"BLOQUEADO {url}")
        return f"Dominio no permitido. Permitidos: {', '.join(DOMINIOS)}"
    p = await pagina()
    await p.goto(url, wait_until="domcontentloaded", timeout=45000)
    await verificar_destino(p)
    registrar(f"ABRIR {p.url}")
    return f"{await p.title()} | {p.url}"


@mcp.tool()
async def leer_texto(max_caracteres: int = 20000) -> str:
    """Devuelve el texto visible de la página actual (máx. 60.000 caracteres)."""
    p = await pagina()
    await verificar_destino(p)
    texto = await p.inner_text("body")
    registrar(f"LEER {p.url} ({len(texto)} car.)")
    return texto[:min(max_caracteres, 60000)]


@mcp.tool()
async def listar_enlaces(max_enlaces: int = 80) -> str:
    """Lista los enlaces (texto → URL) de la página actual."""
    p = await pagina()
    await verificar_destino(p)
    enlaces = await p.eval_on_selector_all(
        "a[href]", "els => els.map(e => [e.innerText.trim().slice(0,80), e.href])")
    return "\n".join(f"{t or '(sin texto)'} → {h}" for t, h in enlaces[:max_enlaces])


@mcp.tool()
async def captura_pantalla() -> Image:
    """Captura de la parte visible de la página actual."""
    p = await pagina()
    await verificar_destino(p)
    registrar(f"CAPTURA {p.url}")
    return Image(data=await p.screenshot(type="png"), format="png")


@mcp.tool()
async def guardar_texto_pagina(nombre: str) -> str:
    """Guarda el texto de la página actual en la carpeta de trabajo (solo nombres simples, se le agrega .txt)."""
    p = await pagina()
    await verificar_destino(p)
    limpio = re.sub(r"[^A-Za-z0-9_.-]", "_", nombre)[:80] or "pagina"
    ruta = CARPETA / f"{limpio}.txt"
    ruta.write_text(f"Fuente: {p.url}\n\n" + await p.inner_text("body"), encoding="utf-8")
    registrar(f"GUARDAR {p.url} -> {ruta.name}")
    return f"Guardado en {ruta}"


if os.environ.get("PERMITIR_CLICS") == "1":
    @mcp.tool()
    async def hacer_clic(texto: str) -> str:
        """Hace clic en un enlace o botón por su texto visible (activado con PERMITIR_CLICS=1). No escribe en formularios."""
        p = await pagina()
        await verificar_destino(p)
        await p.get_by_text(texto, exact=False).first.click(timeout=15000)
        await p.wait_for_load_state("domcontentloaded")
        await verificar_destino(p)
        registrar(f"CLIC '{texto}' -> {p.url}")
        return f"{await p.title()} | {p.url}"


if __name__ == "__main__":
    print(f"Servidor en http://127.0.0.1:{mcp.settings.port}/<secreto>/mcp  | dominios: {', '.join(DOMINIOS)}", flush=True)
    mcp.run(transport="streamable-http")
