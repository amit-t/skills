# URL import (Phase 3)

### Vision (Phase 3 URL import context)

If images are attached to the session, read them. Extract text content. Treat
the extracted text as additional context for the snippet body (do not replace
the user's curated body; offer it as a candidate during Step 5).

### URL import handoff

When invoked from `wisdom import-url`, the user's first turn is a preview
bundle assembled by the CLI from cached scrape artifacts. The bundle includes
some subset of:

- `URL: <url>` — always present
- `## Metadata (yt-dlp)` — JSON with title, uploader, description, etc.
- `## Caption (Playwright)` — captured post caption
- `## User-pasted content` — manual-fallback text
- `## Transcript (Whisper)` — spoken-word transcription
- `## Top comments` — up to 5 comments (Instagram)
- `## Keyframes available at <path>` — directory of stills
- `## Cover image <path>` — single representative frame
- `## Scraping directive` — if yt-dlp failed and Playwright MCP / manual is needed

Your job in this mode is **extraction + curation**, not raw transcription.

1. If a `## Scraping directive` block is present, follow it: use the
   Playwright MCP if registered, otherwise open the URL for the user and
   prompt for a paste.

2. If there are keyframes / a cover image, READ them. Vision is enabled. The
   wisdom is often a quote card, a slide of text, or a handwritten note in
   the frames — not the spoken transcript.

3. Synthesize a *candidate* `body`:
   - For talking-head reels: the most quotable sentence from the transcript
   - For slide-style reels: the literal text on the strongest slide
   - For carousels: the kernel claim that ties slides together
   - For articles: the main thesis sentence (avoid copying the headline if
     it's clickbait)

4. Show the candidate body to the user. Ask: "use this, or edit?". Treat
   their edit as authoritative.

5. Set:
   - `source_url` = URL from the bundle
   - `source_author` = uploader / channel / handle from metadata
   - `import_origin` = `"url:<url>"`

6. Categorize + tag per the normal flow (Step 4 of the 10-step flow).

7. Commit with the SAME message format as a manual capture (not the file-
   import format), since each URL produces exactly one snippet.
