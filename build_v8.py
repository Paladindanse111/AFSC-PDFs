#!/usr/bin/env python3
"""
build_v8.py
Run this in your repo root (next to USAF_Bases_Long_Format_v7.csv
and pilot_billet_locations.csv) to produce USAF_Bases_Long_Format_v8.csv

New columns added:
  Aircraft   - airframe at that base (one row per aircraft)
  Base_Type  - "Active Duty", "ANG", or "Reserve"
"""

import csv

# ── 1. ANG / Reserve base definitions ────────────────────────────────────
# (Base name, Latitude, Longitude, MGRS, Wing website, Aircraft list, Base_Type)
ANG_BASES = [
    ("ATLANTIC CITY ANGB",  "39°26'42.05\"N", "74°35'00.46\"W",  "18S WJ 35841 66244",
     "https://www.177fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("BIRMINGHAM ANGB",     "33°34'07.46\"N", "86°45'19.27\"W",  "16S EC 22706 14367",
     "https://www.117arw.ang.af.mil/",   ["KC-135"],          "ANG"),
    ("BOISE AIR TERMINAL",  "43°33'48.03\"N", "116°13'42.28\"W", "11T NJ 62313 23665",
     "https://www.124fw.ang.af.mil/",    ["A-10"],            "ANG"),
    ("BURLINGTON ANGB",     "44°28'26.48\"N", "73°08'44.61\"W",  "18T XQ 47476 26195",
     "https://www.158fw.ang.af.mil/",    ["F-35"],            "ANG"),
    ("DANE CO REGIONAL",    "43°07'43.64\"N", "89°19'59.14\"W",  "16T CN 10227 77758",
     "https://www.115fw.ang.af.mil/",    ["F-35"],            "ANG"),
    ("DOBBINS ARB",         "33°55'10.69\"N", "84°30'11.59\"W",  "16S GC 30816 56052",
     "https://www.dobbins.afrc.af.mil/", ["C-130J"],          "Reserve"),
    ("DOTHAN RGNL",         "31°19'45.80\"N", "85°28'00.41\"W",  "16R FV 45872 67122",
     "https://www.187fw.ang.af.mil/",    ["F-35"],            "ANG"),
    ("DUKE FIELD",          "30°38'39.32\"N", "86°31'42.41\"W",  "16R EU 45183 90272",
     "https://www.919sow.afrc.af.mil/",  ["MC-130J","AC-130J","U-28"], "Reserve"),
    ("DULUTH INTL",         "46°50'51.90\"N", "92°10'17.62\"W",  "15T WM 63161 88578",
     "https://www.148fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("EBBING ANGB",         "35°20'20.84\"N", "94°22'15.13\"W",  "15S UV 75420 11513",
     "https://www.188wg.ang.af.mil/",    ["F-35"],            "ANG"),
    ("FORT WAYNE ANGB",     "40°59'18.94\"N", "85°10'27.33\"W",  "16T FL 53577 39096",
     "https://www.122fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("FORT WORTH NAS JRB",  "32°47'05.32\"N", "97°25'42.50\"W",  "14S PB 47168 28524",
     "https://www.136aw.ang.af.mil/",    ["C-130J"],          "ANG"),
    ("FRESNO YOSEMITE IAP", "36°45'55.32\"N", "119°42'51.19\"W", "11S KA 57733 72280",
     "https://www.144fw.ang.af.mil/",    ["F-15"],            "ANG"),
    ("HOMESTEAD ARB",       "25°29'38.75\"N", "80°23'38.92\"W",  "17R NJ 60890 19798",
     "https://www.482fw.afrc.af.mil/",   ["F-16"],            "Reserve"),
    ("JACKSONVILLE ANGB",   "30°29'12.57\"N", "81°42'09.47\"W",  "17R MP 32565 72941",
     "https://www.125fw.ang.af.mil/",    ["F-15","F-35"],     "ANG"),
    ("JOE FOSS FIELD",      "43°34'20.99\"N", "96°44'36.80\"W",  "14T PP 82204 26866",
     "https://www.114fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("KINGSLEY FIELD",      "42°09'39.98\"N", "121°44'37.36\"W", "10T FM 03780 68427",
     "https://www.173fw.ang.af.mil/",    ["F-15","F-35"],     "ANG"),
    ("MARCH ARB",           "33°53'26.85\"N", "117°15'42.24\"W", "11S MT 75798 50078",
     "https://www.452amw.afrc.af.mil/",  ["C-17"],            "Reserve"),
    ("MARTIN STATE ANGB",   "39°20'04.63\"N", "76°25'05.12\"W",  "18S UJ 77783 54869",
     "https://www.175wg.ang.af.mil/",    ["A-10"],            "ANG"),
    ("MCENTIRE ANGB",       "33°56'21.44\"N", "80°48'04.75\"W",  "17S NT 18360 55442",
     "https://www.169fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("MINNEAPOLIS ST PAUL", "44°53'34.04\"N", "93°12'02.19\"W",  "15T VK 84159 71060",
     "https://www.133aw.ang.af.mil/",    ["C-130J"],          "ANG"),
    ("MONTGOMERY RGNL",     "32°18'17.80\"N", "86°24'16.52\"W",  "16S EA 56053 74392",
     "https://www.187fw.ang.af.mil/",    ["F-35"],            "ANG"),
    ("NEW ORLEANS NAS",     "29°49'36.42\"N", "90°01'15.36\"W",  "15R YP 87887 03316",
     "https://www.159fw.ang.af.mil/",    ["F-15"],            "ANG"),
    ("WILL ROGERS WORLD",   "35°24'27.86\"N", "97°36'36.18\"W",  "14S PE 26206 19148",
     "https://www.137sow.ang.af.mil/",   ["OA-1K"],           "ANG"),
    ("PEASE ANGB",          "43°05'15.99\"N", "70°48'57.47\"W",  "19T CH 52192 72162",
     "https://www.157arw.ang.af.mil/",   ["KC-46"],           "ANG"),
    ("PHILADELPHIA ANGB",   "40°12'20.78\"N", "75°08'25.02\"W",  "18T VK 88061 50605",
     "https://www.111atkw.ang.af.mil/",  ["F-16"],            "ANG"),
    ("PORTLAND INTL ANGB",  "45°34'31.71\"N", "122°35'32.03\"W", "10T ER 31815 46962",
     "https://www.142wg.ang.af.mil/",    ["F-15"],            "ANG"),
    ("PUEBLO MEM",          "38°16'48.21\"N", "104°30'25.32\"W", "13S EC 43116 37003",
     "https://www.140wg.ang.af.mil/",    ["F-16"],            "ANG"),
    ("ROSECRANS MEM",       "39°46'03.55\"N", "94°54'10.34\"W",  "15S UE 37016 03701",
     "https://www.139aw.ang.af.mil/",    ["C-130J"],          "ANG"),
    ("SAVANNAH HILTON HEAD","32°07'13.83\"N", "81°11'27.61\"W",  "17S MR 81982 53809",
     "https://www.165aw.ang.af.mil/",    ["C-130J"],          "ANG"),
    ("SELFRIDGE ANGB",      "42°36'53.11\"N", "82°49'43.95\"W",  "17T LH 50001 19656",
     "https://www.127wg.ang.af.mil/",    ["A-10","KC-135"],   "ANG"),
    ("SPRINGFIELD BECKLEY", "39°50'50.45\"N", "83°50'35.14\"W",  "17S KE 56756 14683",
     "https://www.178wg.ang.af.mil/",    ["F-16"],            "ANG"),
    ("ST LOUIS LAMBERT",    "38°30'11.64\"N", "90°16'37.73\"W",  "15S YC 37436 65166",
     "https://www.131bw.ang.af.mil/",    ["B-2"],             "ANG"),
    ("TOLEDO EXPRESS",      "41°35'12.89\"N", "83°47'43.99\"W",  "17T KG 66976 07688",
     "https://www.180fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("TULSA INTL",          "36°13'12.24\"N", "95°52'31.49\"W",  "15S TA 41534 12191",
     "https://www.138fw.ang.af.mil/",    ["F-16"],            "ANG"),
    ("WESTFIELD BARNES",    "42°10'03.56\"N", "72°43'28.62\"W",  "18T XM 87951 70897",
     "https://www.104fw.ang.af.mil/",    ["F-15","F-35"],     "ANG"),
    ("YEAGER",              "38°22'22.84\"N", "81°35'10.29\"W",  "17S MC 48795 47365",
     "https://www.130aw.ang.af.mil/",    ["C-130J"],          "ANG"),
    ("TUCSON ANGB",         "32°07'51.61\"N", "110°56'56.82\"W", "12S WA 04799 54957",
     "https://www.162wg.ang.af.mil/",    ["F-16"],            "ANG"),
    ("AMARILLO TRADEWIND",  "35°12'37.21\"N", "101°43'05.79\"W", "14S KD 52557 99754",
     "https://www.afrc.af.mil/",         ["C-130J"],          "Reserve"),
]

