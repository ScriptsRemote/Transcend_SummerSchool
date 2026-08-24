#!/usr/bin/env python3
"""
split_master_notebook.py
========================

Fragmenta el notebook maestro del Summer School TRANSCEND (el que vive en
Google Colab) en un notebook por bloque horario, dentro de la carpeta de cada
dia.

El maestro debe seguir esta estructura de celdas markdown:

    #**Day N - <titulo del dia>**
    ## 1.<tema del bloque 09:00-10:30> [instructores]
    ### 1.1 -
    ## 2.<tema del bloque 10:40-12:10> [instructores]
    ...

Uso
---
    python tools/split_master_notebook.py --master master.ipynb --dry-run
    python tools/split_master_notebook.py --master master.ipynb

Descargar el maestro desde Colab: Archivo -> Descargar -> Descargar .ipynb

AVISO: sin --dry-run, los notebooks generados se SOBRESCRIBEN. Los README y la
carpeta Assets/ nunca se tocan.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import random
import re
import string
import sys

SLOTS = ["09:00 - 10:30", "10:40 - 12:10", "14:00 - 15:30", "15:40 - 17:10"]

DAYS = [
    dict(n=1, date="2026-10-12", weekday="Monday / Lunes",
         folder="Day1_Hydrology_and_WEAP_Modeling",
         title="Hydrology & WEAP Modeling",
         entity="SEI",
         slugs=["hydrology_fundamentals_weap_structure",
                "soil_moisture_method_and_calibration",
                "climate_data_interpolation_and_lulc",
                "weap_model_consolidation"]),
    dict(n=2, date="2026-10-13", weekday="Tuesday / Martes",
         folder="Day2_Hydroeconomics_and_Water_Mapping",
         title="Hydroeconomics & Water Mapping",
         entity="SEI / IMDEA",
         slugs=["agricultural_demand_and_economic_modeling",
                "sensors_and_spectral_behaviour",
                "vegetation_and_water_spectral_indices",
                "platforms_gee_colab_and_qgis"]),
    dict(n=3, date="2026-10-14", weekday="Wednesday / Miercoles",
         folder="Day3_Remote_Sensing_Fundamentals_and_Indices",
         title="Fundamentals of Remote Sensing & Spectral Indices",
         entity="UoM",
         slugs=["long_term_surface_water_jrc",
                "water_quality_proxies",
                "satellite_altimetry_shallow_lakes",
                "digital_image_processing_in_gee"]),
    dict(n=4, date="2026-10-15", weekday="Thursday / Jueves",
         folder="Day4_LULC_and_Climate_with_RS",
         title="Land Use / Land Cover & Climate with RS",
         entity="UoM",
         slugs=["classification_fundamentals_and_algorithms",
                "building_the_classification_input",
                "training_mapping_and_accuracy",
                "climate_products_et_and_water_balance"]),
    dict(n=5, date="2026-10-16", weekday="Friday / Viernes",
         folder="Day5_Soil_Monitoring_and_Irrigation_Efficiency",
         title="Soil Monitoring & Irrigation Efficiency",
         entity="IIAREN / PROSUCO",
         slugs=["soil_salinity_models_part1_fundamentals",
                "soil_salinity_models_part2_validation",
                "automated_drip_irrigation_system",
                "integration_and_water_use_efficiency"]),
]

_FIX = {"gee": "GEE", "jrc": "JRC", "lulc": "LULC", "et": "ET", "weap": "WEAP",
        "rs": "RS", "qgis": "QGIS", "and": "and", "in": "in", "the": "the",
        "of": "of", "part1": "part 1", "part2": "part 2"}


# --------------------------------------------------------------------- helpers
def nid() -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {"id": nid()},
            "source": text.splitlines(keepends=True)}


def code(text: str = "") -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {"id": nid()},
            "outputs": [], "source": text.splitlines(keepends=True)}


def notebook(cells: list) -> dict:
    return {"nbformat": 4, "nbformat_minor": 0,
            "metadata": {"colab": {"provenance": [], "toc_visible": True},
                         "kernelspec": {"name": "python3", "display_name": "Python 3"},
                         "language_info": {"name": "python"}},
            "cells": cells}


def instructors(topic: str) -> str:
    """Ultimo bloque [entre corchetes] del tema."""
    found = re.findall(r"\[([^\[\]]+)\]", topic)
    return found[-1].strip() if found else ""


def strip_instructors(topic: str) -> str:
    """Texto del tema sin el ultimo bloque [instructores]."""
    found = list(re.finditer(r"\[([^\[\]]+)\]", topic))
    if not found:
        return topic.strip()
    last = found[-1]
    return (topic[:last.start()] + topic[last.end():]).strip(" -.–—\t")


def short_title(slug: str) -> str:
    words = slug.split("_")
    out = [_FIX.get(w.lower(), w.capitalize()) for w in words]
    if out and out[0].islower():
        out[0] = out[0].capitalize()
    return " ".join(out)


def parse_master(master_path: pathlib.Path) -> dict:
    """Devuelve {numero_de_dia: [tema_bloque1, ..., tema_bloque4]}."""
    nb = json.loads(master_path.read_text(encoding="utf-8"))
    topics: dict = {}
    current = None
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        s = "".join(cell["source"]).strip()
        if s.startswith("#**Day "):
            current = int(s.split("Day ")[1].split(" ")[0])
            topics.setdefault(current, [])
        elif current and s.startswith("## ") and s[3:4].isdigit() and s[4:5] == ".":
            topics[current].append(" ".join(s[5:].split()))
    return topics


def build(day: dict, k: int, topic: str) -> dict:
    who = instructors(topic)
    body = strip_instructors(topic)
    short = short_title(day["slugs"][k - 1])

    cells = [md(
        f"# Day {day['n']} - {day['title']}\n"
        f"## Session {k}: {short}\n\n"
        f"| | |\n|---|---|\n"
        f"| **Fecha / Date** | {day['date']} ({day['weekday']}) |\n"
        f"| **Horario / Time** | {SLOTS[k - 1]} |\n"
        f"| **Entidad / Entity** | {day['entity']} |\n"
        f"| **Instructores / Instructors** | {who or 'TBD'} |\n\n"
        f"### Contenido / Content\n\n> {body}\n\n"
        f"### Objetivos de aprendizaje / Learning objectives\n\n"
        f"- [ ] Objetivo 1\n- [ ] Objetivo 2\n- [ ] Objetivo 3\n\n"
        f"### Datos necesarios / Required data\n\n"
        f"Los insumos de esta sesion estan en `Assets/Day{day['n']}/`.\n"
        f"Ver `Assets/README.md` para las convenciones de nombres y formatos.\n\n---\n")]

    cells.append(md(f"## {k}.1 - Teoria / Theory\n\n_Notas del instructor._\n"))
    cells.append(code())
    cells.append(md(f"## {k}.2 - Practica guiada / Guided hands-on\n"))
    cells.append(code())
    cells.append(md(f"## {k}.3 - Ejercicio / Exercise\n\n**Consigna:**\n\n**Entregable:**\n"))
    cells.append(code())
    cells.append(md("## Referencias / References\n\n- \n"))
    return notebook(cells)


# ------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--master", required=True, type=pathlib.Path,
                    help="ruta al notebook maestro descargado de Colab")
    ap.add_argument("--root", type=pathlib.Path,
                    default=pathlib.Path(__file__).resolve().parents[1],
                    help="raiz del repositorio (por defecto: la carpeta padre de tools/)")
    ap.add_argument("--dry-run", action="store_true",
                    help="muestra lo que se escribiria, sin tocar el disco")
    args = ap.parse_args()

    if not args.master.is_file():
        print(f"ERROR: no existe {args.master}", file=sys.stderr)
        return 1

    topics = parse_master(args.master)
    problems = [d["n"] for d in DAYS if len(topics.get(d["n"], [])) != 4]
    if problems:
        print(f"ERROR: los dias {problems} no tienen exactamente 4 bloques en el maestro.",
              file=sys.stderr)
        print("       Revise que cada bloque empiece con '## N.' bajo su '#**Day N'.",
              file=sys.stderr)
        return 1

    written = 0
    for day in DAYS:
        folder = args.root / day["folder"]
        for k, (topic, slug) in enumerate(zip(topics[day["n"]], day["slugs"]), start=1):
            path = folder / f"{k:02d}_{slug}.ipynb"
            if args.dry_run:
                verb = "sobrescribiria" if path.exists() else "crearia"
                print(f"[dry-run] {verb}: {path.relative_to(args.root)}")
                continue
            folder.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(build(day, k, topic), ensure_ascii=False, indent=1),
                            encoding="utf-8")
            written += 1

    if args.dry_run:
        print("\nNada fue escrito. Quite --dry-run para aplicar.")
    else:
        print(f"{written} notebooks escritos en {args.root}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        pass
