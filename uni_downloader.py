"""Tool to download all videos from a TU Graz Online LV.

For this to work, a html file has to be deposited in the
working directory (the same directory where all the videos
will be saved to). In this html file, there has to be
information about all the videos that should be downloaded.

If not all videos are displayed when loading the page,
you have to scoll until all videos are loaded.

The defaults will work, if the script and the html file
called 'data.html' are in the current working directory.

This script needs yt-dlp to work correctly:
    https://github.com/yt-dlp/yt-dlp
"""

import subprocess
import argparse
import os
from bs4 import BeautifulSoup
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--working_directory", "wd", type=str, default=None)
    parser.add_argument("--data_file", "df", type=str, default="data.html")
    args = parser.parse_args()

    if args.working_directory is not None:
        os.chdir(args.working_directory)

    path = Path("./")

    downloaded_files = [p.stem for p in path.iterdir() if p.suffix == ".mp4"]

    # Load the extracted html into bs.
    with open(args.data_file) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    items = soup.find_all("div", class_="page-content-box")

    link_general = "https://tube.tugraz.at/paella/ui/"

    for i, item in enumerate(items):
        link_specific = item.find("a", class_="content-box-episode-link").get("href")
        link = f"{link_general}{link_specific}"
        title = item.find("div", class_="content-box-episode-title").get("title")

        print(f"Downloading {i}/{len(items)}")

        # If the file is already in the directory, dont download it again.
        if title in downloaded_files:
            print(f"File {title}.mp4 already downloaded, skipping.")
            continue

        # print(f"yt-dlp -o {title}.(ext)s {link}")
        subprocess.run(["yt-dlp", "-o", f"{title}.%(ext)s", f"{link}"])


if __name__ == "__main__":
    main()
