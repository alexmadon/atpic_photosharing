#!/usr/bin/python3
import subprocess


import os.path

files=[
"./fixture/image_dama.jpg",
"./fixture/raw/RAW_CANON_300D.CRW",
"./fixture/raw/RAW_CANON_300D.jpg",
"./fixture/raw/RAW_CANON_5D_ARGB.CR2",
"./fixture/raw/RAW_FUJI_S5000.RAF",
"./fixture/raw/RAW_MINOLTA_A1.MRW",
"./fixture/raw/RAW_NIKON_D70.NEF",
"./fixture/raw/RAW_OLYMPUS_SP500UZ.ORF",
"./fixture/raw/RAW_PENTAX_K10D_SRGB.PEF",
"./fixture/raw/RAW_SIGMA_SD10.X3F",
"./fixture/raw/RAW_SONY_A100.ARW",
"./fixture/DSCF1390_alt1526.9m.JPG",
]

for file in files:

    p1=subprocess.Popen(["exiftool","-X","-l",file],stdout=subprocess.PIPE)
    out=p1.communicate()[0]
    # print("p1 %s" % p1)
    print(out)
    fh=open("./fixture/exiftool/"+os.path.basename(file)+".xml","w")
    fh.write(out.decode('utf8'))
    fh.close()
