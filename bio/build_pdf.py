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
# Helvetica-Bold widths
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

# RGB helpers
ORANGE = (0.784, 0.314, 0.118)
NAVY   = (0.122, 0.165, 0.267)
GREY   = (0.29, 0.33, 0.39)
DARK   = (0.137, 0.153, 0.18)
BOX    = (0.969, 0.957, 0.941)
BOXB   = (0.925, 0.902, 0.871)
LINE   = (0.886, 0.898, 0.918)
NOTEBG = (0.984, 0.965, 0.925)
NOTEBD = (0.941, 0.886, 0.769)
BLUE   = (0.141, 0.337, 0.651)

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
    def para(self, x, y, s, size, rgb, maxw, lead, bold=False):
        for ln in wrap(s, size, maxw, bold):
            self.text(x, y, ln, size, rgb, bold)
            y -= lead
        return y
    def stream(self):
        return "\n".join(self.ops).encode("latin-1", "replace")

# ---------------- Build page 1 ----------------
p1 = Page()
y = PH - 58
p1.text(ML, y, "FOUNDER CREDIBILITY  .  AUTOMATE ACCELERATOR", 8.5, ORANGE, True, 1.2)
y -= 30
p1.text(ML, y, "Narayan Rathi", 30, NAVY, True)
y -= 20
p1.text(ML, y, "Co-founder & Chief Executive Officer, Automate Accelerator   |   Melbourne, Australia", 10.5, GREY)
y -= 14
p1.line(ML, y, ML + CW, 2, ORANGE)
y -= 20

lead = ("Before founding Automate Accelerator, Narayan was part of the leadership team that built "
        "Time Telecom into the fastest-growing company in Australia - ranked No. 1 on the 2012 BRW "
        "Fast 100 - and then sold the business to ASX-listed M2 Telecommunications Group. The same "
        "operator discipline now sits behind Automate Accelerator's growth partnerships.")
y = p1.para(ML, y, lead, 11, DARK, CW, 16)
y -= 10

