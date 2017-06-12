#!/usr/bin/python3
import subprocess


import os.path

files=[
"image_dama.jpg",
"RAW_CANON_300D.CRW",
"RAW_CANON_300D.jpg",
"RAW_CANON_5D_ARGB.CR2",
"RAW_FUJI_S5000.RAF",
"RAW_MINOLTA_A1.MRW",
"RAW_NIKON_D70.NEF",
"RAW_OLYMPUS_SP500UZ.ORF",
"RAW_PENTAX_K10D_SRGB.PEF",
"RAW_SIGMA_SD10.X3F",
"RAW_SONY_A100.ARW",
"DSCF1390_alt1526.9m.JPG",
]

for file in files:
    print("Doing",file)
    fh=open("./fixture/exiftool/"+file+".xml","r")
    out=fh.read()
    fh.close()
    print(out)
