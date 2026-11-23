// news-image-20261122: copy the entry image to the output directory.
//
// The image is drawn by draw_news.py and shipped in this repository as
// entry.png; this program only copies it to $MAKEFUN_OUTPUT_DIR (or
// /output by default), so both graded runs write identical bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
