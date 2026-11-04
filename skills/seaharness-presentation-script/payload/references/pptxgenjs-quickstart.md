# pptxgenjs 3.12.0 quickstart

Create new PPTX with managed pptxgenjs. Edit existing PPTX with JSZip + OOXML after `ppt_inspect`. Do not use python-pptx. Do not copy artifact-tool.

```js
import PptxGenJS from 'pptxgenjs'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

const { atomicReplace } = await import(pathToFileURL(join(process.env.DSH_OFFICE_HELPERS, 'atomic.mjs')).href)

const Ctor = PptxGenJS.default ?? PptxGenJS
const deck = new Ctor()
deck.defineLayout({ name: 'WIDE', width: 13.333, height: 7.5 })
deck.layout = 'WIDE'
const slide = deck.addSlide()
slide.addText('季度汇报', { x: 0.6, y: 0.4, fontSize: 32, fontFace: 'Arial', bold: true })
slide.addTable([['指标', '数值'], ['营收', '1200']], { x: 0.6, y: 1.6, w: 8, colW: [4, 4], border: [{ pt: 1, color: 'D9D9D9' }] })
slide.addChart(deck.ChartType.bar, [{ name: '营收', labels: ['Q1', 'Q2'], values: [10, 12] }], { x: 0.6, y: 3.4, w: 8, h: 3 })
slide.addNotes('单位：万元。来源：经营表。')
const data = await deck.write('nodebuffer')
await atomicReplace(dest, Buffer.from(data))
```

Keep required tables and charts as native objects, not screenshots. Inspect with `ppt_inspect` and confirm shapes, not a single picture.
