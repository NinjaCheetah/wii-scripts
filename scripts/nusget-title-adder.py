# "nusget-title-adder.py" from wii-scripts by NinjaCheetah
# https://github.com/NinjaCheetah/wii-scripts'

import json
import libWiiPy


if __name__ == '__main__':
    # This program expects to find a text file with the list of TIDs and names that you want to add named the same as
    # the category you want the titles added under.
    print("Welcome to NUSGet Title Adder")
    category_name = input("Enter the name of the category to add: ")
    title_dict = {category_name : []}
    valid_titles = []
    with open(f"{category_name}.txt", 'r') as infile:
        for line in infile:
            line = line.strip()
            tid, name = line.split(' ', 1)
            regioned_tids = [("USA/NTSC", f"{tid[:-2]}45"), ("Europe/PAL", f"{tid[:-2]}50"),
                             ("Japan", f"{tid[:-2]}4A"), ("Korea", f"{tid[:-2]}4B")]
            versions = {}
            for region, target_tid in regioned_tids:
                tmd = libWiiPy.title.TMD()
                try:
                    tmd.load(libWiiPy.title.download_tmd(target_tid))
                    versions[region] = [tmd.title_version]
                except Exception:
                    print(f"Title does not exist for region: {region}")
                    pass
            valid_titles.append((tid, name, versions))
            print((tid, name, versions))
    for tid, name, versions in valid_titles:
        if versions == {}:
            continue
        title_dict[category_name].append(
            {
                "Name": name,
                "TID": tid.upper(),
                "Versions": versions,
                "Ticket": False
            }
        )
    print(f"Done! Wrote data to {category_name}.json")
    open(f"{category_name}.json", 'w').write(json.dumps(title_dict, indent=2))
