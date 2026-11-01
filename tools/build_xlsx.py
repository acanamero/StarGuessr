from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation

F = "Arial"
HEAD = PatternFill("solid", fgColor="1F2A5C")
INPUT = PatternFill("solid", fgColor="FFFF00")
thin = Side(style="thin", color="C9CEDF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
CLR = {"O": "9BB0FF", "B": "AABFFF", "A": "CAD7FF", "F": "F8F7FF", "G": "FFF4EA", "K": "FFD2A1", "M": "FFB56C"}

def sheet(wb, title, headers, rows, widths, first=False, color_col=None, src=None):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    r0 = 1
    if src:
        ws.cell(1, 1, src).font = Font(name=F, italic=True, size=9, color="555555")
        r0 = 2
    for j, h in enumerate(headers, 1):
        c = ws.cell(r0, j, h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BOX
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            c = ws.cell(i, j, v); c.font = Font(name=F, size=10, bold=(j == 1))
            c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = BOX
        if color_col is not None and row[color_col] in CLR:
            ws.cell(i, color_col + 1).fill = PatternFill("solid", fgColor=CLR[row[color_col]])
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(1, j).column_letter].width = w
    ws.freeze_panes = ws.cell(r0 + 1, 2)
    return ws

wb = Workbook()
SRC = "Source: course notes 'Atmósferas Estelares, Tema 1 – Líneas de diagnóstico / Clases de luminosidad' by Sara Rodríguez Berlanas & Artemio Herrero, after Maíz Apellániz, Negueruela & Caballero (2024) and Gray & Corbally (2009). Teff ranges are approximate textbook values, not from the notes."

# 1. Spectral types
sheet(wb, "Spectral types",
  ["Class", "Approx. Teff (K)", "Main features", "Other features", "Subtype diagnostics", "Trend toward later subtypes", "Luminosity-class criteria", "Watch out for"],
  [
   ["O", "> 30,000", "He II absorption (4200, 4542, 4686); H Balmer and He I present (He I grows with subtype).", "Very clean spectrum, few lines: H, He I, He II and highly ionized metals (N III–V, C III–IV, O II–III, Si IV). He II 4542 seen until ~B0.5, He II 4686 until ~B1.",
    "He II 4542 / He I 4471 (≈1 at O7). Earliest (O2–O3.5): N IV 4058 / N III 4634-40-42. Latest: He II 4200 / He I 4144 (≈1 at O9), Si III 4552 / He II 4542 (≈1 at O9.7). No He I before O4.",
    "He II 4542 / He I 4471 decreases; He I strengthens.",
    "Of phenomenon: He II 4686 goes from strong absorption (dwarfs) to emission (supergiants); N III 4634-40-42 emission grows with luminosity. Si IV 4089 / Si II 4116 (positive). Balmer width (negative).",
    "Rotation broadens lines and lowers depth: compare EW, not depth. Suffixes ((f)), (f), f, z describe the He II 4686 / N III behaviour."],
   ["B", "10,000 – 30,000", "He I absorption, no He II (may be very weak in early B). H lines stronger than in O.", "Ionized metals: Si II–IV, N II, C II, O II, Mg II. Ca II H&K noticeable from B3 and growing.",
    "(1) He I vs He II (He II gone by ~B1). (2) Si IV 4089 / Si III 4552 (≈1 at B0.7); Si III 4552 / Si II 4128-32 for mid–late B. (3) Mg II 4481 / He I 4471 (≈1 at B8).",
    "Mg II 4481 / He I 4471 increases; Si II strengthens relative to Si III; He I weakens after ~B2.",
    "Si IV 4116 / He I 4121; Si III 4552 / He I 4471 or 4387 (positive, metallicity dependent). Balmer width & EW decrease with luminosity. O II 4070/4416/4348, N II 3995 (positive). Hypergiants: Hβ P Cygni.",
    "Diagonal effect: B5 III and B8 Ib can have almost identical Balmer profiles – always use a second criterion (Si/He, metals). Watch C/N anomalies."],
   ["A", "7,500 – 10,000", "No He I (very weak in early A). Balmer at maximum (A2). Ca II H&K increasing, stronger than H in late A.", "Ionized metals Fe II, Mg II, Si II (max at A5). Neutral metals (Mg I) start. Ca II H blended with Hε.",
    "(1) Balmer: increases A0→A2, then decreases. (2) Ca II K 3934 grows strongly. (3) Metals: Ca I 4226, Fe I 4271, Mn I 4030; Si II 4128-32 > Mn I 4030-34 at A2, weaker afterwards. B8–A2: Mg II 4481 / He I 4471, Ca II K / He I 4026.",
    "Ca II K and metal lines increase; Balmer decreases after A2.",
    "Balmer width/EW (negative: narrower in supergiants), very marked in early A. Late A: Fe II/Ti II blends 4172-79 and 4395-4400, the '4500 forest' (positive).",
    "Interstellar Ca II K contamination. Many fast rotators and chemically peculiar stars (Am, Ap, λ Boo)."],
   ["F", "6,000 – 7,500", "Ca II very strong, H weakening, neutral metals appear.", "Later F: neutral metals dominate over ionized ones. G band (CH ~4300) prominent from F5.",
    "Metal lines vs Balmer: Fe I 4045 / Hδ, Ca I 4226 / Hγ, G band / Hγ (ratios ~1 at F–G transition). Ca I 4226, Fe I 4046 & 4383 are luminosity-insensitive.",
    "Metal / Balmer ratios increase; G band grows.",
    "Up to F5: Fe II/Ti II blends (4172-8, 4395-4400) vs luminosity-insensitive metals. Later: Sr II 4077 / 4216 vs Fe I (Sr II stronger in supergiants). Fe I 4172 / Ca I 4226 (F0–F8).",
    "Assumes solar metallicity. Fast rotators can look much hotter (e.g. 89 Tau F0 V)."],
   ["G", "5,200 – 6,000", "Ca II even stronger; Fe and other metals strong; H very weak.", "Neutral metals dominate. G band well developed. CH and CN bands.",
    "G band / Hγ (Hγ ≈ G band at G0), Fe I 4045 / Hδ, Fe I 4144 / Hδ, Ca I 4226. Low metallicity: Cr I 4254 / Fe I 4250, Cr I 4290 / Fe I 4326.",
    "G band and metals vs Balmer increase; Hγ inconspicuous by late G.",
    "Sr II 4077 & 4216 vs nearby Fe I; best in the blue: Y II 4376 / Fe I 4383 (increase with luminosity). CN bands deep in giants/supergiants (4215 discontinuity). G band: negative effect.",
    "Only real subtypes: G0, G2, G5, G8 (Keenan 1984)."],
   ["K", "3,700 – 5,200", "Ca II at maximum near K0. Strong metal lines; H very weak. CH and CN bands.", "Neutral metals dominate completely; continuum clearly red. Late K giants: TiO appears.",
    "Ca I 4226 (very prominent mid-K); Mg I b 5167-72-83 triplet (also luminosity-sensitive); Cr I / Fe I ratios.",
    "Ca I 4226 and Mg b increase; TiO begins in late K.",
    "Y II 4376 / Fe I 4383; Sr II 4077 / Fe I. CN deep in giants. MgH (4780, 5200): strong in mid-K dwarfs, weak in luminous stars (negative). TiO visible in mid-K giants, not dwarfs. Fe I 4215 / Ca I 4260 (K3–M).",
    "Only real subtypes K0–K5; K6–K9 are interpolations. K4.5 III and M1 III look very similar."],
   ["M", "2,400 – 3,700", "Strong TiO bands (4584, 4623, 4759, 4804, 4954 Å). Forest of metal and molecular lines.", "Ca II H&K present but not intense. Late types: VO bands. Blue continuum almost totally eroded.",
    "Progressive appearance of TiO bandheads; prefer TiO band ratios (strong bands saturate). TiO 4954 saturates from M3 (M0–3 vs later). Y II 4367 / Fe I 4383 valid until ~M5. VO from M5.",
    "TiO deepens; VO appears; Ca I 4226 very strong from M5.",
    "Ca I 4226: weak in giants/supergiants, very strong in dwarfs. TiO much stronger in giants than in dwarfs of the same type. Late-M luminosity class is hard to set.",
    "Supergiants barely reach M4.5 Ia. M9–M10 only in Mira/LPV variables. Use redder regions for late M."],
  ], [7, 14, 38, 38, 48, 30, 48, 36], first=True, color_col=0, src=SRC)

# 2. Summary table (slide 13)
sheet(wb, "Ratio summary",
  ["Type range", "Lines for spectral type", "Trend toward later types", "LC range", "Lines for luminosity class"],
  [
   ["O3 → O9", "He I 4471 / He II 4541", "Ratio increases", "O3 – O9", "He II 4686 and N III 4634-40-42; Balmer wings"],
   ["B0 → B1", "Si III 4552 / Si IV 4089; Mg II 4481 / He I 4471", "Ratios increase", "O9 – B2", "Si IV 4089-4116 / He I 4121; Balmer wings"],
   ["B2 → B8", "Si II 4128-30 / He I 4121; Mg II 4481 / He I 4471", "Ratios increase", "B0 – B5", "He I 4387 / O II 4416; Si III 4552 / He I 4387; N II 3995 / He I 4009"],
   ["B8 → A2", "Mg II 4481 / He I 4471; Ca II 3934 / He I 4026", "Ratios increase", "B3 – A5", "Balmer wings; N II 3995 / He I 4009"],
   ["A2 → F5", "Ca II 3934; Ca I 4226; Fe I 4271, 4383; Sr II 4077", "Intensity increases", "A3 – F0", "Balmer wings"],
   ["F2 → G5", "G band 4300 / Hγ 4340; Fe I 4045 / Hδ 4101; Ca I 4226 / Hγ 4340 (≈1 at the F–G transition)", "Ratios increase", "F0 – F8", "Fe I 4172 / Ca I 4226 (4172 stronger at LC I)"],
   ["", "", "", "F2 – K5", "Fe I 4046-64-72 / Sr II 4077; Ca I 4226 / Sr II 4077 (Sr II stronger at LC I)"],
   ["G5 → K0", "G band 4300, Ca I 4226; Fe I 4144 / Hδ 4101", "Intensity / ratio increases", "G5 – M", "Discontinuity near 4215 (CN, stronger at LC I); Y II 4376 / Fe I 4383 (increases for LC I, best for G–K); Mg I 5167-72-83 increases with LC"],
   ["K0 → K5", "Ca I 4226; Mg I 5167-72-83", "Intensity increases", "K3 – M", "Fe I 4215 / Ca I 4260 increasing; Fe I 5250 / 5259 increases with LC"],
   ["M", "Ca I 4226 / Fe I 4383 (until M5); TiO bands (0.63–0.84 µm); VO bands (0.73 µm)", "Bands deepen", "M", "Ca I 4226 (weak in giants, strong in dwarfs)"],
  ], [14, 46, 22, 12, 60], src="Source: 'Tabla resumen' slide (A. Herrero & A. Escorza) in the course notes. Wavelengths in Å.")

# 3. Line list
sheet(wb, "Line list",
  ["λ (Å)", "Species", "Group", "Strongest in", "What it is used for"],
  [[3933.7, "Ca II K", "Ionized metal", "late A – K", "Grows with subtype from B3; peaks ~K0. Watch interstellar contamination."],
   [3968.5, "Ca II H", "Ionized metal", "late A – K", "Blended with Hε 3970."],
   [3995.0, "N II", "Ionized metal", "B", "N II 3995 / He I 4009: luminosity (B0–A5)."],
   [4009.3, "He I", "He I", "B", "Luminosity ratio with N II 3995."],
   [4026.2, "He I (+He II)", "He I", "late O – B", "Ca II K / He I 4026 for B8–A2."],
   [4030.8, "Mn I", "Neutral metal", "A – F", "Grows through A; Si II 4128-32 vs Mn I 4030 at A2."],
   [4045.8, "Fe I", "Neutral metal", "F – K", "Fe I 4045 / Hδ (F2–G5); vs Sr II 4077 for luminosity."],
   [4057.8, "N IV", "Ionized metal", "O2 – O3.5 (emission)", "N IV 4058 / N III 4634-42 for the earliest O."],
   [4077.7, "Sr II", "Ionized metal", "F – K", "Luminosity: stronger in supergiants."],
   [4088.9, "Si IV", "Ionized metal", "O – B0", "Si IV 4089 / Si III 4552 (≈1 at B0.7); luminosity with He I 4121."],
   [4101.7, "Hδ", "H Balmer", "A2", "Balmer strength; Fe I 4045 / Hδ, Fe I 4144 / Hδ."],
   [4116.1, "Si IV", "Ionized metal", "O – B0", "Si IV 4116 / He I 4121: luminosity."],
   [4120.8, "He I", "He I", "B", "Reference for Si IV 4116 and Si II 4128-30."],
   [4128.1, "Si II (4128-31)", "Ionized metal", "mid-late B – A", "Si II / He I 4121 (B2–B8); Si III 4552 / Si II (mid-late B)."],
   [4143.8, "He I", "He I", "B", "He II 4200 / He I 4144 (≈1 at O9)."],
   [4144.0, "Fe I", "Neutral metal", "G – K", "Fe I 4144 / Hδ (G5–K0)."],
   [4172.0, "Fe II / Ti II blend (4172-79)", "Ionized metal", "A – F", "Luminosity (positive) in late A – F5."],
   [4199.8, "He II", "He II", "O", "He II 4200 / He I 4144 for late O."],
   [4215.5, "Sr II (+ CN 4215)", "Ionized metal", "F – K", "Luminosity; CN discontinuity near 4215 deeper at high LC."],
   [4226.7, "Ca I", "Neutral metal", "K – M dwarfs", "Temperature (A2 → M); weak in M giants, very strong in M dwarfs."],
   [4271.8, "Fe I", "Neutral metal", "A – K", "Metal-line strength from A2."],
   [4300.0, "G band (CH)", "Molecular", "F5 – K", "G band / Hγ (F2 → G5); negative luminosity effect."],
   [4340.5, "Hγ", "H Balmer", "A2", "Balmer width/EW for luminosity (B–A); vs G band and Ca I 4226."],
   [4374.9, "Y II (≈4376)", "Ionized metal", "G – K", "Y II 4376 / Fe I 4383: best blue luminosity criterion for G–K, valid to ~M5."],
   [4383.5, "Fe I", "Neutral metal", "F – M", "Reference for Y II; Ca I 4226 / Fe I 4383 in M."],
   [4387.9, "He I", "He I", "B", "Si III 4552 / He I 4387 and He I 4387 / O II 4416 (luminosity)."],
   [4395.0, "Fe II / Ti II blend (4395-4400)", "Ionized metal", "A – F", "Luminosity in late A – F5."],
   [4416.0, "O II", "Ionized metal", "early B", "Luminosity (positive)."],
   [4471.5, "He I", "He I", "B2", "Key reference: vs He II 4542 (O) and Mg II 4481 (B)."],
   [4481.2, "Mg II", "Ionized metal", "late B – A", "Mg II 4481 / He I 4471 (≈1 at B8)."],
   [4541.6, "He II", "He II", "O", "He II 4542 / He I 4471 (≈1 at O7)."],
   [4552.6, "Si III", "Ionized metal", "B0 – B2", "Si IV/Si III and Si III/Si II sequences; luminosity vs He I 4387/4471."],
   [4634.0, "N III (4634-40-42)", "Ionized metal", "O (emission)", "Emission grows with luminosity (Of)."],
   [4685.7, "He II", "He II", "O", "Absorption in dwarfs, emission in supergiants (Of)."],
   [4780.0, "MgH", "Molecular", "mid-K dwarfs", "Negative luminosity effect."],
   [4861.3, "Hβ", "H Balmer", "A2", "Luminosity (B–A); P Cygni in hypergiants; lost in metal forest in K."],
   [4954.0, "TiO bandhead", "Molecular", "M", "Saturates from M3; also seen in mid-K giants."],
   [5167.0, "Mg I b (5167-72-83)", "Neutral metal", "K", "Temperature (K0–K5), also luminosity-sensitive."],
   [6159.0, "TiO bandhead", "Molecular", "M", "Prominent in M and mid-K giants."],
   [6562.8, "Hα", "H Balmer", "A2", "Emission in Be stars and active M dwarfs."],
  ], [10, 28, 16, 20, 70], src="Rest air wavelengths, rounded. 'Strongest in' gives approximate peak or main usage range from the course notes.")

# 4. Suffixes
sheet(wb, "Suffixes",
  ["Suffix", "Range", "Meaning"],
  [[":", "All", "Uncertain classification (type or luminosity class)."], ["comp", "All", "Composite spectrum."],
   ["k", "All", "Interstellar absorption present."], ["p", "All", "Peculiar spectrum."], ["var", "All", "Variable line intensities or content."],
   ["w", "All", "Weak lines (metal poor)."], ["(n) / n / nn / nnn", "O–F", "Broadened lines by rotation: v sin i ~200 / 300 / 400 / 500 km/s (O stars)."],
   ["s", "All", "Very narrow (sharp) lines."], ["e / (e) / [e]", "All", "Emission in H lines / weak emission / forbidden Fe emission."],
   ["((f))", "O3.5–O8.5", "Weak N III 4634-40-42 emission, strong He II 4686 absorption."],
   ["(f)", "O4–O8.5", "Medium N III emission, neutral or weak He II 4686 absorption."],
   ["f", "O4–O8.5", "Strong N III emission, He II 4686 emission above continuum."],
   ["z", "O2–O8", "He II 4686 in absorption and stronger than both He I 4471 and He II 4542 (very young dwarfs)."],
   ["N / C", "O+B", "N enhanced, C deficient / C enhanced, N deficient."],
   ["He str / He wk", "B", "Exceptionally strong / weak He lines."], ["m", "A", "Abnormally strong metal lines (Am)."],
   ["λ Boo", "A+F", "λ Boo stars: metal-poor population I."], ["CN / CH / Ba / Fe", "G–M", "Abnormal band or line strengths, followed by a number."]],
  [20, 14, 80], src="Source: Table 1 of Maíz Apellániz, Negueruela & Caballero (2024), as reproduced in the course notes.")

# 5. Method
sheet(wb, "Method",
  ["Step", "What to do"],
  [["0", "Work on the rectified spectrum (continuum = 1). A badly placed continuum shifts every EW."],
   ["1", "First estimate of the class from the general look: He II? He I? Balmer maximum? Metal forest? Molecular bands?"],
   ["2", "Refine the subtype with the class-specific line ratios (see 'Spectral types' and 'Ratio summary'). Compare EW (area), never line depth."],
   ["3", "Evaluate the luminosity class with its own criteria (Balmer width, Of phenomenon, Sr II / Y II vs Fe I, Ca I 4226 in M)."],
   ["4", "Confirm with spectral libraries: compare with standards of ±1 subtype, widen to ±2 if needed."],
   ["5", "Use comparison stars without peculiarities (avoid 'var'). Do not compare stars of very different metallicity (e.g. Milky Way vs LMC/SMC)."],
   ["Tip", "Never rely on a single pair of lines if you can avoid it (diagonal effect in B/A Balmer lines)."]],
  [8, 110], src="Source: 'El método fino' and 'Comparación con estrellas estándares' slides.")

# 6. Self-quiz with formulas
ws = wb.create_sheet("Self-quiz")
ws["A1"] = "Type your answer in the yellow column (B). Column D checks it automatically; answers are in hidden column C (unhide to peek). Example: row 4 is already filled in."
ws["A1"].font = Font(name=F, italic=True, size=9, color="555555")
ws["A2"] = "Score"; ws["A2"].font = Font(name=F, bold=True)
quiz = [
 ("He II 4542 / He I 4471 ≈ 1. Which O subtype?", "O7"),
 ("Mg II 4481 / He I 4471 ≈ 1. Which B subtype?", "B8"),
 ("Si IV 4089 / Si III 4552 ≈ 1. Which subtype?", "B0.7"),
 ("He II 4200 / He I 4144 ≈ 1. Which subtype?", "O9"),
 ("Si III 4552 / He II 4542 ≈ 1. Which subtype?", "O9.7"),
 ("At which subtype do Balmer lines peak?", "A2"),
 ("From which subtype is the G band prominent?", "F5"),
 ("Near which subtype does Ca II H&K reach its maximum?", "K0"),
 ("Below which O subtype does He I disappear?", "O4"),
 ("TiO 4954 saturates from which M subtype?", "M3"),
 ("VO bands appear from which M subtype?", "M5"),
 ("He II 4686 in emission and strong N III emission: dwarf or supergiant? (V or I)", "I"),
 ("Very strong Ca I 4226 in an M star: dwarf or giant? (V or III)", "V"),
 ("Narrow, low-EW Balmer lines in a B star: V or I?", "I"),
 ("Strong Sr II 4077 relative to Fe I 4046 in a G star: V or I?", "I"),
 ("Strong MgH 4780 in a mid-K star: V or I?", "V"),
 ("Suffix for weak N III emission + strong He II 4686 absorption?", "((f))"),
 ("Suffix for lines broadened by rotation (~300 km/s)?", "n"),
 ("He I strong, no He II, Mg II 4481 weak, no Ca II K. Which class?", "B"),
 ("Metal forest, TiO bandheads, eroded blue continuum. Which class?", "M"),
]
for j, h in enumerate(["Question", "Your answer", "Answer", "Check"], 1):
    c = ws.cell(3, j, h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = HEAD; c.border = BOX
first, last = 4, 3 + len(quiz)
for i, (q, a) in enumerate(quiz, first):
    ws.cell(i, 1, q); ws.cell(i, 3, a)
    ws.cell(i, 2).fill = INPUT
    ws.cell(i, 4, f'=IF(TRIM(B{i})="","",IF(UPPER(TRIM(B{i}))=UPPER(C{i}),"Correct","Try again"))')
    for j in range(1, 5):
        c = ws.cell(i, j); c.font = Font(name=F, size=10); c.border = BOX; c.alignment = Alignment(wrap_text=True, vertical="top")
ws.cell(first, 2, "O7")  # example row
ws["B2"] = f'=COUNTIF(D{first}:D{last},"Correct")&" / {len(quiz)}"'
ws["B2"].font = Font(name=F, bold=True)
ws.column_dimensions["A"].width = 70; ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 12; ws.column_dimensions["D"].width = 14
ws.column_dimensions["C"].hidden = True
rng = f"D{first}:D{last}"
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'D{first}="Correct"'], fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'D{first}="Try again"'], fill=PatternFill("solid", fgColor="FFC7CE")))
ws.freeze_panes = "A4"

wb.save("/home/user/spectredle/Spectredle_study_sheet.xlsx")
print("saved")
