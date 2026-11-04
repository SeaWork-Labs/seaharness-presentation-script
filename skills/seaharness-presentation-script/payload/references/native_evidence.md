# Editable tables and charts

Build required tables, data charts and editable diagrams as slide objects, not screenshots. Keep a supplied image unchanged when the user explicitly asks to use that image. Do not turn every short list into a table.

## Tables

Keep required rows, columns, periods and headers on the relevant slides. Calculate each total once and reuse it in tables, titles and notes. Set column widths, row heights and padding from the actual text; preserve template alignment. Use pptxgenjs `addTable` for new decks, or edit `a:tbl` XML with JSZip for existing decks.

Manually check declared simple sums with displayed-rounding tolerance and reports automatically inferred totals as diagnostics. It is not proof of exact arithmetic or full support for localized numbers. Manually check ratios, subtotals and tables with different units when the checker skips them. Also compare source data and numbers in the slide text with the calculations; passing the checker does not verify those.

## Charts

Keep categories, data series, units, dates, positive/negative signs and precision. Choose a chart that answers the audience's question. Set axis and label formats explicitly; spreadsheet formatting may not carry over. To display 31% with a percentage format, use `0.31`, not `31`.

Use the chart's own labels instead of separate text boxes. Do not duplicate labels or titles, and remove the placeholder “Chart Title.” Keep labels and annotations the audience needs or the user requested. For stacked bar/column charts, use `inEnd` or `center`, not `outEnd`. If an invisible data series positions the visible bars, hide its outlines and labels too. If bar positioning requires positive magnitudes, keep the original positive/negative signs in the data shown to the audience. If the API cannot place a label as required, explain the limitation. See pptxgenjs `addChart` for new decks, or edit the chart part with JSZip for existing decks.

Keep original workbooks when required; never invent formulas or data. Inspect charts in Preview and with `ppt_inspect`. A chart working in PowerPoint does not prove it works in Google Slides.

Inspect the rendered slides: check that labels identify the right data, signs and units are correct, and text is readable. If you can open the deck in its target application, edit and resize representative charts in a test copy, then save and reopen it. Record unavailable application tests without implying that previews verify application behavior. Follow the handoff rules in [SKILL.md](../SKILL.md) for what to report. A chart working in PowerPoint does not prove it works in Google Slides.
