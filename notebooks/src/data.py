# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils_1.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aurele <aurele@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/08 21:16:01 by aurele            #+#    #+#              #
#    Updated: 2026/03/08 21:16:03 by aurele           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from __future__ import annotations

from pathlib import Path
from typing import Iterable
import re

import pandas as pd

import urllib.request as request


EXPECTED_COLUMNS = [
    "note",
    "auteur",
    "avis",
    "assureur",
    "produit",
    "type",
    "date_publication",
    "date_exp",
    "avis_en",
    "avis_cor",
    "avis_cor_en",
]

TEXT_COLUMNS = [
    "auteur",
    "avis",
    "assureur",
    "produit",
    "type",
    "avis_en",
    "avis_cor",
    "avis_cor_en",
]

DATE_COLUMNS = ["date_publication", "date_exp"]

def ensure_data(data_dir, file_dir, url):
    if not file_dir.exists():
        print(f"Data not found at {file_dir}. Downloading from GitHub...")
        
        # Create directory if it doesn't exist
        data_dir.mkdir(parents=True, exist_ok=True)
        try:
            request.urlretrieve(url, file_dir)
            print("Download successful!")
        except Exception as e:
            print(f"Failed to download data: {e}")
    else:
        print("Data found locally, skipping download.")

def list_excel_files(folder: str | Path, pattern: str = "avis_*_traduit.xlsx") -> list[Path]:
    """Return all matching Excel files sorted by the numeric index in the filename."""
    folder = Path(folder)
    files = list(folder.glob(pattern))
    return sorted(files, key=_extract_file_number)


def _extract_file_number(path: str | Path) -> int:
    match = re.search(r"avis_(\d+)_traduit\.xlsx", Path(path).name)
    return int(match.group(1)) if match else 10**9


def read_review_file(file_path: str | Path, sheet_name: str | int = 0) -> pd.DataFrame:
    """
    Read one translated review file and keep source-level metadata.
    No heavy cleaning here: just raw loading + provenance columns.
    """
    file_path = Path(file_path)
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df["source_file"] = file_path.name
    df["source_id"] = _extract_file_number(file_path)
    return df


def concat_review_files(files: Iterable[str | Path], ignore_index: bool = True) -> pd.DataFrame:
    """Read and concatenate every review file into a single dataframe."""
    frames = [read_review_file(file_path) for file_path in files]
    if not frames:
        return pd.DataFrame(columns=EXPECTED_COLUMNS + ["source_file", "source_id"])
    return pd.concat(frames, ignore_index=ignore_index)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names, trim spaces, and replace spaces with underscores."""
    out = df.copy()
    out.columns = [
        str(col).strip().lower().replace(" ", "_") for col in out.columns
    ]
    return out


def reorder_known_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Move expected columns first while preserving any extra columns at the end."""
    ordered = [col for col in EXPECTED_COLUMNS if col in df.columns]
    remaining = [col for col in df.columns if col not in ordered]
    return df[ordered + remaining]


def clean_basic_text(value: object) -> object:
    """Light text normalization without changing semantic content."""
    if pd.isna(value):
        return pd.NA
    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text_columns(df: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    columns = list(columns) if columns is not None else [c for c in TEXT_COLUMNS if c in out.columns]
    for col in columns:
        out[col] = out[col].apply(clean_basic_text)
    return out


def cast_note_numeric(df: pd.DataFrame, column: str = "note") -> pd.DataFrame:
    out = df.copy()
    if column in out.columns:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out


def parse_date_columns(df: pd.DataFrame, columns: Iterable[str] | None = None, dayfirst: bool = True) -> pd.DataFrame:
    """Parse review dates to datetime. Keep NaT when parsing fails."""
    out = df.copy()
    columns = list(columns) if columns is not None else [c for c in DATE_COLUMNS if c in out.columns]
    for col in columns:
        out[col] = pd.to_datetime(out[col], errors="coerce", dayfirst=dayfirst)
    return out


def add_row_uid(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.insert(0, "row_uid", range(1, len(out) + 1))
    return out


def minimal_prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal non-destructive preparation stage.
    Intended for the first pass before sanity checks:
    - normalize column names
    - reorder known columns
    - lightly clean text fields
    - cast note to numeric
    - add row id
    """
    out = normalize_column_names(df)
    out = reorder_known_columns(out)
    out = clean_text_columns(out)
    out = cast_note_numeric(out)
    out = add_row_uid(out)
    return out


def export_dataframe(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() == ".csv":
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
    elif output_path.suffix.lower() == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix.lower() in {".xlsx", ".xls"}:
        df.to_excel(output_path, index=False)
    else:
        raise ValueError(f"Unsupported export format: {output_path.suffix}")

    return output_path
