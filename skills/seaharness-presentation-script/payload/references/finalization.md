# Validate and deliver

Use when creating or editing a local PPTX. Set runtime paths as described in `references/implementation.md`. Preview plus `ppt_inspect` / `ppt_validate` is the shipping check. Optional PNG render scripts in `scripts/` are debugging only.

## Declare task requirements

Build requirements from the actual request and source deck:

- An ordinary N-slide request means N total slides, including any cover, unless the user says otherwise.
- Required native tables and charts stay editable objects, not screenshots.
- Keep the template's slide count when the user requires it.
- Fonts come from the template, an explicit user request, or a design choice you can name. Do not claim the user requested fonts you chose.

## Check the draft and write the final file

1. Export the builder to a temp file, then atomically replace the destination.
2. Open with `ppt_open` and `publish=true` as soon as the file exists. That is delivery.
3. Optional: `ppt_inspect` / `ppt_validate` after publish. Do not search the machine for a template when the user already gave a path.
4. The person reviews in Presentation Preview.

Do not import `@oai/artifact-tool`. Do not call a Codex finalizer. Package integrity plus Preview does not prove the slides look good, the facts are correct, or the deck works in PowerPoint or Google Slides.

## Review and repair

Before delivery:

1. Inspect each slide in Preview; use optional PNG scripts only when the user asks for page images.
2. For a small edit, compare changed slides with the originals and scan the whole deck for unintended changes.
3. Fix unintended overlap, clipping, wrapping, broken connectors, unresolved placeholders, inconsistent footers, and chart/data mismatches by patching the same builder and rerunning it.
4. Confirm the deck satisfies the user request and the narrative remains coherent.
5. Verify researched claims and sourced assets are traceable and cite sources when research informed the deck.
