#!/usr/bin/env python3
"""Draw the news-image-20261122 front page: 1024x1024 PNG.

A newspaper-style front page summing up Sunday 22 November 2026 world
news: a navy masthead, a 2x4 grid of story cards, and a sources footer.
Rendered with Pillow and the Noto fonts; no network, no external assets.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto"

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)      # warm off-white paper
NAVY = (22, 38, 63)          # masthead band
GOLD = (201, 162, 39)        # masthead rule and date line
INK = (26, 26, 26)           # headline ink
BODY_INK = (58, 58, 58)      # summary ink
GREY = (110, 110, 105)       # footer grey
CARD = (255, 255, 255)       # card face
CARD_EDGE = (205, 198, 184)  # card border

TAG_COLOURS = {
    "CLIMATE": (46, 125, 50),
    "UKRAINE": (21, 101, 192),
    "USA": (158, 43, 37),
    "WEST BANK": (121, 85, 72),
    "SPORT": (0, 121, 107),
    "TECH": (94, 53, 177),
}

# ------------------------------------------------------------- the stories
# tag, headline, one-line summary -- wordings verified 2026-11-23.
STORIES = [
    ("CLIMATE", "COP31 talks collapse, no deal",
     "EU rejects a pact that omits fossil fuels; longest COP ever."),
    ("UKRAINE", "Drone flattens flats near Kyiv",
     "At least 4 killed in Dymer; a boy survives 14 hours in rubble."),
    ("USA", "Democrats clinch 258 House seats",
     "Largest House majority since 1992, after a North Carolina win."),
    ("USA", "Trump orders contractors to alert White House",
     "Firms must flag Congress's oversight requests to the White House."),
    ("USA", "Trump backs a 10% credit card cap",
     "President says he will work with Democrats on the rate cap."),
    ("WEST BANK", "Eisenkot condemns settler arson",
     "Settlers torch West Bank villages; police investigate."),
    ("SPORT", "Alcaraz wins maiden ATP Finals",
     "Beats world No. 1 Zverev 6-2, 7-6 to take the title."),
    ("TECH", "US probes Nvidia's chip sales to China",
     "Bessent seeks answers on who ran compliance at Nvidia."),
]

TITLE = "THE WORLD IN ONE DAY"
DATE_LINE = "SUNDAY \u00b7 22 NOVEMBER 2026"
SOURCES_LINE = "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera"
DATE_FOOTER = "All events happened on 22 November 2026."

# ------------------------------------------------------------------ layout
W, H = 1024, 1024
MASTHEAD_H = 160
GOLD_RULE_H = 4
MARGIN = 40
GAP = 14
GRID_TOP = MASTHEAD_H + GOLD_RULE_H + 10
FOOTER_TOP = 970
GRID_BOTTOM = FOOTER_TOP - 12

COLS, ROWS = 2, 4
CARD_W = (W - 2 * MARGIN - (COLS - 1) * GAP) // COLS
CARD_H = (GRID_BOTTOM - GRID_TOP - (ROWS - 1) * GAP) // ROWS
CARD_PAD = 14
CHIP_H = 24
CHIP_PAD_X = 12


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines, each within max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def wrap_balanced(draw, text, fnt, max_width):
    """Wrap a headline so its lines come out even, not ragged.

    Greedy wrapping leaves orphan words ("deal" alone on line 2);
    for a two-line headline, try every split point and keep the one
    whose longest line is shortest. Falls back to greedy wrapping
    when the headline needs one line, or three.
    """
    words = text.split()
    if len(words) < 3:
        return wrap(draw, text, fnt, max_width)
    greedy = wrap(draw, text, fnt, max_width)
    if len(greedy) != 2:
        return greedy
    best, best_max = None, None
    for cut in range(1, len(words)):
        first = " ".join(words[:cut])
        second = " ".join(words[cut:])
        if (draw.textlength(first, font=fnt) > max_width
                or draw.textlength(second, font=fnt) > max_width):
            continue
        longest = max(draw.textlength(first, font=fnt),
                      draw.textlength(second, font=fnt))
        if best_max is None or longest < best_max:
            best, best_max = (first, second), longest
    return list(best) if best else greedy


def wrap_card(draw, story, head_font, sum_font, inner_w):
    """Wrap one story: balanced headline, greedy summary."""
    _, headline, summary = story
    head_lines = wrap_balanced(draw, headline, head_font, inner_w)
    sum_lines = wrap(draw, summary, sum_font, inner_w)
    return head_lines, sum_lines


def block_height(head_lines, sum_lines, head_font, sum_font):
    """Height of a card's text block: chip + headline + summary."""
    head_lh = int(head_font.size * 1.15)
    sum_lh = int(sum_font.size * 1.25)
    return (CHIP_H + 7
            + len(head_lines) * head_lh + 5
            + len(sum_lines) * sum_lh)


