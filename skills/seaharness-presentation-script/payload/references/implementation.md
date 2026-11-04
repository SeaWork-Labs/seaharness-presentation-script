# Local presentation implementation

Read before creating or editing a local PPTX. Do not modify this skill's files while making a deck.

## Runtime and paths

Use `$DSH_OFFICE_NODE` and `$DSH_OFFICE_NODE_MODULES` from the managed Office runtime. Optional Python helpers use `$DSH_OFFICE_PYTHON`. Do not install substitutes or modify the bundled dependencies. Do not forge those environment variables.

Set `SKILL_DIR` to this skill's absolute directory and write the deck inside the Session workspace. Create a private build subdirectory for drafts. Run modules with `$DSH_OFFICE_NODE`; `import PptxGenJS from 'pptxgenjs'` resolves without `NODE_PATH` or a `node_modules` symlink. Prefer `write('nodebuffer')` over `writeFile`, which appends `.pptx`. Plain `.mjs` files cannot contain TypeScript annotations or JSX syntax.

Write to a temp file, SHA-256 the destination if it exists, then `os.replace`. Validate with `ppt_inspect` / `ppt_validate`, then `ppt_open` with `publish=true`. Never overwrite the source unless explicitly requested.

## Typography and geometry

Keep template fonts and slide dimensions. Otherwise choose suitable available fonts and a 16:9 slide size. pptxgenjs geometry uses inches. Keep intended font pairings and any additional fonts needed for other writing systems.

Use `references/pptxgenjs-quickstart.md` for new decks and `references/ooxml-edit.md` for existing decks. Put source citations in the relevant slide's speaker notes. Follow `references/finalization.md` for validation and delivery.
