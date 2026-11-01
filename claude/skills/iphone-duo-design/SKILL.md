---
name: iphone-duo-design
description: Design and adapt iOS apps for iPhone Duo, Apple's foldable with a compact outer display and a large inner display. Use when designing screens or mock-ups for iPhone Duo, adapting an existing iPhone or iPad app to it, laying out the vertical rail of toolbars and tab bars, building side-by-side panes for the open phone, designing tent mode (the outer display in landscape) or the tabletop pose (half open on a table like a laptop), handling the fold, sheets, Split View, the cameras or reserved regions, or fixing SwiftUI layout bugs that only show up on the Duo.
---

# iPhone Duo design

iPhone Duo is still an iPhone, so the usual iOS patterns apply. Two things are new:

- **One app, many shapes.** The same session moves between a compact outer display and a large inner display as the phone opens, closes, folds and rotates.
- **Bars move to the side.** Toolbars, tab bars and the status bar run down a vertical rail, not across the top and bottom.

Aim for **one narrow layout and one wide layout that flex between them**, not a custom layout per pose. Narrow is compact width (the outer display) and wide is regular width (the inner display). The one pose-specific layout Apple suggests is an optional [tabletop layout](#tabletop-pose). Make the journey continuous: whatever is on screen when the phone is closed should still be there, in the same order, when it opens.

## The device

| Pose | Display | Size (pt, approx.) | Bars | Camera |
|---|---|---|---|---|
| Closed, portrait | outer | 466 × 678 | rail on the trailing edge | corner, at the top of the rail, always visible |
| Closed landscape and tent ("standing on its edges") | outer | 678 × 466 | rail on the trailing edge | corner, at the bottom of the rail |
| Open, landscape (like a book) | inner | 951 × 669 | rail on the trailing edge | behind the display, only shows while in use |
| Open, portrait | inner | 669 × 951 | standard horizontal bars | as above |
| Partially folded, like a book | inner, landscape | curve down the middle | rail on the trailing edge, controls move to either side of the curve | as above |
| Partially folded on a table, like a laptop ([tabletop](#tabletop-pose)) | inner, portrait | curve across the middle | horizontal bars, interactive elements move to the bottom half | as above |
| Split View multitasking | inner, shared 50/50 | each app gets half, and each half works on its own | each app's rail is on its outer edge, so the left-hand app's rail is on the left | |

- **Where the sizes come from:** the Duo simulator in Device Hub. The outer display is 1398 × 2034 px at 3x.
- **Closed content width:** with the rail, closed content is about 394pt wide.
- **Target two size classes, not these sizes.** The outer display is compact width and the inner display is regular width.
  - Don't use fixed widths, breakpoints or metrics tied to one screen.
  - Build from layout margins and horizontal safe area insets. An app that's already freely resizable mostly adapts on its own.
- **Height changes at runtime too.** Picture in Picture can be pinned to the top of the screen, and your app shrinks to fit what's left. Partially fold the phone and the video grows to half the screen, so the app resizes again, live.

- **Rail contents, top to bottom:** the Dynamic Island, the status bar, the toolbar (including Back/Close), then the tab bar.
  - It stays aligned with the hardware, so it keeps its position relative to the outer camera.
  - It doesn't flip in right-to-left languages.
  - The exception is Split View, where each app's rail sits on its outer edge, away from the centre.
  - It gets shorter mid-session. The Dynamic Island grows down the rail as Live Activities arrive, so toolbar items can overflow into "…" without the pose changing.
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
- **Map an existing iPhone design across by position:**
  - Items in the top navigation bar go to the top of the rail.
  - Items in the bottom toolbar go to the bottom of the rail.
  - The tab bar stays at the bottom.
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
  - Prefer symbols. Items too wide for the rail, such as text buttons and segmented controls, stay in the navigation bar.
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

- **Centre content on the area beside the rail, not on the whole screen.** Most content needs an offset so the rail doesn't hide it. Align to the horizontal safe area insets and the offset comes for free.
- **Keep text and buttons clear of the rail, but run backgrounds under it.**
  - Colour, hero images and diff/code backgrounds carry on underneath, so the pane reads as one surface.
  - Text and buttons never go underneath.
- **Go full width for immersive, non-scrolling views**, such as maps, video, games and calculators. Only do it when you're sure no interactive element ends up under the rail, the Dynamic Island or the status bar.
  - You can mix the two: a full-width header or background, with scrolling content inset.
  - Then put every interactive element in the inset, scrolling layer so nothing gets covered.
- **Keep state identical across displays:** scroll position, selection, map position, drafts and playback.
  - Folding should only change how much room each pane gets.
- **The space is asymmetric, so trust your eye over maths.**
  - Claude widened the gap between sidebar and chat in landscape because the symmetric one felt cramped.
  - When a single column of cards gets the whole open screen, cap it at a readable width (about 640pt).
- **Games** can lock to one orientation but must still fill the screen.
  - Prefer changing the aspect ratio over letterboxing.
  - If you must letterbox, put artwork in the bars.

## The inner display

Don't ship a stretched-out iPhone app. Pick the approach that suits the content:

1. **Split view.** Show two levels of the hierarchy at once, as in the mental model above. The hierarchy itself must be the same inside and out.
2. **Reflow for the width.** A vertically stacked layout rearranges itself into two columns when there's room, like Music.
3. **Tab bar as a sidebar.** Best for information-dense apps like Health, and not right for every app. Use `TabView` with `.tabViewStyle(.sidebarAdaptable)`.

Whichever you pick, never limit a feature to the inner or outer display. People open and close the phone mid-task, so the app must stay predictable.

## The fold

Partially open, the display curves through the centre. Treat the curve as a natural divider for the layout.

- **Keep interactive elements out of the curve.** Buttons are hard to tap when they land in it.
  - Like a book: text and images shift away from the curve, and controls move to either side.
  - Like a laptop: interactive elements move to the bottom half, where they're easy to reach and tapping doesn't rock the phone.
- **Scrolling content doesn't need to avoid it.** Scroll views don't split around the fold, so a row can straddle it.
- **Use system components to get fold avoidance for free.** Sheets, alerts, menus, toolbar buttons and more nudge themselves aside. Custom floating controls don't, so check them with `reservedRegions` (see [references/swiftui.md](references/swiftui.md)).
- **Avoid big rearrangements as the phone folds.** Move only what's needed to stay visible and tappable.
  - In grids, prefer an even number of columns so content divides at the fold.

## Sheets

- **Outer display:** the sheet's controls move to the rail by default.
  - A sheet with a single toolbar button can opt out with `.toolbarVerticalBehavior(.disabled)`. It then stops just short of the front camera, and the status bar moves to fit.
- **Inner display:** sheets use horizontal bars, in landscape and portrait.
- **Partially folded:** sheets slide to one side so they don't sit in the fold. Alerts and menus do the same.

## Tabletop pose

The phone sits on a table like a laptop: the inner display in portrait, partially open, with the curve across the middle. It's good for hands-free use, such as video calls and recipe or workout videos. This is the one optional pose-specific layout Apple suggests.

- **Put media on top and tappable controls on the stable bottom half.**
  - A split `ArrangementView` puts the primary on top in portrait, so make the media the primary.
- **Keep the same controls and hierarchy as every other pose.** Never tie a feature to this pose. It's a rearrangement, not a mode.

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
3. **Design narrow, then wide, then the optional poses.** Narrow and wide are the real layouts. Tent is narrow reflowed. Tabletop, if you do one, is wide with media above the curve and controls below it.
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
   - Split View, on the left half and the right half
   - Picture in Picture pinned to the top, flat and partially folded
   - a Live Activity arriving while the rail is full
   - opening and closing mid-task
   - right-to-left languages

   Use Device Hub in Xcode, then a real device. The simulator doesn't show you what your hand covers.

## Checklist

- [ ] Built with the latest Xcode (apps built with Xcode 26 or earlier don't extend under the status bar and camera)
- [ ] Layout targets compact width (outer) and regular width (inner), with no fixed widths, breakpoints or device-size checks
- [ ] Closed shows the last screen and open shows the last two, in the same order
- [ ] The inner display uses a split view, a reflowed layout or a sidebar, not a stretched iPhone layout
- [ ] Every feature works in every pose and on both displays
- [ ] Opening and closing mid-task keeps state: scroll, selection, map position, drafts
- [ ] Panes beside each other can go full screen and back with one button, and each can close
- [ ] Every toolbar item has a title and a symbol. Text buttons and segmented controls stay in the navigation bar
- [ ] Back/Close sits at the top of the rail
- [ ] Priorities are set, and destructive actions are in "…"
- [ ] Pane-specific controls sit with their pane, not on the rail
- [ ] Content is centred beside the rail, not on the whole screen
- [ ] Text and buttons are clear of the rail and the cameras. Backgrounds run underneath
- [ ] Nothing you tap sits in the fold when partially open, custom controls included, and grids divide evenly
- [ ] Works in Split View on either half, and with Picture in Picture pinned to the top
- [ ] Any tabletop layout has the same controls and hierarchy as every other pose
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
