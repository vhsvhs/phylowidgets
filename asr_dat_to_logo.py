#
# Convert an ASR *.dat file into a sequence motif and then render the motif
# using MEME's ceqlogo software.
#


import sys, os
from Bio import Motif
from Bio.Alphabet import IUPAC
alphabet = IUPAC.ExtendedIUPACProtein.letters

from argParser import *
ap = ArgParser(sys.argv)

def getprobs(inpath):
    fin = open(inpath, "r")
    lines = fin.readlines()
    fin.close()

    site_states_probs = {}
    for l in lines:
        tokens = l.split()
        site = int(tokens[0])
        site_states_probs[ site ] = {}
        i = 1
        while i < tokens.__len__():
            s = tokens[i]
            foundgap = False
            if s == "-":
                p = 0.0
                foundgap = True
            else:
                p = float(tokens[i+1])
            if p > 1.0:
                p = 0.0
                foundgap = True
            site_states_probs[site][s] = p
            i += 2
            if foundgap:
                i = tokens.__len__() # stop early
    return site_states_probs

def print_ml_sequence(site_states_probs):
    mlseq = ""
    sites = site_states_probs.keys()
    sites.sort()
    for site in sites:
        maxp = 0.0
        maxc = ""
        for c in site_states_probs[site]:
            #print site_states_probs[site][c]
            if site_states_probs[site][c] > maxp:
                maxp = site_states_probs[site][c]
                maxc = c
        if maxc != "-":
            mlseq += maxc
    print mlseq
        

def fill_missing_data(site_states_probs):
    for i in site_states_probs.keys():
        for a in alphabet:
            if False == site_states_probs[i].__contains__(a):
                site_states_probs[i][a] = 0.000
    return site_states_probs

#
#
#   
def write_pfm_file(site_states_probs, outpath, startsite, stopsite):
    if os.path.exists(outpath):
        os.system("rm " + outpath)
    fd = open(outpath, "w")
    for c in alphabet:
        line = ""
        for i in range(startsite, stopsite):  
            if site_states_probs.__contains__(i):
                line += int(site_states_probs[i][c]).__str__() + " "
        fd.write(line + "\n")
    fd.close()    

