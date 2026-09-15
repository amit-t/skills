# Wayfinder Context

Read this only when the grill or session is connected to a Wayfinder map. This is
context retrieval for a summary, not the Wayfinder ticket-execution workflow.

## Resolve the map

1. Follow the grill/session's explicit map link or the current ticket's parent-map
   relationship first. Read the map body, not merely its title or a search snippet.
2. If no map is linked, discover within the current project in order: root `map.md`
   and one-level `*/map.md` with Wayfinder markers/frontmatter; other repository
   Markdown (including relevant hidden/ignored planning files); then the configured
   tracker. On GitHub, look for `wayfinder:map`, then a targeted issue search. Use
   the available connector or `gh` read commands; absence of a tool is a limitation,
   not evidence that no map exists.
3. Establish identity with the full host/repository and issue reference, or the
   map's local path. For a bare `#N`, inspect and deduplicate configured remotes;
   resolve against plausible repositories rather than assuming `origin`. Match the
   current ticket via explicit membership/parent links, not title similarity.
   If ambiguity remains, summarise the known grill and ask one short map-selection
   question; do not combine maps or block the useful local summary.

## Read only the relevant path

Read the destination, the current ticket's purpose, the prior decision/work that
explains it, and direct blockers/dependants needed to explain what follows. Prefer
current native parent/child and dependency relationships over stale copied lists.
If those are unavailable, use explicit map/body links as a labelled snapshot.
List order, issue numbers, and “closed” alone do not prove dependency order, shipped
behavior, or approval. If the map conflicts with the grill, state the material
conflict and keep the two source states distinct.

Use that evidence to answer:

- What larger outcome is this map pursuing?
- Why is this grill the next decision, or which part of that outcome does it serve?
- What would resolving it enable, and what other gate would still remain?

Include only relationships supported by the sources. If there is no evidenced
prior step or next ticket, omit that detail rather than manufacture a sequence.
Avoid enumerating unrelated branches of the map.

## Missing or stale context

If a linked map cannot be read, continue from the grill and explicitly say the wider
map context could not be verified. If only supplied snapshots are available, name
them as snapshots, not current tracker verification. Do not expose credentials,
probe unrelated accounts, or mutate the tracker to obtain context.

For example, with sources establishing that map #8 aims for reproducible setup,
ticket #40 settled version selection, and #43 depends on this decision:

> The map aims to let teams restore the same reviewed setup without surprises.
> Version selection is settled; this grill now decides what happens when a download
> fails. Answering would settle the policy that restore work (#43) depends on;
> implementation still needs its own approval.

Attach the actual map/grill/ticket links when available. The example is a pattern,
not reusable project evidence.
