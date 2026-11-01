"""Build spectra data + line measurements for StarGuessr.
Usage: python -I build_data.py <dat_dir> <out_js>"""
import sys, os, re, json, math
import numpy as np

LINES = {
 # key: (lambda0, half-window, label)
 "HeII4542": (4541.6, 3.5), "HeI4471": (4471.5, 3.5), "HeII4200": (4199.8, 3.5),
 "HeI4144": (4143.8, 3.0), "HeII4686": (4685.7, 3.5), "HeI4388": (4387.9, 3.0),
 "HeI4121": (4120.8, 2.5), "HeI4026": (4026.2, 3.5), "HeI4009": (4009.3, 2.5),
 "SiIV4089": (4088.9, 2.0), "SiIV4116": (4116.1, 2.0), "SiIII4552": (4552.6, 1.6),
 "SiII4130": (4129.5, 2.6), "MgII4481": (4481.2, 2.0), "NIII4640": (4640.0, 6.0),
 "NII3995": (3995.0, 1.6), "OII4416": (4415.0, 2.5), "NIV4058": (4057.8, 1.5),
 "CaIIK": (3933.7, 6.0), "Hdelta": (4101.7, 20.0), "Hgamma": (4340.5, 20.0),
 "Hbeta": (4861.3, 20.0), "Halpha": (6562.8, 20.0),
 "CaI4226": (4226.7, 1.2), "FeI4046": (4045.8, 1.2), "FeI4383": (4383.5, 1.2),
 "FeI4271": (4271.8, 1.2), "MnI4030": (4030.8, 1.5), "SrII4077": (4077.7, 0.9),
 "SrII4216": (4215.5, 0.9), "YII4376": (4374.9, 0.9), "FeI4144": (4143.9, 1.0),
 "CrI4254": (4254.3, 0.9), "FeI4250": (4250.8, 0.9), "CrI4290": (4289.7, 0.9),
 "FeI4326": (4325.8, 0.9), "Gband": (4305.0, 10.0), "Mgb": (5175.0, 12.0),
 "FeIITiII4173": (4175.0, 4.0), "FeIITiII4398": (4397.0, 3.5),
 "HdeltaCore": (4101.7, 2.5), "HgammaCore": (4340.5, 2.5), "CaI4226w": (4226.7, 1.2),
}

def load(path):
    a = np.loadtxt(path)
    w, f = a[:, 0], a[:, 1]
    ok = np.isfinite(f)
    return w[ok], f[ok]

def ew(w, f, l0, hw, cont=None):
    m = (w > l0 - hw) & (w < l0 + hw)
    if m.sum() < 3: return None
    if cont is None:
        side = ((w > l0 - hw - 12) & (w < l0 - hw)) | ((w > l0 + hw) & (w < l0 + hw + 12))
        cont = np.percentile(f[side], 90) if side.sum() > 5 else 1.0
        cont = max(min(cont, 1.05), 0.3)
    return float(np.trapezoid(1 - f[m] / cont, w[m]))

def parse(name):
    m = re.match(r"(.+?)_([OBAFGKM])(\d+(?:\.\d+)?)(I|II|III|IV|V)_Melchiors(\d+)", name)
    star, cls, sub, lc, mid = m.groups()
    return dict(star=star.replace("HD", "HD "), cls=cls, sub=float(sub), lc=lc, melchiors=mid)

def tio(w, f, head):
    # TiO bandhead depth: flux just blueward vs redward of head
    blue = np.median(f[(w > head - 12) & (w < head - 2)])
    red = np.median(f[(w > head + 2) & (w < head + 12)])
    return float(1 - red / blue)

stars = []
d = sys.argv[1]
for fn in sorted(os.listdir(d)):
    if not fn.endswith(".dat"): continue
    meta = parse(fn[:-4])
    w, f = load(os.path.join(d, fn))
    hot = meta["cls"] in "OBA"
    meas = {}
    for k, (l0, hw) in LINES.items():
        broad = k in ("Hdelta", "Hgamma", "Hbeta", "Halpha", "Gband", "Mgb", "CaIIK", "NIII4640")
        v = ew(w, f, l0, hw, cont=1.0 if (hot or broad) else None)
        meas[k] = None if v is None else round(v, 3)
    meas["TiO4954"] = round(tio(w, f, 4954.0), 3)
    meas["TiO5167"] = round(tio(w, f, 5167.0), 3)
    meas["TiO6159"] = round(tio(w, f, 6159.0), 3)
    # Balmer FWHM-ish width at 0.25 below continuum? use width where depth > half of max depth
    m = (w > 4861.3 - 40) & (w < 4861.3 + 40)
    dep = 1 - f[m]; half = dep.max() / 2
    meas["Hbeta_fwhm"] = round(float(np.ptp(w[m][dep > half])), 2)
    # resample to 0.4 A grid for display
    grid = np.arange(3900.0, 6800.0, 0.4)
    fb = np.interp(grid, w, f)
    stars.append(dict(**meta, file=fn, meas=meas,
                      w0=3900.0, dw=0.4, flux=[round(float(x), 3) for x in fb]))
    print(f"{fn[:30]:30s}", {k: meas[k] for k in ["HeII4542","HeI4471","HeII4686","SiIII4552","MgII4481","CaIIK","Hgamma","CaI4226","Gband","SrII4077","FeI4046","YII4376","FeI4383","TiO4954","Hbeta_fwhm"]})

with open(sys.argv[2], "w") as fo:
    fo.write("window.SPECTRA = " + json.dumps(stars, separators=(",", ":")) + ";\n")
print("wrote", len(stars))