# ── 2. Build active-duty base->aircraft from pilot CSV ────────────────────
base_aircraft_raw = {}
with open("pilot_billet_locations.csv", newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        title = row["afsc_title"]
        base  = row["ilc_title"].strip()
        parts = title.split(",")
        if len(parts) >= 2:
            aircraft = parts[-1].strip()
            skip = {
                "GENERAL","OTHER","AIRLIFT","TANKER","BOMBER","FIGHTER",
                "HELO/VSTOL","AIR COMMANDO","AIRCRAFT COMMANDER",
                "AIRLFT/TANK/BOMB","ALO","AMLO","SUPT-H","RPA",
                "IFF (AT-38/T-38C)","GENERALIST PILOT","C-130E/H","C-130E/H)"
            }
            if aircraft not in skip:
                base_aircraft_raw.setdefault(base, set()).add(aircraft)

NAME_MAP = {
    "ALTUS":"ALTUS AFB","ANDERSEN":"ANDERSEN AFB","AVIANO":"AVIANO AB",
    "BARKSDALE":"BARKSDALE AFB","BEALE":"BEALE AFB","BUCKLEY":"BUCKLEY SFB",
    "CANNON":"CANNON AFB","COLUMBUS":"COLUMBUS AFB",
    "DAVIS-MONTHAN":"DAVIS-MONTHAN AFB","DOVER":"DOVER AFB","DYESS":"DYESS AFB",
    "EDWARDS":"EDWARDS AFB","EGLIN":"EGLIN AFB","EGLIN AFB":"EGLIN AFB",
    "EIELSON":"EIELSON AFB","ELLSWORTH":"ELLSWORTH AFB",
    "F E WARREN":"FE WARREN AFB","FAIRCHILD":"FAIRCHILD AFB",
    "GOODFELLOW":"GOODFELLOW AFB","GRAND FORKS":"GRAND FORKS AFB",
    "HANSCOM":"HANSCOM AFB","HILL":"HILL AFB","HOLLOMAN":"HOLLOMAN AFB",
    "HURLBURT FIELD":"HURLBURT FIELD","INCIRLIK":"INCIRLIK AB",
    "JBSA FT SAM":"JBSA FT SAM HOUSTON","JBSA LACKLAND":"JBSA LACKLAND",
    "JBSA RANDOLPH":"JBSA RANDOLPH","KADENA":"KADENA AB","KEESLER":"KEESLER AFB",
    "KIRTLAND":"KIRTLAND AFB","KUNSAN":"KUNSAN AB","LAKENHEATH":"LAKENHEATH RAF",
    "LAUGHLIN":"LAUGHLIN AFB","LITTLE ROCK":"LITTLE ROCK AFB","LUKE":"LUKE AFB",
    "MACDILL":"MACDILL AFB","MALMSTROM":"MALMSTROM AFB",
    "MAXWELL":"MAXWELL-GUNTER AFB","MCCONNELL":"MCCONNELL AFB",
    "MILDENHALL":"MILDENHALL RAF","MINOT":"MINOT AFB","MISAWA":"MISAWA AB",
    "MOODY":"MOODY AFB","MOUNTAIN HOME":"MOUNTAIN HOME AFB","NELLIS":"NELLIS AFB",
    "OFFUTT":"OFFUTT AFB","OSAN AB":"OSAN AB","PATRICK":"PATRICK SFB",
    "PENTAGON":"PENTAGON","PETERSON":"PETERSON SFB","POPE AAF":"POPE AAF",
    "RAMSTEIN":"RAMSTEIN AB","ROBINS":"ROBINS AFB","SCHRIEVER":"SCHRIEVER SFB",
    "SCOTT":"SCOTT AFB","SEYMOUR JOHNSON":"SEYMOUR JOHNSON AFB","SHAW":"SHAW AFB",
    "SHEPPARD":"SHEPPARD AFB","SPANGDAHLEM":"SPANGDAHLEM AB","TINKER":"TINKER AFB",
    "TRAVIS":"TRAVIS AFB","TYNDALL":"TYNDALL AFB","VANCE":"VANCE AFB",
    "VANDENBERG":"VANDENBERG SFB","WHITEMAN":"WHITEMAN AFB",
    "WRIGHT PATTERSON":"WRIGHT-PATTERSON AFB","YOKOTA":"YOKOTA AB",
    "JB ANDREWS":"ANDREWS JB","JB CHARLESTON":"JB CHARLESTON",
    "JB ELMENDORF-RICH":"JB ELMENDORF-RICHARDSON",
    "JB PRL HBR-HICKAM":"JB PEARL HARBOR-HICKAM",
    "JBLM MCCHORD":"JB LEWIS-MCCHORD","JBMDL MCGUIRE":"JB MCGUIRE-DIX-LAKEHURST",
    "JBAB BOLLING":"JB ANACOSTIA-BOLLING","FT CAMPBELL":"FT CAMPBELL",
    "FT RUCKER":"FT RUCKER",
}

master_aircraft = {}
for pb, aset in base_aircraft_raw.items():
    mb = NAME_MAP.get(pb)
    if mb:
        master_aircraft.setdefault(mb, set()).update(aset)

# ── 3. Read v7 and write v8 ───────────────────────────────────────────────
FIELDNAMES = [
    "Base","Latitude","Longitude","MGRS",
    "AFSC_Code","AFSC_Full_Name","PDF_URL","Base_URL",
    "Aircraft","Base_Type"
]

rows_written = 0

with open("USAF_Bases_Long_Format_v7.csv", newline="", encoding="utf-8-sig") as fin, \
     open("USAF_Bases_Long_Format_v8.csv", "w", newline="", encoding="utf-8") as fout:

    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=FIELDNAMES)
    writer.writeheader()

    # Active duty rows
    for row in reader:
        base = row["Base"]
        aircraft_list = sorted(master_aircraft.get(base, []))

        if aircraft_list:
            for ac in aircraft_list:
                writer.writerow({
                    "Base":           base,
                    "Latitude":       row["Latitude"],
                    "Longitude":      row["Longitude"],
                    "MGRS":           row["MGRS"],
                    "AFSC_Code":      row["AFSC_Code"],
                    "AFSC_Full_Name": row["AFSC_Full_Name"],
                    "PDF_URL":        row["PDF_URL"],
                    "Base_URL":       row["Base_URL"],
                    "Aircraft":       ac,
                    "Base_Type":      "Active Duty",
                })
                rows_written += 1
        else:
            writer.writerow({
                "Base":           base,
                "Latitude":       row["Latitude"],
                "Longitude":      row["Longitude"],
                "MGRS":           row["MGRS"],
                "AFSC_Code":      row["AFSC_Code"],
                "AFSC_Full_Name": row["AFSC_Full_Name"],
                "PDF_URL":        row["PDF_URL"],
                "Base_URL":       row["Base_URL"],
                "Aircraft":       "",
                "Base_Type":      "Active Duty",
            })
            rows_written += 1

    # ANG / Reserve rows
    for (bname, lat, lon, mgrs, wing_url, aircraft_list, btype) in ANG_BASES:
        if isinstance(aircraft_list, str):
            aircraft_list = [aircraft_list]
        ac_iter = aircraft_list if aircraft_list else [""]
        for ac in ac_iter:
            writer.writerow({
                "Base":           bname,
                "Latitude":       lat,
                "Longitude":      lon,
                "MGRS":           mgrs,
                "AFSC_Code":      "NONE",
                "AFSC_Full_Name": "NO AFSCS ASSIGNED",
                "PDF_URL":        "",
                "Base_URL":       wing_url,
                "Aircraft":       ac,
                "Base_Type":      btype,
            })
            rows_written += 1

print(f"Done!  USAF_Bases_Long_Format_v8.csv written.")
print(f"Total data rows: {rows_written:,}")
