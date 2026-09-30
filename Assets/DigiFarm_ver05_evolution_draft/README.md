# DigiFarm Ver 0.5 evolution expansion — review draft

This package expands the supplied files to all 21 unique species listed in Main.md Ver 0.5. The duplicate Lopmon entry is counted once. Original asset identifiers remain unchanged; all new identifiers are proposals and must be matched to your actual asset folders before use.

## Files

- `tree.json`: expanded legacy schema, keyed by source stage and source name. Every destination still has exactly `name`, `field`, `attribute`, `level`, `speed`, `next_level`.
- `starting_eggs.json`: 21 starting egg IDs grouped by project field and attribute.
- `review_manifest.json`: proposed asset IDs, added-edge review status, reference URLs, and special evolution requirements.

## Review status

This is valid JSON with a structurally closed graph, but it is not a fully source-verified canon database. Wikimon retrieval was incomplete. A relationship marked `relationship_supported_by_retrieved_wikimon` was visible in retrieved material; this does not certify the node's field/attribute, establish a measured popularity ranking, or mean the whole chain appeared in an anime. `candidate_needs_source_confirmation` means the relationship needs checking before treating it as canon. Reference URLs for candidates are suggested review pages, not claims that those pages were successfully read. Original edges are retained as legacy content and are not certified by this review.

Selection favours recognizable anime/manga lines and closely associated forms, then sensible attribute variety. Some species have mostly one attribute; no artificial Vaccine/Data/Virus trios were inserted. Free is retained as Free for relevant 02 forms; your selector must support it.

## Compatibility and design limits

- Asset folders were not attached. The 127 new IDs are proposed, not verified existing assets. `Candmon`, `DORUmon`, `Growmon_Orange`, etc. retain your uploaded spelling. New examples include `Veemon`, `Hackmon`, `Demidevimon`, `PawnChessmon_Black`.
- Main.md's `Gammon` is interpreted as Gammamon. New baby ID `Kurimon` corresponds to Wikimon's Curimon.
- Baby fields/attributes follow your existing routing convention and inherit a line affinity. They are game selection metadata, not a claim that babies officially have those attributes. Shared babies may now branch into multiple listed species.
- `speed` and `next_level` remain prototype defaults; no balancing was invented.
- The file retains your stage-skipping and special-form approach. XVmon -> Paildramon and Aquilamon -> Silphymon are flattened into ordinary entries for compatibility. Their anime Jogress partners are recorded in the manifest; the current schema does not enforce those partners. For strict anime mechanics, gate these edges in your loader until a requirements system exists. Existing armor/X/fusion entries likewise remain ungated legacy content.
- Ultimate -> Digitama entries are your project's rebirth convention, not researched natural evolutions. Shared forms can route to different eggs because this schema cannot retain origin lineage. Store an origin egg on the creature instance if rebirth should preserve its family.
- Existing questionable special links such as Beelzebumon -> Ogudomon and Piemon -> VoltoBautamon remain for compatibility and need separate lore/requirements review.

## Corrections to supplied data

- Dodomon -> Dorimon now targets `baby_II`, where Dorimon's definition actually lives.
- `Nature Spirit` normalized to `Nature Spirits` to match the egg selector.
- Growmon_X changed to Virus.
- BlackGalgomon / BlackRapidmon / BlackSaintGalgomon changed to Virus.
- Wizarmon_X -> Beelzebumon_X now targets `ultimate`.
- Alphamon -> Alphamon_Ouryuken now targets `ultimate`, not `digitama`.
- `Uknown` spelling corrected to `Unknown`.
- Missing Andiramon_Virus -> Cherubimon_Vice branch completed.

## Scope and reachable Ultimate forms

These are graph reachability results, including retained legacy links; they are not canon endorsements.

| Ver 0.5 species ID | Reachable Ultimate forms |
|---|---|
| Veemon | Imperialdramon_Dragon, UlforceVdramon |
| Floramon | BloomLordmon, Lotusmon, Pinochimon, Rosemon |
| Funbeemon | HerakleKabuterimon, Queenbeemon, TigerVespamon |
| Hawkmon | Hououmon, Valkyrimon |
| Alraumon | Pinochimon, Rosemon |
| Crabmon | Cthyllamon, MetalSeadramon, Pukumon |
| Swimmon | MetalSeadramon, Pukumon, Regalecusmon |
| Gizamon | Nidhoggmon |
| PawnChessmon_Black | QueenChessmon |
| Zubamon | Durandamon |
| Hackmon | JESmon |
| Gammamon | Arcturusmon, Siriusmon |
| Demidevimon | Piemon, VenomVamdemon |
| Mushmon | Pinochimon |
| Tentomon | GranKuwagamon, HerakleKabuterimon |
| Guilmon | ChaosDukemon, ChaosDukemon_Core, Dukemon, Dukemon_X, Megidramon, Megidramon_X |
| Impmon | Beelzebumon, Beelzebumon_X |
| Candmon | Beelzebumon, Beelzebumon_X, Boltmon, Gankoomon, Gankoomon_X, Piemon |
| Lopmon | Cherubimon_Vice, Cherubimon_Virtue |
| Terriermon | BlackSaintGalgomon, Rapidmon_Armor, SaintGalgomon |
| DORUmon | Alphamon, DORUgoramon |

## Validation

Both JSON files parse. All 21 egg IDs resolve. All 271 evolution destinations resolve in their stated stage. No source has an empty evolution list. All 21 scoped species have at least one path to an Ultimate form. Asset loading and compatibility with the game's Python/Unity loader could not be tested because code and assets were not attached.
