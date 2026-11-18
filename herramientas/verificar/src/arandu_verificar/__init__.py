"""arandu-verificar · Taller I · contrato v1.

Corre cada caso de aceptación (un archivo .json) contra el sistema del estudiante y compara la
respuesta con el resultado esperado. No contiene ninguna implementación de las reglas: solo
ejecuta el comando del estudiante y compara.

Uso:
    arandu-verificar                     # corre los casos de ./casos contra «uv run arandu evaluar»
    arandu-verificar casos casos-publicos
    arandu-verificar --publicos          # corre los 13 casos públicos de la cátedra
    arandu-verificar --solo-esquema      # solo revisa que los casos cumplan el formato
    arandu-verificar --cmd "python -m arandu evaluar" casos
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from importlib import resources
from pathlib import Path

import jsonschema


def _esquema() -> dict:
    return json.loads(resources.files(__package__).joinpath("caso-v1.schema.json").read_text(encoding="utf-8"))


def _casos(carpetas: list[str]) -> list[Path]:
    archivos: list[Path] = []
    for c in carpetas:
        p = Path(c)
        archivos += sorted(p.glob("*.json")) if p.is_dir() else [p]
    return archivos


def validar(archivo: Path, esquema: dict) -> tuple[dict | None, str | None]:
    try:
        datos = json.loads(archivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return None, f"no es JSON válido: {e}"
    try:
        jsonschema.validate(datos, esquema)
    except jsonschema.ValidationError as e:
        donde = "/".join(str(x) for x in e.absolute_path) or "(raíz)"
        return None, f"no cumple el formato en {donde}: {e.message}"
    return datos, None


def ejecutar(cmd: str, archivo: Path, timeout: float = 30) -> tuple[dict | None, str | None]:
    try:
        r = subprocess.run(shlex.split(cmd) + [str(archivo)], check=False, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return None, f"no se encontró el comando: {cmd}"
    except subprocess.TimeoutExpired:
        return None, f"tardó más de {timeout:.0f} s"
    salida = r.stdout.strip().splitlines()
    if not salida:
        return None, f"no imprimió nada (código {r.returncode}). stderr: {r.stderr.strip()[-200:]}"
    try:
        return json.loads(salida[-1]), None
    except json.JSONDecodeError:
        return None, f"la última línea no es JSON: {salida[-1][:120]}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="arandu-verificar", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpetas", nargs="*", default=["casos"])
    ap.add_argument("--cmd", default="uv run arandu evaluar", help="comando que recibe la ruta del caso (por defecto: %(default)s)")
    ap.add_argument("--solo-esquema", action="store_true", help="solo revisar el formato de los casos")
    ap.add_argument("--publicos", action="store_true", help="correr los casos públicos de la cátedra (incluidos en la herramienta)")
    a = ap.parse_args(argv)
    if a.publicos:
        a.carpetas = [str(resources.files(__package__).joinpath("casos_publicos"))]

    esquema = _esquema()
    archivos = _casos(a.carpetas)
    if not archivos:
        print(f"No hay casos en {', '.join(a.carpetas)}.")
        return 1
    ok = fallas = 0
    for f in archivos:
        datos, error = validar(f, esquema)
        if error:
            fallas += 1
            print(f"✗ {f.name}: {error}")
            continue
        if a.solo_esquema:
            ok += 1
            print(f"✓ {f.name}")
            continue
        obtenido, error = ejecutar(a.cmd, f)
        if error:
            fallas += 1
            print(f"✗ {datos['caso']}: {error}")
        elif obtenido == datos["esperado"]:
            ok += 1
            print(f"✓ {datos['caso']}")
        else:
            fallas += 1
            print(f"✗ {datos['caso']}: esperado {json.dumps(datos['esperado'], ensure_ascii=False)}, "
                  f"obtenido {json.dumps(obtenido, ensure_ascii=False)}")
    print(f"\n{ok} de {ok + fallas} casos correctos.")
    return 0 if fallas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
