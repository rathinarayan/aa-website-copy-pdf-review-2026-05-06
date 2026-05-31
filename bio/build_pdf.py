#!/usr/bin/env python3
"""Dependency-free PDF generator for Narayan Rathi credibility one-pager.
Uses the base-14 Helvetica fonts (WinAnsi) and real AFM glyph widths so text
wraps correctly without any external library."""

# --- Helvetica AFM widths (units / 1000 em) for ASCII 32..126 ---
HELV = {
 32:278,33:278,34:355,35:556,36:556,37:889,38:667,39:191,40:333,41:333,42:389,
 43:584,44:278,45:333,46:278,47:278,48:556,49:556,50:556,51:556,52:556,53:556,
 54:556,55:556,56:556,57:556,58:278,59:278,60:584,61:584,62:584,63:556,64:1015,
 65:667,66:667,67:722,68:722,69:667,70:611,71:778,72:722,73:278,74:500,75:667,
 76:556,77:833,78:722,79:778,80:667,81:778,82:722,83:667,84:611,85:722,86:667,
 87:944,88:667,89:667,90:611,91:278,92:278,93:278,94:469,95:556,96:333,97:556,
 98:556,99:500,100:556,101:556,102:278,103:556,104:556,105:222,106:222,107:500,
 108:222,109:833,110:556,111:556,112:556,113:556,114:333,115:500,116:278,117:556,
 118:500,119:722,120:500,121:500,122:500,123:334,124:260,125:334,126:584}
HELVB = {
 32:278,33:333,34:474,35:556,36:556,37:889,38:722,39:238,40:333,41:333,42:389,
 43:584,44:278,45:333,46:278,47:278,48:556,49:556,50:556,51:556,52:556,53:556,
 54:556,55:556,56:556,57:556,58:333,59:333,60:584,61:584,62:584,63:611,64:975,
 65:722,66:722,67:722,68:722,69:667,70:611,71:778,72:722,73:278,74:556,75:722,
 76:611,77:833,78:722,79:778,80:667,81:778,82:722,83:667,84:611,85:722,86:667,
 87:944,88:667,89:667,90:611,91:333,92:278,93:333,94:584,95:556,96:333,97:556,
 98:611,99:556,100:611,101:556,102:333,103:611,104:611,105:278,106:278,107:556,
 108:278,109:889,110:611,111:611,112:611,113:611,114:389,115:556,116:333,117:611,
 118:556,119:778,120:556,121:556,122:500,123:389,124:280,125:389,126:584}

def tw(s, size, bold=False):
    t = HELVB if bold else HELV
    return sum(t.get(ord(c), 556) for c in s) / 1000.0 * size

def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

def wrap(s, size, maxw, bold=False):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(trial, size, bold) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

ORANGE = (0.784, 0.314, 0.118)
NAVY   = (0.122, 0.165, 0.267)
GREY   = (0.29, 0.33, 0.39)
DARK   = (0.137, 0.153, 0.18)
BOX    = (0.969, 0.957, 0.941)
BOXB   = (0.925, 0.902, 0.871)
LINE   = (0.886, 0.898, 0.918)
NOTEBG = (0.984, 0.965, 0.925)
NOTEBD = (0.941, 0.886, 0.769)

PW, PH = 595.28, 841.89
ML, MR = 50, 50
CW = PW - ML - MR

class Page:
    def __init__(self):
        self.ops = []
    def col(self, rgb, fill=True):
        op = "rg" if fill else "RG"
        self.ops.append(f"{rgb[0]:.3f} {rgb[1]:.3f} {rgb[2]:.3f} {op}")
    def rect(self, x, y, w, h, rgb):
        self.col(rgb, True)
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")
    def line(self, x1, y, x2, w, rgb):
        self.col(rgb, False)
        self.ops.append(f"{w:.2f} w {x1:.2f} {y:.2f} m {x2:.2f} {y:.2f} l S")
    def text(self, x, y, s, size, rgb, bold=False, spacing=0.0):
        f = "F2" if bold else "F1"
        self.col(rgb, True)
        self.ops.append("BT")
        if spacing:
            self.ops.append(f"{spacing:.2f} Tc")
        self.ops.append(f"/{f} {size:.1f} Tf {x:.2f} {y:.2f} Td ({esc(s)}) Tj")
        if spacing:
            self.ops.append("0 Tc")
        self.ops.append("ET")
    def rtext(self, xr, y, s, size, rgb, bold=False):
        self.text(xr - tw(s, size, bold), y, s, size, rgb, bold)
    def para(self, x, y, s, size, rgb, maxw, lead, bold=False):
        for ln in wrap(s, size, maxw, bold):
            self.text(x, y, ln, size, rgb, bold)
            y -= lead
        return y
    def stream(self):
        return "\n".join(self.ops).encode("latin-1", "replace")

