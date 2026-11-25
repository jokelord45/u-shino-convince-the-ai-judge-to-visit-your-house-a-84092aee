// u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee entrypoint
// (Node 22, standard library only).
// Copies the bundled invitation image (entry.png beside this file) to
// /output/entry.png, or to $MAKEFUN_OUTPUT_DIR when set (local runs).
// The image is a PNG rendered by render_letter.py: a letter addressed
// to the AI judge, drawn with code so every word is exactly legible.
// Before copying, the entrypoint refuses anything that is not a
// complete PNG within the gate limits (at most 1 MiB, at most
// 1024x1024), and after copying it re-checks the bytes on disk, so
// two runs always write the same valid bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1_048_576;
const MAX_DIM = 1024;
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const IEND = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);

function die(msg: string): never {
  console.error(`error: ${msg}`);
  process.exit(1);
}

function pngSize(blob: Buffer): [number, number] | null {
  if (blob.length < 33 || !blob.subarray(0, 8).equals(PNG_SIG)) return null;
  if (blob.readUInt32BE(8) !== 13 || blob.toString('ascii', 12, 16) !== 'IHDR') {
    return null;
  }
  const width = blob.readUInt32BE(16);
  const height = blob.readUInt32BE(20);
  return [width, height];
}

function check(blob: Buffer): [number, number] {
  if (blob.length > MAX_BYTES) die(`bundled image too large: ${blob.length} bytes`);
  if (!blob.subarray(blob.length - 12).equals(IEND)) {
    die('bundled image has no PNG IEND trailer');
  }
  const size = pngSize(blob);
  if (!size) die('cannot read the bundled image dimensions');
  const [w, h] = size;
  if (w > MAX_DIM || h > MAX_DIM) die(`bundled image too big: ${w}x${h}`);
  return size;
}

const source = new URL('./entry.png', import.meta.url);
const blob = readFileSync(source);
const [width, height] = check(blob);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);

const written = readFileSync(dest);
if (!written.equals(blob)) die('written output differs from the bundled image');
const [ow, oh] = check(written);
if (ow !== width || oh !== height) die('written output dimensions changed');
const sha = createHash('sha256').update(written).digest('hex');
console.log(`entry.png: ${width}x${height}, ${written.length} bytes, sha256 ${sha} -> ${dest}`);
