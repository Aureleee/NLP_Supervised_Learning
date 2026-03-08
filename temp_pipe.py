from __future__ import annotations

from pathlib import Path

from utils_1 import (
    concat_review_files,
    export_dataframe,
    list_excel_files,
    minimal_prepare,
)


DATA_DIR = Path("../data")
FILE_PATTERN = "avis_*_traduit.xlsx"
OUTPUT_DIR = DATA_DIR / "outputs"


def main() -> None:
    files = list_excel_files(DATA_DIR, pattern=FILE_PATTERN)

    if not files:
        raise FileNotFoundError(
            f"No files found in {DATA_DIR} matching pattern {FILE_PATTERN!r}."
        )

    df_raw = concat_review_files(files)
    df_prepared = minimal_prepare(df_raw)

    export_dataframe(df_raw, OUTPUT_DIR / "reviews_concat_raw.csv")
    export_dataframe(df_prepared, OUTPUT_DIR / "reviews_concat_prepared.csv")

    print(f"Files detected: {len(files)}")
    print(f"Rows in raw concatenated dataframe: {len(df_raw)}")
    print(f"Columns: {list(df_raw.columns)}")
    print(f"Saved raw file to: {OUTPUT_DIR / 'reviews_concat_raw.csv'}")
    print(f"Saved prepared file to: {OUTPUT_DIR / 'reviews_concat_prepared.csv'}")


if __name__ == "__main__":
    main()
