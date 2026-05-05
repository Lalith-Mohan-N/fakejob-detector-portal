import os
import zipfile
from pathlib import Path

import kaggle


def download_emscad_dataset(output_dir: Path | str = "data/raw") -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    dataset = "shivamb/real-or-fake-fake-jobposting-prediction"
    print(f"Downloading EMSCAD dataset from Kaggle: {dataset}")
    kaggle.api.dataset_download_files(dataset, path=str(output), unzip=True)

    csv_file = output / "fake_job_postings.csv"
    if csv_file.exists():
        print(f"Dataset ready at {csv_file}")
    else:
        for zf in output.glob("*.zip"):
            with zipfile.ZipFile(zf, "r") as zip_ref:
                zip_ref.extractall(output)
            zf.unlink()
        print(f"Extracted dataset to {output}")
    return output


if __name__ == "__main__":
    download_emscad_dataset()
