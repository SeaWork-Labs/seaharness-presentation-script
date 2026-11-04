import JSZip from 'jszip'
import { join } from 'node:path'
import { readFile } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'

const { atomicReplace, sha256File } = await import(pathToFileURL(join(process.env.DSH_OFFICE_HELPERS, 'atomic.mjs')).href)

const dest = process.argv[2]
const expected = await sha256File(dest)
const zip = await JSZip.loadAsync(await readFile(dest))
const name = 'ppt/slides/slide3.xml'
const xml = await zip.file(name).async('string')
zip.file(name, xml.replace(/>([^<]{0,80})</, '>修订标题<'))
const out = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' })
await atomicReplace(dest, out, expected)
console.log('updated', dest)