# ---------------- Page 1 : client-facing ----------------
p1 = Page()
y = PH - 56
p1.text(ML, y, "FOUNDER CREDIBILITY  .  AUTOMATE ACCELERATOR", 8.5, ORANGE, True, 1.2)
y -= 29
p1.text(ML, y, "Narayan Rathi", 29, NAVY, True)
y -= 19
p1.text(ML, y, "Co-founder & Chief Executive Officer, Automate Accelerator   |   Melbourne, Australia", 10.5, GREY)
y -= 13
p1.line(ML, y, ML + CW, 2, ORANGE)
y -= 18

lead = ("Before founding Automate Accelerator, Narayan co-founded and built two of Australia's "
        "fastest-growing telecommunications businesses. Time Telecom was ranked No. 1 on the 2012 BRW "
        "Fast 100 and acquired by ASX-listed M2 Group; its successor, Smart Business Telecom, kept the "
        "run going with back-to-back BRW Fast Starters and Deloitte Technology Fast 50 placings.")
y = p1.para(ML, y, lead, 10.5, DARK, CW, 15)
y -= 8

# pull-quote
q1 = "\"First place on the Fast 100 list went to telecommunications company Time Telecom,"
q2 = "with a revenue of $51.13m and growth of 375.21 percent.\""
qh = 40
p1.rect(ML, y - qh, 3.5, qh, ORANGE)
p1.rect(ML + 3.5, y - qh, CW - 3.5, qh, BOX)
p1.text(ML + 14, y - 15, q1, 9.5, NAVY, True)
p1.text(ML + 14, y - 27, q2, 9.5, NAVY, True)
p1.text(ML + 14, y - 36, "Coverage of the BRW Fast 100, 2012", 7.5, GREY, False, 0.3)
y = y - qh - 16

# key numbers (single row)
kh = 46
p1.rect(ML, y - kh, CW, kh, BOX)
p1.col(BOXB, False); p1.ops.append(f"0.8 w {ML:.2f} {y-kh:.2f} {CW:.2f} {kh:.2f} re S")
kn = [("3-YEAR REVENUE GROWTH", "375.21%"),
      ("REVENUE AT BRW No. 1", "$51.13 million"),
      ("CUSTOMERS ACQUIRED BY M2", "~30,000")]
cw3 = CW / 3.0
for i, (lbl, val) in enumerate(kn):
    cx = ML + 14 + i * cw3
    p1.text(cx, y - 17, lbl, 7.5, ORANGE, True, 0.3)
    p1.text(cx, y - 33, val, 13, NAVY, True)
y = y - kh - 22

# recognition timeline
p1.text(ML, y, "Recognition track record", 11.5, NAVY, True)
y -= 5
p1.line(ML, y, ML + CW, 0.8, LINE); y -= 16
rows = [
 ("2012", "BRW Fast 100 - ranked No. 1 in Australia", "Time Telecom"),
 ("2012", "Acquired by ASX-listed M2 Group (ASX: MTU)", "Time Telecom"),
 ("2014", "BRW Fast Starters - 8th", "Smart Business Telecom"),
 ("2015", "BRW Fast Starters - 4th", "Smart Business Telecom"),
 ("2015", "Deloitte Technology Fast 50 Australia - 47th (120% growth)", "Smart Business Telecom"),
]
for yr, head, ent in rows:
    p1.text(ML, y, yr, 10, ORANGE, True)
    p1.text(ML + 40, y, head, 10, NAVY, True)
    p1.rtext(ML + CW, y, ent, 9, GREY, False)
    y -= 8
    p1.line(ML, y, ML + CW, 0.5, LINE)
    y -= 9
