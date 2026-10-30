# Mock-ups and prototypes

Static boards hide the hard decisions on a device that changes shape. Mock up at real sizes, then prototype in motion before building.

## Frames

Use the real sizes in points:

| Pose | Frame | Content area |
|---|---|---|
| Closed portrait | 466 × 678 | about 394 wide, with the rail (about 72) on the right and the camera at its top |
| Tent / closed landscape | 678 × 466 | about 606 wide, with the rail on the right and the camera at its bottom |
| Open landscape | 951 × 669 | with the rail on the right |
| Open portrait | 669 × 951 | with horizontal bars at the top and bottom |

- **Draw system chrome as part of the frame, not the app.**
  - The rail holds the Dynamic Island, status bar, toolbar icons and tab bar, top to bottom.
  - Keep it visually separate so nobody designs something the app can't control.
  - Don't draw a second status bar or camera inside the content.
- **Leave reserved regions empty:**
  - the outer camera, always
  - the inner camera, only while it's in use
  - the fold, down the middle of the inner display while it's partially open

  Hatch or tint them so it's obvious nothing goes there.
- **Use SF Symbols for every rail item**, with the title noted beside it. It's a reminder that items need both.
- **Get the margins and safe areas from [Apple Design Resources](https://developer.apple.com/design/resources/)**, not guesses.

## Boards

- **Lay out one row per step in the path:** closed | open | tent, plus open portrait if it differs. Reading across a row shows what happens when someone opens or turns the phone.
- **Add rows for mid-journey changes**, e.g. "closed, with a detail open" → "open". These are where layouts break.
- **Label every board** with the pose and the size.
- **Annotate the rail:**
  - each item's priority
  - what overflows into "…" at this height
  - which controls belong to a pane rather than to the rail
- **Show both side-by-side and full-screen states** for any pane that can go full screen.

## Prototype in motion

- **Build a fold page:** a drawn Duo that opens and closes with the mock-ups on it, plus a slider to fold it by hand.
  - The slider drives the hinge from closed to open.
  - The layout swaps from the outer to the inner display at the point the phone would.
  - Animate panes moving into place, so you can see what jumps, duplicates or vanishes.
- **Watch it at full speed and at 1/4 speed.** Full speed shows whether the change feels calm. 1/4 speed shows what actually moves.
- **Judge the decisions here, not on static boards.**
  - Example: a drawer sidebar against a full-screen sidebar only resolved once it was in motion.
- **Check that the thing the person was looking at stays put**, and that everything else moves around it.

## Riffs

- **Ask for several distinct takes on a tricky screen**, not one answer.
  - Put them side by side on one canvas at real size, and pick the best.
  - Vary one thing at a time across the riffs, e.g. pane ratio, where controls go, or what the leading column holds, so the comparison means something.
- **Trust the eye over maths.**
  - The space is asymmetric: the rail is on one side and the hand on the other.
  - Spacing that's symmetric on paper can look cramped.
- **Finish on a device.**
  - Once a direction is chosen, build it and hold it.
  - The simulator doesn't show what your hand covers.

## Keep the decisions in one place

Record the choices in the project's CLAUDE.md or a project skill, so new screens follow them without re-deriving them:

- breakpoints
- pane widths
- pairings
- rail priorities
- what goes in "…"
- the tent layout
