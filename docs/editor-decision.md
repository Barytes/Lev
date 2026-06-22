# Editor Decision

## Question

Should Lev fork an existing text editor frontend, use an existing editor library,
or implement an editor from scratch?

## Recommendation

Do not fork a full editor product for the MVP. Use a tiny native `<textarea>`
for the first runnable version, then migrate the editor surface to CodeMirror 6
behind an adapter once cursor-aware features matter.

## Why Not Fork A Full Editor

Forking a complete editor app sounds faster, but it usually imports another
product's assumptions:

- command palette, file tree, settings, themes, and plugin system
- build tooling and dependency churn
- UX decisions that compete with Lev's no-chat, side-panel-first concept
- maintenance burden before the HC agent loop is validated

Lev's core risk is not text editing. The core risk is whether passive document
observation can produce useful, non-invasive assistance. A full fork adds
surface area before that risk is answered.

## Why Not Build A Rich Editor From Scratch

A plain `<textarea>` can detect:

- current text
- cursor offset through `selectionStart`
- selection through `selectionStart` and `selectionEnd`
- keyboard and input events

That is enough for the MVP.

It is not enough for the later product if Lev needs:

- line/column mapping with decorations
- inline anchors
- jump-to-evidence
- hover widgets
- stable range tracking across edits
- syntax-aware blocks
- multi-cursor or structured selections

Those should not be hand-rolled.

## Why CodeMirror 6 Next

CodeMirror 6 is the best next editor base for Lev:

- lighter than a full IDE editor
- designed as composable packages
- strong state/update transaction model
- first-class selections and cursor information
- decorations and view plugins for inline assistance
- programmatic scrolling and selection changes
- good fit for Markdown/prose workbenches

The future Lev editor adapter should expose only the methods Lev needs:

```ts
interface EditorAdapter {
  getText(): string;
  setText(text: string): void;
  getCursorOffset(): number;
  getSelection(): { from: number; to: number };
  focusRange(from: number, to: number): void;
  scrollToOffset(offset: number): void;
  onChange(callback: () => void): void;
  onSelectionChange(callback: () => void): void;
}
```

The current `web/app.js` already behaves like a primitive version of this
adapter. It should be split into an explicit `textareaAdapter.js` before adding
CodeMirror.

## When Monaco Makes Sense

Monaco is a strong choice if Lev becomes code-first:

- code navigation
- language services
- diagnostics
- IDE-like editor commands
- large-file code editing

For Lev's current writing/research MVP, Monaco is heavier than necessary.

## Workload Comparison

| Option | MVP work | Future cursor/jump support | Maintenance |
| --- | --- | --- | --- |
| Native textarea | lowest | limited but enough for MVP | lowest |
| CodeMirror 6 library | medium | strong | medium |
| Monaco library | medium-high | very strong for code | medium-high |
| Fork full editor app | high hidden cost | depends on fork | highest |

## Decision

Use native textarea now, design the boundary so the next editor can be
CodeMirror 6 without changing Lev's backend or agent loop.