y -= 6

def section(p, y, title, body):
    p.text(ML, y, title, 11.5, NAVY, True)
    y -= 5
    p.line(ML, y, ML + CW, 0.8, LINE)
    y -= 15
    y = p.para(ML, y, body, 10.5, DARK, CW, 14.5)
    return y - 9

y = section(p1, y, "The story",
    "Co-founded by Narayan, Time Telecom was a Melbourne-based provider serving ~30,000 small-business "
    "and residential customers Australia-wide. Disciplined growth - 375.21% over three years to $51.13 "
    "million in revenue - took it to the top of the 2012 BRW Fast 100 (the AFR / BRW ranking of the "
    "country's fastest-growing established companies). In 2012 it was acquired by M2 Telecommunications "
    "Group (ASX: MTU) via subsidiary Southern Cross Telco for a reported A$18.5 million. Narayan and his "
    "co-founders then built Smart Business Telecom, doubling revenue from ~$22M to ~$48M in three years "
    "and earning fresh BRW Fast Starters and Deloitte Technology Fast 50 recognition.")

y = section(p1, y, "What he does today",
    "Narayan is co-founder and CEO of Automate Accelerator, an Australian-owned B2B growth partner that "
    "helps companies reach specific buyers through clear buyer definitions, checked decision-maker data "
    "and human-led outreach - measured by real replies and conversations, not activity.")

fy = 60
p1.line(ML, fy + 10, ML + CW, 0.8, LINE)
p1.text(ML, fy, "Automate Accelerator  .  Melbourne, Victoria  .  info@automateaccelerator.com", 8.5, GREY)
p1.text(ML, fy - 11, "Figures relate to Time Telecom / Smart Business Telecom, from public sources (see reference sheet). Australian English; ex GST where applicable.", 7.5, GREY)

# ---------------- Page 2 : reference sheet ----------------
p2 = Page()
y = PH - 56
p2.text(ML, y, "FOR YOUR REFERENCE - NOT FOR THE CLIENT", 8.5, ORANGE, True, 1.0)
y -= 27
p2.text(ML, y, "Sources & screenshots to capture", 20, NAVY, True)
y -= 11
p2.line(ML, y, ML + CW, 2, ORANGE); y -= 16
y = p2.para(ML, y,
    "BRW / Deloitte lists credit the COMPANY (Time Telecom, then Smart Business Telecom), not "
    "individuals - there is no standalone article naming Narayan personally. The mention that names you "
    "directly is your own LinkedIn 'Honors & awards' section (first row). Outbound image downloads are "
    "blocked in this environment, so below are the source links; open each, screenshot the highlighted "
    "item and place it beside the matching claim.", 9.5, DARK, CW, 13.5)
y -= 7

sources = [
 ("Narayan Rathi - LinkedIn 'Honors & awards' (NAMES YOU)", "Lists 'BRW Fast Starters - 1st place' and 'BRW Fast 100'. The artifact that credits you personally - screenshot it.  linkedin.com/in/narayanrathi"),
 ("BRW Fast 100 2012 - No. 1 (PUBLISHED ARTICLE)", "Franchise Business, 'Which franchises made the Fast 100 list?' quotes verbatim: \"First place on the Fast 100 list went to telecommunications company Time Telecom, with a revenue of $51.13m and growth of 375.21 percent.\"  franchisebusiness.com.au/which-franchises-made-the-fast-100-list/"),
 ("M2 acquisition of Time Telecom (2012)", "The Register, 28 Feb 2012, 'M2 Telecoms buys some Time' (Southern Cross Telco; ~A$18.5M; ~30,000 customers).  theregister.com/2012/02/28/m2_buys_time/ ; M2 Group: en.wikipedia.org/wiki/M2_Group"),
 ("Smart Business Telecom - BRW Fast Starters (2014 & 2015)", "Ex-Time Telecom group; moved 8th (2014) to 4th (2015); revenue ~$22M to ~$48M in three years.  forums.whirlpool.net.au/thread/1091483"),
 ("Smart Business Telecom - Deloitte Tech Fast 50 2015 (#47)", "Ranked 47th with 120% growth.  Deloitte Technology Fast 50 Winners 2015 (slideshare.net/DeloitteAustralia/deloitte-technology-fast-50-winners-2015)"),
 ("Companies (LinkedIn)", "Time Telecom: au.linkedin.com/company/time-telecom ; Smart Business Telecom: crunchbase.com/organization/smart-business-telecom"),
]
for title, desc in sources:
    p2.text(ML, y, title, 10, NAVY, True)
    y -= 13
    y = p2.para(ML + 4, y, desc, 9, GREY, CW - 4, 12)
    y -= 5
    p2.line(ML, y + 2, ML + CW, 0.6, LINE)
    y -= 11

