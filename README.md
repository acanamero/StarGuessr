# Spectredle

A spectral classification game. Each round shows a real rectified spectrum (3900–6800 Å) from the
MELCHIORS library. Read the absorption lines and name the star's MK spectral type. If you miss, the
game explains the right answer using line-ratio criteria and equivalent widths measured on that spectrum.

**Play:** https://acanamero.github.io/Spectredle/

- 28 stars from O4 to M1, dwarfs (V) and supergiants (I)
- Exact answer: 100 pts; within one subtype: 70 pts with an explanation of why it isn't that type
- Expert mode also grades the luminosity class
- `Spectredle_study_sheet.xlsx`: criteria per spectral class, ratio summary, line list, suffixes and a self-quiz

Classification criteria follow the course notes *Atmósferas Estelares, Tema 1 – Líneas de diagnóstico /
Clases de luminosidad* by Sara Rodríguez Berlanas & Artemio Herrero, after Maíz Apellániz, Negueruela & Caballero (2024, arXiv:2410.07301) and
Gray & Corbally (2009). Spectra: MELCHIORS (Royer et al. 2024).

## Files

- `index.html` – the game (no build step)
- `spectra.js` – spectra resampled to 0.4 Å plus automatic line measurements
- `tools/build_data.py` – rebuilds `spectra.js` from a folder of `STAR_TYPE+CLASS_MelchiorsID.dat` files:
  `python3 tools/build_data.py <folder> spectra.js`
- `tools/build_xlsx.py` – rebuilds the study sheet
