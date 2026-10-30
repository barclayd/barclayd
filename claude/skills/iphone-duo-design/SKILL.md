---
name: iphone-duo-design
description: Design and adapt iOS apps for iPhone Duo, Apple's foldable with a compact outer display and a large inner display. Use when designing screens or mock-ups for iPhone Duo, adapting an existing iPhone or iPad app to it, laying out the vertical rail of toolbars and tab bars, building side-by-side panes for the open phone, designing tent mode (the outer display in landscape), handling the fold, the cameras or reserved regions, or fixing SwiftUI layout bugs that only show up on the Duo.
---

# iPhone Duo design

iPhone Duo is still an iPhone, so the usual iOS patterns apply. Two things are new:

- **One app, many shapes.** The same session moves between a compact outer display and a large inner display as the phone opens, closes, folds and rotates.
- **Bars move to the side.** Toolbars, tab bars and the status bar run down a vertical rail, not across the top and bottom.

Aim for **one narrow layout and one wide layout that flex between them**, not a custom layout per pose. Make the journey continuous: whatever is on screen when the phone is closed should still be there, in the same order, when it opens.

## The device

| Pose | Display | Size (pt, approx.) | Bars | Camera |
|---|---|---|---|---|
| Closed, portrait | outer | 466 × 678 | rail on the trailing edge | corner, at the top of the rail, always visible |
| Closed landscape and tent ("standing on its edges") | outer | 678 × 466 | rail on the trailing edge | corner, at the bottom of the rail |
| Open, landscape (like a book) | inner | 951 × 669 | rail on the trailing edge | behind the display, only shows while in use |
| Open, portrait | inner | 669 × 951 | standard horizontal bars | as above |
| Partially folded, like a book or a laptop | inner | divided by the fold | as open | as above |
| Split View multitasking | inner, shared | each app gets a part | each app's rail is on its outer edge | |

- **Where the sizes come from:** the Duo simulator in Device Hub. The outer display is 1398 × 2034 px at 3x.
- **Closed content width:** with the rail, closed content is about 394pt wide.
- **Don't hard-code any of these sizes.** Lay out from size classes, safe areas and container size.

- **Rail contents, top to bottom:** the Dynamic Island, the status bar, the toolbar (including Back/Close), then the tab bar.
  - It stays aligned with the hardware, so it keeps its position relative to the outer camera.
  - It doesn't flip in right-to-left languages.
- **Reserved regions** are areas your content keeps clear of:
  - **The outer camera.** Always active. It grows into the Dynamic Island for Live Activities.
  - **The inner camera.** Only active while it's in use, and the UI moves aside when it is.
  - **The fold.** A division that's only active while the phone is partially open.

## Mental model

1. **Your app is a path of screens, from general to specific.**
   - Closed, the phone shows the last screen. Open, it shows the last two side by side.
   - The order never changes: general on the leading side, specific on the trailing side.
   - Example: Mail shows the list or the email when closed, and both when open.
2. **Design journeys, not screens.** Ask what someone was doing on the closed phone and what will be useful when they unfold it.
   - Whatever was open should land beside its parent, not reset.
   - Example: in Claude, an artefact opened on the closed Duo moves next to the chat when the phone unfolds.
3. **Offer side by side *and* full screen, with one button between them.** The same button takes a pane full screen and brings it back.
4. **Keep panels predictable.**
   - Allow a small, fixed set of pairings, e.g. sidebar + main, or main + detail.
   - Give every pane that can close its own Close button.
   - Make it obvious how to step back.
5. **Keep input predictable while navigating.**
   - Tapping a destination that's a list opens it on the leading side. The trailing content stays until something is picked.
   - Anything temporarily pushed aside comes back when the thing that displaced it closes.
6. **Judge layouts while they move.** Screenshots lie on a device that changes shape.
   - Watch the phone open and close, at full speed and at 1/4 speed.
   - Example: in Claude, a drawer looked better in static shots, but a full-screen sidebar felt more consistent once they watched the phone unfold.

## Bars and the rail

- **Use the system bars.** That means `.toolbar` on a `NavigationStack` or `NavigationSplitView`, and `TabView`. Custom bars don't move to the rail.
- **Follow the order from the top of the rail:**
  1. Back or Close
  2. The prominent action (Done)
  3. The remaining groups, kept in their original groupings
- **Plan the overflow.**
  - Items overflow from the bottom up into the system "…" menu.
  - Give frequent actions and anything that shows status (badges) the highest priority, so they overflow last.
  - Show only the most useful items. Claude shows two on a plain chat in landscape.
  - Put destructive actions such as Delete in "…" so they can't be tapped by accident.
- **Give every item a title and a symbol.**
  - Items with only a title, and custom views, never appear in the rail.
  - Prefer symbols. Text buttons stay in horizontal bars.
- **Pick a compression behaviour when space runs out:**
  - Navigation-led screens keep the tab bar and overflow the toolbar items. This is the default.
  - Task-led screens minimise the tab bar and keep the toolbar.
