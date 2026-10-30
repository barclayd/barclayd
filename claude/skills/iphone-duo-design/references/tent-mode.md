# Tent mode

## The pose

- **What it is:** the phone stands folded on a desk, hinge on top, like a tent. To the app it's the outer display in landscape, the same as holding the closed phone sideways.
- **Size:** about 678 × 466pt. Height is the scarce dimension.
- **Rail:** stays on the hardware edge, on the right. The outer camera sits at the **bottom** of the rail, the opposite end to closed portrait.
- **How it's used:** glanced at from arm's length or across a room, on a desk, counter or bedside table, and touched now and then.
- **Typical uses:** anything that runs in the background of something else, such as a timer, a workout, a recipe step, a live score, a delivery or ride on a map, now playing, or a call.

## Layout

- **Reflow the compact layout into two columns.** Don't invent a third layout.
  - **Leading column:** the hero, i.e. the status, the big number or the map.
  - **Trailing column:** the supporting cards or list.
  - Keep the same content in the same order as closed. Things that were stacked now sit side by side.
- **Make it glanceable.**
  - The one number that matters goes at display size, roughly 2–3 times what you'd use closed. Scale it with Dynamic Type, e.g. `@ScaledMetric`.
  - Keep secondary text at body size or larger. Drop dense metadata rather than shrinking it.
- **Keep the important things on the first screen.** Nobody scrolls a phone standing on a desk. Scrolling is fine for secondary content in the trailing column.
- **Go full-bleed for immersive views** such as maps, video, camera and games.
  - Run them under the rail and float glass cards over them for the details.
  - Keep text and buttons clear of the rail and the camera region.
- **Choose the primary carefully in a split `ArrangementView`.** In closed landscape, and so in tent, it shows only the primary view, so make the primary the glanceable one.

## Controls

- **Keep the same rail controls as closed.**
  - Don't add, remove or reorder items just for tent.
  - Someone who switches poses should find everything where it was.
- **Expect more overflow.** The rail is about 466pt tall here, against about 678pt closed.
  - Set `visibilityPriority` so the essentials stay.
  - Let the system "…" take the rest, e.g. secondary filters or sort options.
  - Use "…" only when items genuinely don't fit. Never draw a custom one.
- **Use large targets.**
  - The phone is touched from a distance, often with one finger while it stands.
  - Prefer big tap targets for the primary action.
  - Avoid making swipes, long presses or precise drags the only way to do something.

## Don't

- **Don't draw a status bar, Dynamic Island or camera cutout** in the app. The system draws the rail, and it moves with the pose.
- **Don't detect tent by device model or hinge angle.** Lay out from the container size. Wider than tall and under the wide threshold means "short and landscape" (see [swiftui.md](swiftui.md)). The same layout then works on any iPhone held sideways.
- **Don't put the key information where the hand or the desk hides it.** In tent that means the very bottom edge, which is closest to the surface and furthest from the eye.

## Examples

| App | Leading column | Trailing column | Rail |
|---|---|---|---|
| Workout | Elapsed time and heart rate, large | Splits, pace, route preview | Pause, lap; End in "…" |
| Recipe | Current step, large, with its timer | Ingredients for this step, next step | Previous and next step, timers |
| Delivery or ride | Full-bleed map | Floating ETA card and driver details | Message, call |
| Stock or inventory | Count or status, large | Items needing attention | Refresh, add; filters in "…" |
