# TODO Tasks

## Documentation
- [ ] shaping an effect with effects data (currently in `default_fx`)
- [ ] manager, map, maker (see below)

## FIX: Live Exceptions
- [ ] `MOVE` effect moves each letter to same `x` location, not relative
  - expected: move relative to each letter
  - question: transform not offset but to fixed target for all effects?
- [ ] compound effects apply effect-sequentially to letters
  - expected: apply all effects to first letter, move to next letter, apply ...

## Collect Relevant Comments
- [ ] parse scripts for and pull out TODO comments
- [ ] parse scripts for and pull out NOTE comments
- [ ] format comments into task checklist below

## Persist Effects Data between Executions and Sessions
- (see README for more info on this challenge)
- [ ] make text fx empty objects usable between file save, quit, reopen
  - [ ] read effect empties' `text_fx` between sessions
  - [ ] read scene's `text_fx` data between sessions
- [ ] modify existing text effects
  - [ ] update existing effect properties through empty
  - [ ] decide: is scene `text_fx` data read-only?
    - [ ] if not, update existing scene data even when effect not created
  - [ ] use `replace` prop to layer vs overwrite effects

## Props & attributes
- [ ] set prop value UI defaults for individual effects (e.g. popin defaults frames a bit negative)
- [ ] randomization (see "calculations" below)
- [ ] document how to add key to effect data (as had to do with `'relative'`)
  - [ ] through `default_fx`, `fx_manager`, `fx_map` and `fx_maker`

## Calculations
- [ ] add randomness to transforms
  - [ ] prop for randomizing effect
  - [ ] apply (compare `kf_arc` in fx and logic in `fx_maker`)
- [ ] test letter spacing and offsetting in `fx_maker.string_to_letters` with a range of fonts
  - [ ] account for right-left and other letter patterns
  - [ ] revisit deleting spaces - should they be part of effect?

## Namespacing
- [ ] take time to think about names and list rationale here
  - data rationale: ...
  - logic rationale: ...
  - ui rationale: ...
  - registration rationale: ...
  - helper/handler rationale: ...
- [ ] consider "fx" consistency: `text_fx` vs `fx` vs `effect` vs `effects`
  - is an "effect" (1) the data that describes a type of text effect?
  - is an "effect" (2) the application of (1) to a string of text?
  - is an "effect" (3) the animated letters-plus-parent left after running (2)?
- [ ] consider "maker" ambiguity: is it a creator? an applier? a maker? an fx-er?
  - the `fx_maker` _applies_ effects to create or "make" a nested text_fx object (letters + empty)
    - _empty_ represents the abstract effected text
      - store fx data for the created effect
      - parent to its letters
    - _letters_ are animated text objects using the fx props through maker logic

## Effects Maker
- [ ] see test class in
- [ ] resolve naming ambiguity above for term "maker"
- [ ] resolve naming ambiguity above for effects terms
- [ ] add ability to create and store custom effects
  - [ ] take effect name, affected attribute, keyframe `(magnitude, frames)` arc, axis
  - [ ] compound or stack effects with array of existing effect names
  - [ ] read effects between sessions (see persistence above)
- [ ] view and edit through UI
