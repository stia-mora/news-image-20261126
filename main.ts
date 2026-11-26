// news-image-20261126 entry program.
//
// Copies the pre-rendered front page (entry.png, drawn from scratch
// with Python + PIL in draw_entry.py) into the output directory as
// entry.png. Runs with no network and uses only the Node standard
// library.
import { copyFileSync, mkdirSync, existsSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || join(here, "out");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error(`missing source image: ${src}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

// Verify the output is a complete PNG within the competition limits.
const bytes = readFileSync(dst);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("output is not a PNG file");
  process.exit(1);
}
if (bytes.length > 1048576) {
  console.error(`output is ${bytes.length} bytes, over the 1 MiB limit`);
  process.exit(1);
}
const sha256 = createHash("sha256").update(bytes).digest("hex");
console.log(`wrote ${dst} (${bytes.length} bytes, sha256 ${sha256})`);