# stat box
box_h = 96
box_top = y
p1.rect(ML, box_top - box_h, CW, box_h, BOX)
p1.col(BOXB, False)
p1.ops.append(f"0.8 w {ML:.2f} {box_top-box_h:.2f} {CW:.2f} {box_h:.2f} re S")
colw = CW / 3.0
cells = [
 ("BRW FAST 100 (2012)", ["Ranked No. 1 - Australia's", "fastest-growing company"]),
 ("3-YEAR REVENUE GROWTH", ["375.21%", "(to FY2011-12)"]),
 ("REVENUE AT RANKING", ["$51.13 million"]),
 ("EXIT", ["Acquired by ASX-listed", "M2 Group (2012)"]),
 ("CUSTOMERS AT ACQUISITION", ["~30,000 business &", "residential"]),
 ("FURTHER RECOGNITION", ["Deloitte Technology", "Fast 50 Australia"]),
]
for i, (lbl, vals) in enumerate(cells):
    cx = ML + 12 + (i % 3) * colw
    cy = box_top - 20 - (i // 3) * (box_h / 2.0)
    p1.text(cx, cy, lbl, 7.5, ORANGE, True, 0.3)
    yy = cy - 13
    for v in vals:
        p1.text(cx, yy, v, 10.5, NAVY, True)
        yy -= 12
y = box_top - box_h - 24

def section(p, y, title, body):
    p.text(ML, y, title, 11.5, NAVY, True)
    y -= 5
    p.line(ML, y, ML + CW, 0.8, LINE)
    y -= 16
    y = p.para(ML, y, body, 10.5, DARK, CW, 15)
    return y - 10

y = section(p1, y, "The Time Telecom story",
    "Time Telecom was a Melbourne-based telecommunications provider serving small and medium business "
    "and residential customers Australia-wide. Through sustained, disciplined growth it reached $51.13 "
    "million in revenue on the back of 375.21% revenue growth over three years - enough to top the 2012 "
    "BRW Fast 100, the Australian Financial Review / BRW ranking of the country's fastest-growing "
    "established companies. In 2012 the business was acquired by M2 Telecommunications Group (ASX: MTU) "
    "- then one of Australia's largest challenger telcos - through its subsidiary Southern Cross Telco, "
    "in a deal reported at around A$18.5 million, bringing across roughly 30,000 customers. M2 later "
    "merged with Vocus in 2016.")

y = section(p1, y, "Continuing the growth track record",
    "Narayan stayed in the high-growth telco sector, where the group also earned recognition among "
    "Australia's fastest-growing technology companies in the Deloitte Technology Fast 50, and the "
    "follow-on venture Smart Business Telecom placed 4th on the BRW Fast Starters list in 2015. In 2021 "
    "he founded Automate Accelerator, applying the same buyer-clarity and operating discipline to help "
    "Australian B2B companies build serious outbound growth channels.")

y = section(p1, y, "What he does today",
    "Narayan is co-founder and CEO of Automate Accelerator, an Australian-owned B2B growth partner. AA "
    "helps companies reach specific buyers through clear buyer definitions, checked decision-maker data "
    "and human-led outreach - measured by real replies and conversations, not activity. He stays close "
    "to strategy, offer positioning and the first version of every new client brief.")

# footer
fy = 64
p1.line(ML, fy + 10, ML + CW, 0.8, LINE)
p1.text(ML, fy, "Automate Accelerator  .  Melbourne, Victoria  .  info@automateaccelerator.com", 8.5, GREY)
p1.text(ML, fy - 11, "Figures relate to Time Telecom and are drawn from public sources (see reference sheet). Australian English; figures ex GST where applicable.", 8.0, GREY)

# ---------------- Build page 2 (reference) ----------------
p2 = Page()
y = PH - 58
p2.text(ML, y, "FOR YOUR REFERENCE - NOT FOR THE CLIENT", 8.5, ORANGE, True, 1.0)
y -= 28
p2.text(ML, y, "Sources & screenshots to capture", 20, NAVY, True)
y -= 12
p2.line(ML, y, ML + CW, 2, ORANGE)
y -= 18
y = p2.para(ML, y,
    "I could not embed live screenshots from this environment (outbound image downloads are blocked here), "
    "so below are the primary links. Open each, screenshot the highlighted figure, and place the image beside "
    "the matching claim in the one-pager.", 9.5, DARK, CW, 14)
y -= 8

sources = [
 ("BRW Fast 100 2012 - No. 1", "Time Telecom first place: $51.13M revenue, 375.21% growth (3 yrs to 2011-12). AFR / BRW Fast 100 2012 archives; franchisebusiness.com.au coverage."),
 ("M2 acquisition of Time Telecom", "The Register, 28 Feb 2012 - 'M2 Telecoms buys some Time' (Southern Cross Telco; ~A$18.5M; ~30,000 customers).  theregister.com/2012/02/28/m2_buys_time/"),
 ("M2 Group (ASX: MTU)", "Company background, acquisitions and 2016 Vocus merger.  en.wikipedia.org/wiki/M2_Group"),
 ("Deloitte Technology Fast 50 Australia", "Program overview - CONFIRM exact year & rank before publishing a specific placement.  deloitte.com/au/en/Industries/tmt/about/technology-fast-50.html"),
 ("Smart Business Telecom - Fast Starters 4th (2015)", "Ex-Time Telecom group, moved from 8th to 4th.  forums.whirlpool.net.au/thread/1091483"),
 ("Time Telecom (company)", "au.linkedin.com/company/time-telecom"),
]
for title, desc in sources:
    p2.text(ML, y, title, 10, NAVY, True)
    y -= 13
    y = p2.para(ML + 4, y, desc, 9, GREY, CW - 4, 12)
    y -= 6
    p2.line(ML, y + 2, ML + CW, 0.6, LINE)
    y -= 12

# note box
note_lines = [
 ("Verification notes - please confirm before sending:", True),
 ("1. Your exact role/title at Time Telecom (public records list 'Senior Director, Operations'). Adjust the 'leadership team' wording to match.", False),
 ("2. Deloitte Technology Fast 50: exact year/rank not verifiable in public sources. The one-pager only says 'recognised in' (no rank). If you have the certificate/year I'll make it specific; otherwise consider removing it to stay fully proof-honest.", False),
 ("3. Award logos: your launch checklist flags confirming whether BRW / Deloitte / M2 logos can be used. Get sign-off before adding logos to a client-facing version.", False),
]
# measure box height
wrapped = []
for txt, b in note_lines:
    wls = wrap(txt, 9, CW - 24, b)
    wrapped.append((wls, b))
nh = 16 + sum(len(w) * 12 for w, _ in wrapped) + 6
p2.rect(ML, y - nh, CW, nh, NOTEBG)
p2.col(NOTEBD, False)
p2.ops.append(f"0.8 w {ML:.2f} {y-nh:.2f} {CW:.2f} {nh:.2f} re S")
ny = y - 16
for wls, b in wrapped:
    for ln in wls:
        p2.text(ML + 12, ny, ln, 9, (0.353, 0.290, 0.165), b)
        ny -= 12
    ny -= 0

# ---------------- Assemble PDF ----------------
def pdf(pages):
    objs = []
    def add(b):
        objs.append(b); return len(objs)
    # placeholders to keep numbering: 1 catalog,2 pages,3 font,4 fontb, then per page: page obj + content
    cat = 1; pages_obj = 2; f1 = 3; f2 = 4
    page_ids = []; content_ids = []
    nid = 5
    for _ in pages:
        page_ids.append(nid); content_ids.append(nid + 1); nid += 2
    out = []
    out.append(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    buf = bytearray(out[0])
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

data = pdf([p1, p2])
with open("Narayan_Rathi_Credibility_Bio.pdf", "wb") as fh:
    fh.write(data)
print("wrote Narayan_Rathi_Credibility_Bio.pdf", len(data), "bytes")
