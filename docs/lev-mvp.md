# Lev MVP

## Definition

Lev is a small human-centered agent workspace for live document work.

The user opens a folder, selects a document, writes in that document, and sees
agent assistance in a read-only side panel. Lev observes the work instead of
waiting for a chat prompt.

## Core Hypothesis

For meaningful writing or thinking tasks, an agent is more useful when it
observes the user's current work and prepares context than when it asks the user
to repeatedly prompt it.

Lev succeeds if the user can keep writing while the agent quietly supplies
useful context, references, contradictions, or next moves.

## Non-Goals

- No chat box in the main workbench.
- No automatic edits to the user's document.
- No full-document generation as the default behavior.
- No general-purpose IDE clone.
- No multi-agent orchestration in the first MVP.

## MVP Loop

```text
document edit
  -> debounce
  -> autosave
  -> capture cursor and selection
  -> build recent diff
  -> infer likely intent
  -> optionally search/read pages
  -> update read-only assistance panel
```

## Assistance Contract

Lev may:

- identify the likely current intent
- summarize the local diff
- show useful context from the current document
- find references when the writing intent needs external material
- offer short candidate phrases
- suggest the next small move

Lev should not:

- replace the entire paragraph
- decide the user's conclusion
- turn the side panel into a chat thread
- ask the user to approve work Lev should not have taken over

## Current Implementation

The current implementation is deliberately small:

- `lev/server.py` serves the UI and JSON API using Python standard library HTTP.
- `lev/workspace.py` restricts reads/writes to the selected workspace.
- `web/app.js` captures edits, cursor offset, and selection offsets.
- `lev/assist.py` turns a document-change event into an agent prompt.
- `main.py` remains the reusable lower-level agent loop.

If `BUILDER_API_KEY` is missing or the agent call fails, Lev returns a fallback
panel based on local diff and cursor context. This keeps the UI testable without
the remote model.

## Evaluation

The MVP should be evaluated on whether the human's subject action becomes
smoother:

- Does the user keep writing instead of stopping to prompt?
- Are the side-panel suggestions relevant to the current cursor area?
- Does Lev avoid completing the user's meaningful work?
- Does it save manual search/context-switching?
- Would the user leave it open for a 20-minute writing session?

The first success target:

> During a 20-minute writing session, Lev provides at least three useful pieces
> of context or next-step support without taking over the document.

