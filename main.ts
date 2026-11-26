// news-image-20261126 — a one-image newspaper front page for
// Thursday 26 November 2026.
//
// The picture itself lives in this repository as entry.png (1024x1024,
// drawn by build/render.py with Pillow). This program does nothing but
// place an exact copy of it at the path the grader reads.
//
// Node 22, standard library only, no network, no dependencies:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Running it twice writes the same bytes both times.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Where the image goes: the grader's /output, or MAKEFUN_OUTPUT_DIR
// when set (handy for a local check). Make the folder first, since a
// fresh container may not have it yet.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });

// entry.png sits next to this file; copy it byte for byte.
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outputDir, "entry.png"));
