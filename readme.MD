# Repository for Coptic-Arabic Alignment

This repo is provided as-is for anyone who would like to use the alignment code or check my results. At this point, I don't even remember how all of it works. I would have to go through it myself. But it is all here and should be fairly straightforward to use.

The main purpose of sharing it here is to demonstrate that the computational alignment operates without interference and produces the results shown in my papers. The alignment and the evidence leads, analysis comes after. All the results should be confirmed by repeating the analysis.

## Data Sources

The input is in the `parallel_texts.csv` file in the root. These data are taken from:

* [Casanova, Paul (1901). Un texte arabe transcrit en caractères coptes. *Le Bulletin de l’Institut français d’archéologie orientale* 1:1-20.](http://www.ifao.egnet.net/bifao/1/)
* [Burmester, OHE (1965-1966). Further leaves from the Arabic MS. in Coptic script of the Apophthegmata Patrum. *Bulletin de la Société d’archéologie copte* 18:51-64.](https://copticsounds.files.wordpress.com/2010/01/furtherleavesfromthearabicmsincopticscriptoftheapophthehmatapatrum.pdf)

Additional data found in Sobhy 1926 have not yet been added due to time constraints. Updated readings of the Arabic found in Blau 1979 have not yet been included. This will change in future iterations.

One minor issue to note is that Coptic <ⲟⲩ> has been replaced with the character <ȣ>. This was done to ensure that these will be treated as a single grapheme by the analysis. The results demonstrate the validity of this approach. Otherwise, <ⲟ> and <ⲩ> are separately correlated with various Arabic phonemes.

## Results

The code will create output files in the `output` directory.

Viewable results in a formatted Excel spreadsheet are in the file: `Coptic-Arabic Text Alignment Results.xlsx`.