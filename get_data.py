import requests
import os
import subprocess
import sys
import platform
from pathlib import Path


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

end_path = os.path.basename(os.path.normpath(dname)) 



if "MA2502_CW2" not in end_path: # just in case you download the zip also
    sys.exit("Running outside of repo - wrong folder")

Path("Data/zips").mkdir(parents=True, exist_ok=True)

os.chdir(f"{dname}/Data/zips")

files = [
    ("historical-nba-data-and-player-box-scores.zip",
     "https://www.kaggle.com/api/v1/datasets/download/eoinamoore/historical-nba-data-and-player-box-scores"),
    ("nba-aba-baa-stats.zip",
     "https://www.kaggle.com/api/v1/datasets/download/sumitrodatta/nba-aba-baa-stats"),
    ("wyatt_basketball.zip",
     "https://www.kaggle.com/api/v1/datasets/download/wyattowalsh/basketball")
]

running_os = platform.system()

for filename, url in files:
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {filename}")

    print(f"Extracting {filename}")
    
    if running_os == "Windows":
        subprocess.run(["powershell", "-Command", f"Expand-Archive -Path {filename} -DestinationPath ../{os.path.splitext(filename)[0]}"])
    elif running_os == "Linux":
        subprocess.run(["unzip", filename, "-d", f"../{os.path.splitext(filename)[0]}"])
    else:
        raise NotImplementedError
    
    print(f"Extracted {filename}")

## now get another height dataset from github
# https://github.com/simonwarchol/NBA-Height-Weight

os.chdir(f"{dname}/Data/")

subprocess.run(["git", "clone", r"https://github.com/simonwarchol/NBA-Height-Weight.git"])

os.chdir(f"{dname}")