- **Use the system overflow menu.** Don't build your own. Reserve the ellipsis for overflow, and give every other menu a distinct symbol.
- **Keep pane controls with their pane.**
  - The rail belongs to the trailing pane.
  - Controls that act on the leading pane sit at the top of that pane, like Mail's list controls.
- **Don't override the rail.** Opt out of vertical bars only for UIs that are better with horizontal ones, like a full-screen video player or a calculator. Make it a stable choice, not something that changes per view.
- **Think about reach and what the hand covers.**
  - The bottom-right of the open Duo is hard to see while holding it.
  - Closed, put the main create action at the bottom of the rail, by the thumb.

## Content

- **Keep text and buttons clear of the rail, but run backgrounds under it.**
  - Colour, hero images and diff/code backgrounds carry on underneath, so the pane reads as one surface.
  - Text and buttons never go underneath.
- **Go full width for immersive, non-scrolling views**, such as maps, video, games and calculators, as long as nothing hits the Dynamic Island or the status bar.
  - You can mix the two: a full-width header or background, with scrolling content inset.
- **Keep state identical across displays:** scroll position, selection, map position, drafts and playback.
  - Folding should only change how much room each pane gets.
- **Avoid big rearrangements as the phone folds.** Move only what's needed to stay visible and tappable.
  - In grids, prefer an even number of columns so content divides at the fold.
  - Scroll views don't split around the fold, so a row can straddle it.
- **The space is asymmetric, so trust your eye over maths.**
  - Claude widened the gap between sidebar and chat in landscape because the symmetric one felt cramped.
  - When a single column of cards gets the whole open screen, cap it at a readable width (about 640pt).
- **Games** can lock to one orientation but must still fill the screen.
  - Prefer changing the aspect ratio over letterboxing.
  - If you must letterbox, put artwork in the bars.

## Tent mode

The phone stands folded on a desk with the hinge on top, so the outer display is in landscape (about 678 × 466pt). It's viewed at arm's length and touched occasionally.

- Reflow the compact layout into two columns rather than inventing a third layout.
- Make the one number that matters big, and keep the same rail controls as closed.

For more, see [references/tent-mode.md](references/tent-mode.md).

## Workflow for adapting an app

1. **Map the path.**
   - List the screens from general to specific.
   - For each step, decide what shows when closed (that screen) and when open (it and its parent).
   - Decide what happens to anything open mid-journey when the phone opens or closes.
2. **Audit the bars.** For every toolbar item, set:
   - its title and symbol
   - its group
   - its priority
   - whether it belongs in "…"
   - whether it's a pane control rather than a rail item
3. **Design narrow, then wide, then tent.** Narrow and wide are the real layouts. Tent is narrow reflowed.
4. **Mock up and prototype in motion.** See [references/mockups.md](references/mockups.md).
5. **Build with system containers first:**
   - `NavigationSplitView`
   - `TabView`
   - `ArrangementView`
   - system toolbars

   Then handle the cases they don't cover. See [references/swiftui.md](references/swiftui.md) for the APIs, patterns and pitfalls.
6. **Test every pose:**
   - closed portrait
   - closed landscape / tent
   - open landscape
   - open portrait
   - partially folded both ways
   - Split View
   - opening and closing mid-task
   - right-to-left languages

   Use Device Hub in Xcode, then a real device. The simulator doesn't show you what your hand covers.

## Checklist

- [ ] Built with the latest Xcode (apps built with Xcode 26 or earlier don't extend under the status bar and camera)
- [ ] No fixed widths or device-size checks. Layout comes from size classes, safe areas and container size
- [ ] Closed shows the last screen and open shows the last two, in the same order
- [ ] Opening and closing mid-task keeps state: scroll, selection, map position, drafts
- [ ] Panes beside each other can go full screen and back with one button, and each can close
- [ ] Every toolbar item has a title and a symbol
- [ ] Back/Close sits at the top of the rail
- [ ] Priorities are set, and destructive actions are in "…"
- [ ] Pane-specific controls sit with their pane, not on the rail
- [ ] Text and buttons are clear of the rail and the cameras. Backgrounds run underneath
- [ ] Nothing important lands in the fold when partially open, and grids divide evenly
- [ ] Tent layout is readable at arm's length, with nothing important below the fold of the screen
- [ ] Tested on a real device in every pose

## Sources

- [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), Apple HIG ([JSON](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/designing-for-iphone-duo.json): the page itself is client-rendered)
- [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo), Apple developer docs
- Tech talks:
  - [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466)
  - [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462)
  - [Strike a pose with adaptive layouts on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111463)
- [How Claude for iPhone Duo was built](https://x.com/RobertJBye/status/2113808129368760750), a thread by Robert Bye (Anthropic)
- [Apple Design Resources](https://developer.apple.com/design/resources/) for margins and safe areas
