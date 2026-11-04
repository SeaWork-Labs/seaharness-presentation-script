# Editable bullet lists

Keep the template's paragraph and numbering settings. For new pptxgenjs lists, use native text objects with bullet options, not a screenshot of a list and not extra text boxes of typed bullet characters.

```js
slide.addText(
  [
    { text: "Revenue held", options: { bullet: true, breakLine: true } },
    { text: "Cost fell", options: { bullet: true, breakLine: true } },
  ],
  { x: 0.6, y: 1.6, w: 8, h: 2.4, fontSize: 18, fontFace: selectedFamily, color: "142735", valign: "top" },
)
```

Choose spacing to suit the font and layout; these values are examples, not a required style. Use structured text runs for bold phrases so their formatting is preserved.

When editing an existing deck with JSZip, keep `a:pPr@marL`, hanging `indent`, `a:buChar` or `a:buAutoNum`, and paragraph spacing. Wrapped lines should align with the text above them, not with the bullet. Leave a clear gap between bullet and text. Do not imitate lists with repeated spaces.
