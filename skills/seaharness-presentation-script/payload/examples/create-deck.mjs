import PptxGenJS from 'pptxgenjs'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

const { atomicReplace } = await import(pathToFileURL(join(process.env.DSH_OFFICE_HELPERS, 'atomic.mjs')).href)

const dest = process.argv[2] || 'deck.pptx'
const Ctor = PptxGenJS.default ?? PptxGenJS
const deck = new Ctor()
const cover = deck.addSlide()
cover.addText('季度汇报', { x: 0.6, y: 2.4, fontSize: 36, bold: true })
const toc = deck.addSlide()
toc.addText('目录', { x: 0.6, y: 0.4, fontSize: 28, bold: true })
const evidence = deck.addSlide()
evidence.addText('证据', { x: 0.6, y: 0.4, fontSize: 28, bold: true })
evidence.addTable([['指标', '数值'], ['营收', '1200'], ['毛利', '360']], { x: 0.6, y: 1.4, w: 8 })
const chart = deck.addSlide()
chart.addChart(deck.ChartType.bar, [{ name: '营收', labels: ['Q1', 'Q2'], values: [10, 12] }], { x: 0.8, y: 1.2, w: 10, h: 4 })
const close = deck.addSlide()
close.addText('结论', { x: 0.6, y: 2.4, fontSize: 32, bold: true })
const data = await deck.write('nodebuffer')
await atomicReplace(dest, Buffer.from(data))
console.log('wrote', dest)