################################################
#
#
def generate_eps(nsites):
    epsdata = []
    epsdata.append("%!PS-Adobe-3.0 EPSF-3.0\n")
    epsdata.append("%%Title: Sequence Logo :\n")
    epsdata.append("%%Creator:\n")
    epsdata.append("%%CreationDate:\n")
    boundingwidth = 50 + nsites*15.2
    epsdata.append("%%BoundingBox:   0  0  " + int(boundingwidth).__str__() + "  141\n")
    epsdata.append("%%Pages: 0\n")
    epsdata.append("%%DocumentFonts:\n")
    epsdata.append("%%EndComments\n")
    epsdata.append("\n")
    epsdata.append("% * PROTEIN ALIGNMENT\n")
    epsdata.append("% ---- CONSTANTS ----\n")
    epsdata.append("/cmfactor 72 2.54 div def % defines points -> cm conversion\n")
    epsdata.append("/cm {cmfactor mul} bind def % defines centimeters\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% ---- VARIABLES ----\n")
    epsdata.append("\n")
    epsdata.append("/black [0 0 0] def\n")
    epsdata.append("/red [0.8 0 0] def\n")
    epsdata.append("/green [0 0.8 0] def\n")
    epsdata.append("/blue [0 0 0.8] def\n")
    epsdata.append("/yellow [1 0.7 1.0] def\n")
    epsdata.append("/purple [0.8 0 0.8] def\n")
    epsdata.append("/orange [1 0.7 0] def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/logoWidth 18 cm def\n")
    epsdata.append("/logoHeight 3 cm def\n")
    epsdata.append("/logoTitle () def\n")
    epsdata.append("\n")
    epsdata.append("/yaxis true def\n")
    epsdata.append("/yaxisLabel () def\n")
    epsdata.append("/yaxisBits  1.0 def % posterior probabilities\n")
    epsdata.append("/yaxisTicBits 1 def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/xaxis true def\n")
    epsdata.append("/xaxisLabel () def\n")
    epsdata.append("/showEnds (p) def % d: DNA, p: PROTEIN, -: none\n")
    epsdata.append("\n")
    epsdata.append("/showFineprint true def\n")
    epsdata.append("/fineprint (Lazarus -- markov.uoregon.edu/software/lazarus; Weblogo -- weblogo.berkeley.edu) def\n")
    epsdata.append("\n")
    epsdata.append("/charsPerLine 30 def\n")
    epsdata.append("/logoLines 1 def\n")
    epsdata.append("\n")
    epsdata.append("/showingBox (n) def    %n s f\n")
    epsdata.append("/shrinking false def\n")
    epsdata.append("/shrink  0.5 def\n")
    epsdata.append("/outline false def\n")
    epsdata.append("\n")
    epsdata.append("/IbeamFraction  1 def\n")
    epsdata.append("/IbeamGray      0.50 def\n")
    epsdata.append("/IbeamLineWidth 0.5 def\n")
    epsdata.append("\n")
    epsdata.append("/fontsize       12 def\n")
    epsdata.append("/titleFontsize  14 def\n")
    epsdata.append("/smallFontsize   6 def\n")
    epsdata.append("\n")
    epsdata.append("/defaultColor black def\n")
    epsdata.append("\n")
    epsdata.append("% Standard Amino Acid colors\n")
    epsdata.append("/colorDict <<\n")
    epsdata.append("(G)  black\n")
    epsdata.append("(S)  black\n")
    epsdata.append("(T)  black\n")
    epsdata.append("(Y)  black\n")
    epsdata.append("(C)  black\n")
    epsdata.append("(N)  black\n")
    epsdata.append("(Q)  black\n")
    epsdata.append("(K)  black\n")
    epsdata.append("(R)  black\n")
    epsdata.append("(H)  black\n")
    epsdata.append("(D)  black\n")
    epsdata.append("(E)  black\n")
    epsdata.append("(P)  black\n")
    epsdata.append("(A)  black\n")
    epsdata.append("(W)  black\n")
    epsdata.append("(F)  black\n")
    epsdata.append("(L)  black\n")
    epsdata.append("(I)  black\n")
    epsdata.append("(M)  black\n")
    epsdata.append("(V)  black\n")
    epsdata.append("\n")
    epsdata.append(">> def\n")
    epsdata.append("\n")
    epsdata.append("% Standard DNA/RNA color scheme\n")
    epsdata.append("% /colorDict <<\n")
    epsdata.append("%   (G)  black\n")
    epsdata.append("%   (T)  black\n")
    epsdata.append("%   (C)  black\n")
    epsdata.append("%   (A)  black\n")
    epsdata.append("%   (U)  black\n")
    epsdata.append("% >> def\n")
    epsdata.append("\n")
    epsdata.append("% Standard Amino Acid colors\n")
    epsdata.append("%/colorDict <<\n")
    epsdata.append("%  (G)  black\n")
    epsdata.append("%  (S)  black\n")
    epsdata.append("%  (T)  black\n")
    epsdata.append("%  (Y)  black\n")
    epsdata.append("%  (C)  black\n")
    epsdata.append("%  (N)  black\n")
    epsdata.append("%  (Q)  black\n")
    epsdata.append("%  (K)  black\n")
    epsdata.append("%  (R)  black\n")
    epsdata.append("%  (H)  black\n")
    epsdata.append("%  (D)  black\n")
    epsdata.append("%  (E)  black\n")
    epsdata.append("%  (P)  black\n")
    epsdata.append("%  (A)  black\n")
    epsdata.append("%  (W)  black\n")
    epsdata.append("%  (F)  black\n")
    epsdata.append("%  (L)  black\n")
    epsdata.append("%  (I)  black\n")
    epsdata.append("%  (M)  black\n")
    epsdata.append("%  (V)  black\n")
    epsdata.append("%>> def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% ---- DERIVED PARAMETERS ----\n")
    epsdata.append("\n")
    epsdata.append("/leftMargin\n")
    epsdata.append("fontsize 3.5 mul\n")
    epsdata.append("\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/bottomMargin\n")
    epsdata.append("fontsize 0.75 mul\n")
    epsdata.append("\n")
    epsdata.append("% Add extra room for axis\n")
    epsdata.append("xaxis {fontsize 1.75 mul add } if\n")
    epsdata.append("xaxisLabel () eq {} {fontsize 0.75 mul add} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/topMargin\n")
    epsdata.append("logoTitle () eq { 10 }{titleFontsize 4 add} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/rightMargin\n")
    epsdata.append("%Add extra room if showing ends\n")
    epsdata.append("showEnds (-) eq { fontsize}{fontsize 1.5 mul} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/yaxisHeight\n")
    epsdata.append("logoHeight\n")
    epsdata.append("bottomMargin sub\n")
    epsdata.append("topMargin sub\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/ticWidth fontsize 2 div def\n")
    epsdata.append("\n")
    epsdata.append("/pointsPerBit yaxisHeight yaxisBits div  def\n")
    epsdata.append("\n")
    epsdata.append("/isBoxed\n")
    epsdata.append("showingBox (s) eq\n")
    epsdata.append("showingBox (f) eq or {\n")
    epsdata.append("true\n")
    epsdata.append("} {\n")
    epsdata.append("false\n")
    epsdata.append("} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/stackMargin 1.0 def\n")
    epsdata.append("\n")
    epsdata.append("% Do not add space aroung characters if characters are boxed\n")
    epsdata.append("/charRightMargin\n")
    epsdata.append("isBoxed { 0.0 } {stackMargin} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/charTopMargin\n")
    epsdata.append("isBoxed { 0.0 } {stackMargin} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/charWidth\n")
    epsdata.append("logoWidth\n")
    epsdata.append("leftMargin sub\n")
    epsdata.append("rightMargin sub\n")
    epsdata.append("charsPerLine div\n")
    epsdata.append("charRightMargin sub\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/charWidth4 charWidth 4 div def\n")
    epsdata.append("/charWidth2 charWidth 2 div def\n")
    epsdata.append("\n")
    epsdata.append("/stackWidth\n")
    epsdata.append("charWidth charRightMargin add\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/numberFontsize\n")
    epsdata.append("fontsize charWidth lt {fontsize}{charWidth} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("% movements to place 5'/N and 3'/C symbols\n")
    epsdata.append("/leftEndDeltaX  fontsize neg         def\n")
    epsdata.append("/leftEndDeltaY  fontsize 1.5 mul neg def\n")
    epsdata.append("/rightEndDeltaX fontsize 0.25 mul     def\n")
    epsdata.append("/rightEndDeltaY leftEndDeltaY        def\n")
    epsdata.append("\n")
    epsdata.append("% Outline width is proporional to charWidth,\n")
    epsdata.append("% but no less that 1 point\n")
    epsdata.append("/outlinewidth\n")
    epsdata.append("charWidth 32 div dup 1 gt  {}{pop 1} ifelse\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% ---- PROCEDURES ----\n")
    epsdata.append("\n")
    epsdata.append("/StartLogo {\n")
    epsdata.append("% Save state\n")
    epsdata.append("save\n")
    epsdata.append("gsave\n")
    epsdata.append("\n")
    epsdata.append("% Print Logo Title, top center\n")
    epsdata.append("gsave\n")
    epsdata.append("SetTitleFont\n")
    epsdata.append("\n")
    epsdata.append("logoWidth 2 div\n")
    epsdata.append("logoTitle\n")
    epsdata.append("stringwidth pop 2 div sub\n")
    epsdata.append("logoHeight logoLines mul\n")
    epsdata.append("titleFontsize sub\n")
    epsdata.append("moveto\n")
    epsdata.append("\n")
    epsdata.append("logoTitle\n")
    epsdata.append("show\n")
    epsdata.append("grestore\n")
    epsdata.append("\n")
    epsdata.append("% Print X-axis label, bottom center\n")
    epsdata.append("gsave\n")
    epsdata.append("SetStringFont\n")
    epsdata.append("\n")
    epsdata.append("logoWidth 2 div\n")
    epsdata.append("xaxisLabel stringwidth pop 2 div sub\n")
    epsdata.append("fontsize 3 div\n")
    epsdata.append("moveto\n")
    epsdata.append("\n")
    epsdata.append("xaxisLabel\n")
    epsdata.append("show\n")
    epsdata.append("grestore\n")
    epsdata.append("\n")
    epsdata.append("% Show Fine Print\n")
    epsdata.append("showFineprint {\n")
    epsdata.append("gsave\n")
    epsdata.append("SetSmallFont\n")
    epsdata.append("logoWidth\n")
    epsdata.append("fineprint stringwidth pop sub\n")
    epsdata.append("smallFontsize sub\n")
    epsdata.append("smallFontsize 3 div\n")
    epsdata.append("moveto\n")
    epsdata.append("\n")
    epsdata.append("fineprint show\n")
    epsdata.append("grestore\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("% Move to lower left corner of last line, first stack\n")
    epsdata.append("leftMargin bottomMargin translate\n")
    epsdata.append("\n")
    epsdata.append("% Move above first line ready for StartLine\n")
    epsdata.append("0 logoLines logoHeight mul translate\n")
    epsdata.append("\n")
    epsdata.append("SetLogoFont\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("/EndLogo {\n")
    epsdata.append("grestore\n")
    epsdata.append("showpage\n")
    epsdata.append("restore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/StartLine{\n")
    epsdata.append("% move down to the bottom of the line:\n")
    epsdata.append("0 logoHeight neg translate\n")
    epsdata.append("\n")
    epsdata.append("gsave\n")
    epsdata.append("yaxis { MakeYaxis } if\n")
    epsdata.append("xaxis { ShowLeftEnd } if\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("/EndLine{\n")
    epsdata.append("xaxis { ShowRightEnd } if\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/MakeYaxis {\n")
    epsdata.append("gsave\n")
    epsdata.append("stackMargin neg 0 translate\n")
    epsdata.append("ShowYaxisBar\n")
    epsdata.append("ShowYaxisLabel\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowYaxisBar {\n")
    epsdata.append("gsave\n")
    epsdata.append("SetStringFont\n")
    epsdata.append("\n")
    epsdata.append("/str 10 string def % string to hold number\n")
    epsdata.append("/smallgap stackMargin 2 div def\n")
    epsdata.append("\n")
    epsdata.append("% Draw first tic and bar\n")
    epsdata.append("gsave\n")
    epsdata.append("ticWidth neg 0 moveto\n")
    epsdata.append("ticWidth 0 rlineto\n")
    epsdata.append("0 yaxisHeight rlineto\n")
    epsdata.append("stroke\n")
    epsdata.append("grestore\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% Draw the tics\n")
    epsdata.append("% initial increment limit proc for\n")
    epsdata.append("0 yaxisTicBits yaxisBits abs %cvi\n")
    epsdata.append("{/loopnumber exch def\n")
    epsdata.append("\n")
    epsdata.append("% convert the number coming from the loop to a string\n")
    epsdata.append("% and find its width\n")
    epsdata.append("loopnumber 10 str cvrs\n")
    epsdata.append("/stringnumber exch def % string representing the number\n")
    epsdata.append("\n")
    epsdata.append("stringnumber stringwidth pop\n")
    epsdata.append("/numberwidth exch def % width of number to show\n")
    epsdata.append("\n")
    epsdata.append("/halfnumberheight\n")
    epsdata.append("stringnumber CharBoxHeight 2 div\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("numberwidth % move back width of number\n")
    epsdata.append("neg loopnumber pointsPerBit mul % shift on y axis\n")
    epsdata.append("halfnumberheight sub % down half the digit\n")
    epsdata.append("\n")
    epsdata.append("moveto % move back the width of the string\n")
    epsdata.append("\n")
    epsdata.append("ticWidth neg smallgap sub % Move back a bit more\n")
    epsdata.append("0 rmoveto % move back the width of the tic\n")
    epsdata.append("\n")
    epsdata.append("stringnumber show\n")
    epsdata.append("smallgap 0 rmoveto % Make a small gap\n")
    epsdata.append("\n")
    epsdata.append("% now show the tic mark\n")
    epsdata.append("0 halfnumberheight rmoveto % shift up again\n")
    epsdata.append("ticWidth 0 rlineto\n")
    epsdata.append("stroke\n")
    epsdata.append("} for\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("/ShowYaxisLabel {\n")
    epsdata.append("gsave\n")
    epsdata.append("SetStringFont\n")
    epsdata.append("\n")
    epsdata.append("% How far we move left depends on the size of\n")
    epsdata.append("% the tic labels.\n")
    epsdata.append("/str 10 string def % string to hold number\n")
    epsdata.append("yaxisBits yaxisTicBits div cvi yaxisTicBits mul\n")
    epsdata.append("str cvs stringwidth pop\n")
    epsdata.append("ticWidth 1.5 mul  add neg\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("yaxisHeight\n")
    epsdata.append("yaxisLabel stringwidth pop\n")
    epsdata.append("sub 2 div\n")
    epsdata.append("\n")
    epsdata.append("translate\n")
    epsdata.append("90 rotate\n")
    epsdata.append("0 0 moveto\n")
    epsdata.append("yaxisLabel show\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/StartStack {  % <stackNumber> startstack\n")
    epsdata.append("xaxis {MakeNumber}{pop} ifelse\n")
    epsdata.append("gsave\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("/EndStack {\n")
    epsdata.append("grestore\n")
    epsdata.append("stackWidth 0 translate\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% Draw a character whose height is proportional to symbol bits\n")
    epsdata.append("/MakeSymbol{ % charbits character MakeSymbol\n")
    epsdata.append("gsave\n")
    epsdata.append("/char exch def\n")
    epsdata.append("/bits exch def\n")
    epsdata.append("\n")
    epsdata.append("/bitsHeight\n")
    epsdata.append("bits pointsPerBit mul\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("/charHeight\n")
    epsdata.append("bitsHeight charTopMargin sub\n")
    epsdata.append("dup\n")
    epsdata.append("0.0 gt {}{pop 0.0} ifelse % if neg replace with zero\n")
    epsdata.append("def\n")
    epsdata.append("\n")
    epsdata.append("charHeight 0.0 gt {\n")
    epsdata.append("char SetColor\n")
    epsdata.append("charWidth charHeight char ShowChar\n")
    epsdata.append("\n")
    epsdata.append("showingBox (s) eq { % Unfilled box\n")
    epsdata.append("0 0 charWidth charHeight false ShowBox\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("showingBox (f) eq { % Filled box\n")
    epsdata.append("0 0 charWidth charHeight true ShowBox\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("grestore\n")
    epsdata.append("\n")
    epsdata.append("0 bitsHeight translate\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowChar { % <width> <height> <char> ShowChar\n")
    epsdata.append("gsave\n")
    epsdata.append("/tc exch def    % The character\n")
    epsdata.append("/ysize exch def % the y size of the character\n")
    epsdata.append("/xsize exch def % the x size of the character\n")
    epsdata.append("\n")
    epsdata.append("/xmulfactor 1 def\n")
    epsdata.append("/ymulfactor 1 def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% if ysize is negative, make everything upside down!\n")
    epsdata.append("ysize 0 lt {\n")
    epsdata.append("% put ysize normal in this orientation\n")
    epsdata.append("/ysize ysize abs def\n")
    epsdata.append("xsize ysize translate\n")
    epsdata.append("180 rotate\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("shrinking {\n")
    epsdata.append("xsize 1 shrink sub 2 div mul\n")
    epsdata.append("ysize 1 shrink sub 2 div mul translate\n")
    epsdata.append("\n")
    epsdata.append("shrink shrink scale\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("% Calculate the font scaling factors\n")
    epsdata.append("% Loop twice to catch small correction due to first scaling\n")
    epsdata.append("2 {\n")
    epsdata.append("gsave\n")
    epsdata.append("xmulfactor ymulfactor scale\n")
    epsdata.append("\n")
    epsdata.append("ysize % desired size of character in points\n")
    epsdata.append("tc CharBoxHeight\n")
    epsdata.append("dup 0.0 ne {\n")
    epsdata.append("div % factor by which to scale up the character\n")
    epsdata.append("/ymulfactor exch def\n")
    epsdata.append("} % end if\n")
    epsdata.append("{pop pop}\n")
    epsdata.append("ifelse\n")
    epsdata.append("\n")
    epsdata.append("xsize % desired size of character in points\n")
    epsdata.append("tc CharBoxWidth\n")
    epsdata.append("dup 0.0 ne {\n")
    epsdata.append("div % factor by which to scale up the character\n")
    epsdata.append("/xmulfactor exch def\n")
    epsdata.append("} % end if\n")
    epsdata.append("{pop pop}\n")
    epsdata.append("ifelse\n")
    epsdata.append("grestore\n")
    epsdata.append("} repeat\n")
    epsdata.append("\n")
    epsdata.append("% Adjust horizontal position if the symbol is an I\n")
    epsdata.append("tc (I) eq {\n")
    epsdata.append("charWidth 2 div % half of requested character width\n")
    epsdata.append("tc CharBoxWidth 2 div % half of the actual character\n")
    epsdata.append("sub 0 translate\n")
    epsdata.append("% Avoid x scaling for I\n")
    epsdata.append("/xmulfactor 1 def\n")
    epsdata.append("} if\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% ---- Finally, draw the character\n")
    epsdata.append("\n")
    epsdata.append("newpath\n")
    epsdata.append("xmulfactor ymulfactor scale\n")
    epsdata.append("\n")
    epsdata.append("% Move lower left corner of character to start point\n")
    epsdata.append("tc CharBox pop pop % llx lly : Lower left corner\n")
    epsdata.append("exch neg exch neg\n")
    epsdata.append("moveto\n")
    epsdata.append("\n")
    epsdata.append("outline {  % outline characters:\n")
    epsdata.append("outlinewidth setlinewidth\n")
    epsdata.append("tc true charpath\n")
    epsdata.append("gsave 1 setgray fill grestore\n")
    epsdata.append("clip stroke\n")
    epsdata.append("} { % regular characters\n")
    epsdata.append("tc show\n")
    epsdata.append("} ifelse\n")
    epsdata.append("\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowBox { % x1 y1 x2 y2 filled ShowBox\n")
    epsdata.append("gsave\n")
    epsdata.append("/filled exch def\n")
    epsdata.append("/y2 exch def\n")
    epsdata.append("/x2 exch def\n")
    epsdata.append("/y1 exch def\n")
    epsdata.append("/x1 exch def\n")
    epsdata.append("newpath\n")
    epsdata.append("x1 y1 moveto\n")
    epsdata.append("x2 y1 lineto\n")
    epsdata.append("x2 y2 lineto\n")
    epsdata.append("x1 y2 lineto\n")
    epsdata.append("closepath\n")
    epsdata.append("\n")
    epsdata.append("clip\n")
    epsdata.append("\n")
    epsdata.append("filled {\n")
    epsdata.append("fill\n")
    epsdata.append("}{\n")
    epsdata.append("0 setgray stroke\n")
    epsdata.append("} ifelse\n")
    epsdata.append("\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/MakeNumber { % number MakeNumber\n")
    epsdata.append("gsave\n")
    epsdata.append("SetNumberFont\n")
    epsdata.append("stackWidth 0 translate\n")
    epsdata.append("90 rotate % rotate so the number fits\n")
    epsdata.append("dup stringwidth pop % find the length of the number\n")
    epsdata.append("neg % prepare for move\n")
    epsdata.append("stackMargin sub % Move back a bit\n")
    epsdata.append("charWidth (0) CharBoxHeight % height of numbers\n")
    epsdata.append("sub 2 div %\n")
    epsdata.append("moveto % move back to provide space\n")
    epsdata.append("show\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/Ibeam{ % heightInBits Ibeam\n")
    epsdata.append("gsave\n")
    epsdata.append("% Make an Ibeam of twice the given height in bits\n")
    epsdata.append("/height exch  pointsPerBit mul def\n")
    epsdata.append("/heightDRAW height IbeamFraction mul def\n")
    epsdata.append("\n")
    epsdata.append("IbeamLineWidth setlinewidth\n")
    epsdata.append("IbeamGray setgray\n")
    epsdata.append("\n")
    epsdata.append("charWidth2 height neg translate\n")
    epsdata.append("ShowIbar\n")
    epsdata.append("newpath\n")
    epsdata.append("0 0 moveto\n")
    epsdata.append("0 heightDRAW rlineto\n")
    epsdata.append("stroke\n")
    epsdata.append("newpath\n")
    epsdata.append("0 height moveto\n")
    epsdata.append("0 height rmoveto\n")
    epsdata.append("currentpoint translate\n")
    epsdata.append("ShowIbar\n")
    epsdata.append("newpath\n")
    epsdata.append("0 0 moveto\n")
    epsdata.append("0 heightDRAW neg rlineto\n")
    epsdata.append("currentpoint translate\n")
    epsdata.append("stroke\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowIbar { % make a horizontal bar\n")
    epsdata.append("gsave\n")
    epsdata.append("newpath\n")
    epsdata.append("charWidth4 neg 0 moveto\n")
    epsdata.append("charWidth4 0 lineto\n")
    epsdata.append("stroke\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowLeftEnd {\n")
    epsdata.append("gsave\n")
    epsdata.append("SetStringFont\n")
    epsdata.append("leftEndDeltaX leftEndDeltaY moveto\n")
    epsdata.append("showEnds (d) eq {(5) show ShowPrime} if\n")
    epsdata.append("showEnds (p) eq {(N) show} if\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowRightEnd {\n")
    epsdata.append("gsave\n")
    epsdata.append("SetStringFont\n")
    epsdata.append("rightEndDeltaX rightEndDeltaY moveto\n")
    epsdata.append("showEnds (d) eq {(3) show ShowPrime} if\n")
    epsdata.append("showEnds (p) eq {(C) show} if\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/ShowPrime {\n")
    epsdata.append("gsave\n")
    epsdata.append("SetPrimeFont\n")
    epsdata.append("(\242) show\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("/SetColor{ % <char> SetColor\n")
    epsdata.append("dup colorDict exch known {\n")
    epsdata.append("colorDict exch get aload pop setrgbcolor\n")
    epsdata.append("} {\n")
    epsdata.append("pop\n")
    epsdata.append("defaultColor aload pop setrgbcolor\n")
    epsdata.append("} ifelse\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("% define fonts\n")
    epsdata.append("/SetTitleFont {/Times-Bold findfont titleFontsize scalefont setfont} bind def\n")
    epsdata.append("/SetLogoFont  {/Helvetica-Narrow-Bold findfont charWidth  scalefont setfont} bind def\n")
    epsdata.append("/SetStringFont{/Helvetica-Bold findfont fontsize scalefont setfont} bind def\n")
    epsdata.append("/SetPrimeFont {/Symbol findfont fontsize scalefont setfont} bind def\n")
    epsdata.append("/SetSmallFont {/Helvetica findfont smallFontsize scalefont setfont} bind def\n")
    epsdata.append("\n")
    epsdata.append("/SetNumberFont {\n")
    epsdata.append("/Helvetica-Bold findfont\n")
    epsdata.append("numberFontsize\n")
    epsdata.append("scalefont\n")
    epsdata.append("setfont\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("%Take a single character and return the bounding box\n")
    epsdata.append("/CharBox { % <char> CharBox <lx> <ly> <ux> <uy>\n")
    epsdata.append("gsave\n")
    epsdata.append("newpath\n")
    epsdata.append("0 0 moveto\n")
    epsdata.append("% take the character off the stack and use it here:\n")
    epsdata.append("true charpath\n")
    epsdata.append("flattenpath\n")
    epsdata.append("pathbbox % compute bounding box of 1 pt. char => lx ly ux uy\n")
    epsdata.append("% the path is here, but toss it away ...\n")
    epsdata.append("grestore\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% The height of a characters bounding box\n")
    epsdata.append("/CharBoxHeight { % <char> CharBoxHeight <num>\n")
    epsdata.append("CharBox\n")
    epsdata.append("exch pop sub neg exch pop\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% The width of a characters bounding box\n")
    epsdata.append("/CharBoxWidth { % <char> CharBoxHeight <num>\n")
    epsdata.append("CharBox\n")
    epsdata.append("pop exch pop sub neg\n")
    epsdata.append("} bind def\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("% Deprecated names\n")
    epsdata.append("/startstack {StartStack} bind  def\n")
    epsdata.append("/endstack {EndStack}     bind def\n")
    epsdata.append("/makenumber {MakeNumber} bind def\n")
    epsdata.append("/numchar { MakeSymbol }  bind def\n")
    epsdata.append("\n")
    epsdata.append("%%EndProlog\n")
    epsdata.append("\n")
    epsdata.append("%%Page: 1 1\n")
    epsdata.append("StartLogo\n")
    epsdata.append("StartLine % line number 1\n")
    epsdata.append("\n")
    epsdata.append("%%SequenceData\n")
    epsdata.append("\n")
    epsdata.append("EndLine\n")
    epsdata.append("EndLogo\n")
    epsdata.append("\n")
    epsdata.append("%%EOF\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    epsdata.append("\n")
    return epsdata
    
#
#
#
def write_eps_logo(site_states_probs, outpath):
    fout = open(outpath, "w")
    for l in generate_eps( site_states_probs.__len__() ):
        fout.write(l)
        if l.startswith("%%SequenceData"):
            sites = site_states_probs.keys()
            sites.sort()
            for site in sites:
                fout.write( write_single_stack(site, site_states_probs[site] ) )
    fout.close()

#
#
#
def write_single_stack(sitenum, data):
    probs_states = {}
    for state in data:
        if probs_states.keys().__contains__( data[state] ):
            probs_states[ data[state] ].append(state)
        else:
            probs_states[ data[state] ] = [ state ]
    ps = probs_states.keys()
    ps.sort()
    line = "(" + sitenum.__str__() + ") startstack\n"
    for prob in ps:
        if prob > 0.001:
            for state in probs_states[prob]:
                line += " %.3f"%prob + " (" + state + ") numchar\n"
    line += "endstack\n"
    return line

####################################
#
# main
#
datpath = ap.getArg("--datpath")
probs = getprobs(datpath)
probs = fill_missing_data(probs)
rsites = None

if ap.doesContainArg("--sites"):
    rsites = ap.getList("--sites")
    #for s in rsites:
        
if True == ap.getOptionalToggle("--printml"):
    print_ml_sequence(probs)

if True == ap.getOptionalToggle("--printlogo"): 
    write_eps_logo(probs, datpath + ".eps")