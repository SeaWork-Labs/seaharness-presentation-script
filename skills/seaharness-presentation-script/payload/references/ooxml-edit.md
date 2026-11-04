# OOXML edits for existing PPTX

1. `ppt_open` then `ppt_inspect`. Read `sourceState`. Conflict: stop. Stale: `ppt_refresh`.
2. Open the PPTX with JSZip from `$DSH_OFFICE_NODE_MODULES`.
3. Patch only the requested slide XML (`ppt/slides/slideN.xml` and its rels). Preserve masters, layouts, media, and unrelated slides. Replace text inside existing `<a:t>` nodes so surrounding `<a:rPr>` (font, size, bold, color) and `<a:pPr>` stay. Do not rebuild the slide or invent a new default font for the replacement.
4. Atomic replace, `ppt_validate`, `ppt_refresh`.

Do not rebuild the deck from pptxgenjs unless the user asked for a new file.

```js
import JSZip from 'jszip'
import { join } from 'node:path'
import { readFile } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'

const { atomicReplace, sha256File } = await import(pathToFileURL(join(process.env.DSH_OFFICE_HELPERS, 'atomic.mjs')).href)

const expected = await sha256File(dest)
const zip = await JSZip.loadAsync(await readFile(dest))
const xml = await zip.file('ppt/slides/slide3.xml').async('string')
zip.file('ppt/slides/slide3.xml', xml.replace('旧标题', '新标题'))
const out = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' })
await atomicReplace(dest, out, expected)
```