def choose_sizes(draw, inner_w, inner_h):
    """One headline size and one summary size that fit every card.

    Scores each fitting pair by headline + summary size, keeping the
    summary within 9 px of the headline so the two stay in proportion;
    the worst card governs, so all eight cards share the same sizes.
    Raises if nothing fits.
    """
    best = None
    for head_size in range(31, 23, -1):
        for sum_size in range(23, 17, -1):
            if sum_size < head_size - 9:
                continue
            head_font = font("NotoSerif-Bold.ttf", head_size)
            sum_font = font("NotoSans-Regular.ttf", sum_size)
            ok = True
            for story in STORIES:
                head_lines, sum_lines = wrap_card(
                    draw, story, head_font, sum_font, inner_w)
                if len(head_lines) > 3 or len(sum_lines) > 2:
                    ok = False
                    break
                if block_height(head_lines, sum_lines,
                                head_font, sum_font) > inner_h:
                    ok = False
                    break
            if ok:
                score = (head_size + sum_size, head_size)
                if best is None or score > best[0]:
                    best = (score, head_font, sum_font)
    if best is None:
        raise AssertionError("no type size fits all cards")
    return best[1], best[2]


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    title_font = font("NotoSerif-Bold.ttf", 62)
    date_font = font("NotoSans-Bold.ttf", 30)
    title_w = draw.textlength(TITLE, font=title_font)
    draw.text(((W - title_w) / 2, 34), TITLE, font=title_font,
              fill=(255, 255, 255))
    date_w = draw.textlength(DATE_LINE, font=date_font)
    draw.text(((W - date_w) / 2, 108), DATE_LINE, font=date_font,
              fill=GOLD)
    draw.rectangle([0, MASTHEAD_H, W, MASTHEAD_H + GOLD_RULE_H], fill=GOLD)

    # ------------------------------------------------------------ stories
    tag_font = font("NotoSans-Bold.ttf", 17)
    inner_w = CARD_W - 2 * CARD_PAD
    inner_h = CARD_H - 2 * CARD_PAD
    head_font, sum_font = choose_sizes(draw, inner_w, inner_h)
    print("type sizes: headline %d, summary %d"
          % (head_font.size, sum_font.size))
    for index, story in enumerate(STORIES):
        row, col = divmod(index, COLS)
        x0 = MARGIN + col * (CARD_W + GAP)
        y0 = GRID_TOP + row * (CARD_H + GAP)
        x1, y1 = x0 + CARD_W, y0 + CARD_H
        rounded(draw, [x0, y0, x1, y1], radius=10, fill=CARD,
                outline=CARD_EDGE, width=1)

        head_lines, sum_lines = wrap_card(
            draw, story, head_font, sum_font, inner_w)
        tag, headline, summary = story

        # Tag chip.
        chip_w = int(draw.textlength(tag, font=tag_font)) + 2 * CHIP_PAD_X
        chip_y = y0 + CARD_PAD
        rounded(draw, [x0 + CARD_PAD, chip_y,
                       x0 + CARD_PAD + chip_w, chip_y + CHIP_H],
                radius=CHIP_H // 2, fill=TAG_COLOURS[tag])
        draw.text((x0 + CARD_PAD + CHIP_PAD_X, chip_y + 4), tag,
                  font=tag_font, fill=(255, 255, 255))

        # Headline, then summary.
        cursor = chip_y + CHIP_H + 7
        head_lh = int(head_font.size * 1.15)
        for line in head_lines:
            draw.text((x0 + CARD_PAD, cursor), line, font=head_font,
                      fill=INK)
            cursor += head_lh
        cursor += 5
        sum_lh = int(sum_font.size * 1.25)
        for line in sum_lines:
            draw.text((x0 + CARD_PAD, cursor), line, font=sum_font,
                      fill=BODY_INK)
            cursor += sum_lh

        # Nothing may spill past the card's inner box.
        assert cursor - sum_lh <= y1 - CARD_PAD, \
            "card %d overflows: %r" % (index + 1, headline)

    # -------------------------------------------------------------- footer
    foot_font = font("NotoSans-Regular.ttf", 18)
    for i, line in enumerate((SOURCES_LINE, DATE_FOOTER)):
        line_w = draw.textlength(line, font=foot_font)
        draw.text(((W - line_w) / 2, FOOTER_TOP + i * 26), line,
                  font=foot_font, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote %s (%dx%d, %d bytes)" % (out, W, H, size))
    assert size <= 1048576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