note_lines = [
 ("Verification notes - please confirm before sending:", True),
 ("1. Role: per your confirmation the bio describes you as co-founder/owner of both Time Telecom and Smart Business Telecom. (Public LinkedIn currently shows 'Senior Director, Operations' then 'Senior Director, Marketing' - consider aligning your LinkedIn so it matches the co-founder framing before a client cross-checks it.)", False),
 ("2. Deloitte Technology Fast 50: now specific and sourced - Smart Business Telecom, 2015, 47th, 120% growth (Deloitte Australia winners list). Confirm before publishing.", False),
 ("3. Award logos: your launch checklist flags confirming whether BRW / Deloitte / M2 logos can be used. Get sign-off before adding logos to a client-facing version.", False),
]
wrapped = []
for txt, b in note_lines:
    wrapped.append((wrap(txt, 9, CW - 24, b), b))
nh = 16 + sum(len(w) * 12 for w, _ in wrapped) + 6
p2.rect(ML, y - nh, CW, nh, NOTEBG)
p2.col(NOTEBD, False); p2.ops.append(f"0.8 w {ML:.2f} {y-nh:.2f} {CW:.2f} {nh:.2f} re S")
ny = y - 16
for wls, b in wrapped:
    for ln in wls:
        p2.text(ML + 12, ny, ln, 9, (0.353, 0.290, 0.165), b)
        ny -= 12

# ---------------- Assemble ----------------
def pdf(pages):
    cat, pages_obj, f1, f2 = 1, 2, 3, 4
    nid = 5
    page_ids, content_ids = [], []
    for _ in pages:
        page_ids.append(nid); content_ids.append(nid + 1); nid += 2
    buf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    def emit(num, body):
        offsets[num] = len(buf)
        buf.extend(f"{num} 0 obj\n".encode()); buf.extend(body); buf.extend(b"\nendobj\n")
    emit(cat, f"<< /Type /Catalog /Pages {pages_obj} 0 R >>".encode())
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    emit(pages_obj, f"<< /Type /Pages /Count {len(pages)} /Kids [{kids}] >>".encode())
    emit(f1, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    emit(f2, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    for i, pg in enumerate(pages):
        pid, cid = page_ids[i], content_ids[i]
        emit(pid, (f"<< /Type /Page /Parent {pages_obj} 0 R /MediaBox [0 0 {PW} {PH}] "
                   f"/Resources << /Font << /F1 {f1} 0 R /F2 {f2} 0 R >> >> /Contents {cid} 0 R >>").encode())
        s = pg.stream()
        emit(cid, b"<< /Length " + str(len(s)).encode() + b" >>\nstream\n" + s + b"\nendstream")
    xref_pos = len(buf)
    n = nid - 1
    buf.extend(f"xref\n0 {n+1}\n".encode())
    buf.extend(b"0000000000 65535 f \n")
    for num in range(1, n + 1):
        buf.extend(f"{offsets[num]:010d} 00000 n \n".encode())
    buf.extend(f"trailer\n<< /Size {n+1} /Root {cat} 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode())
    return bytes(buf)

with open("Narayan_Rathi_Credibility_Bio.pdf", "wb") as fh:
    fh.write(pdf([p1, p2]))
print("wrote Narayan_Rathi_Credibility_Bio.pdf")
