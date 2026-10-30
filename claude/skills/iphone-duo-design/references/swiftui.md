# SwiftUI on iPhone Duo

## APIs

Most of these need iOS 27.1. `visibilityPriority`, `ToolbarOverflowMenu` and `topBarPinnedTrailing` arrived in 27.0. If you deploy to anything earlier, wrap them in `if #available`.

| Need | SwiftUI | UIKit |
|---|---|---|
| Two related views that follow the pose and fold | `ArrangementView { primary } secondary: { … }` with `.arrangementViewStyle(.split)` or `.overlay` | `UIArrangementViewController` |
| Limit an arrangement to one axis | `.arrangementViewStyle(.split.axes(.horizontal))` | `updateArrangement(.split.axes(.horizontal))` |
| Size the panes of a split arrangement | `.splitArrangementLayoutRatio(0.3)`, `.splitArrangementLayoutSize(…)` on the primary | |
| Which side the primary takes when folded (overlay) | `.overlayArrangementEdge(.leading)` | |
| Where the cameras and the fold are | `GeometryReader` → `proxy.reservedRegions(kind: .occlusion / .division, options: .includeInactive)` | `view.reservedRegions(kind:options:)` |
| Whether the rail is used here, and on which side | `@Environment(\.toolbarVerticalEdge)` (`HorizontalEdge?`, `nil` = never vertical) | `traitCollection.verticalBarEdge` |
| Opt a screen out of the rail | `.toolbarVerticalBehavior(.disabled)` | `preferredVerticalBarBehavior` |
| Keep an item out of the rail, or prefer it there | `.axisBehavior(.horizontalOnly / .verticalPreferred)` on the `ToolbarItem` | `UIBarButtonItem.axisBehavior` |
| Overflow order | `.visibilityPriority(.high / .low)` on a `ToolbarItem` or group, or `ToolbarItemVisibilityPriority(higherThan:)` | `visibilityPriority` |
| Always in the "…" menu | `ToolbarOverflowMenu { Button(…) }` | `navigationItem.additionalOverflowItems` |
| Keep the tab bar or the toolbar when squeezed | `.toolbarVerticalCompressionBehavior(.prefersTabBar / .prefersToolbarItems)` | `UIVerticalBarCompressionBehavior` |
| Prominent action, e.g. Done | `ToolbarItem(placement: .topBarPinnedTrailing)` | `navigationItem.pinnedTrailingGroup` |
| Custom Back or Close | `ToolbarItem(placement: .cancellationAction)` | `navigationItem.leadingItemGroups` |
| Hero image under the rail | `.backgroundExtensionEffect()` | `UIBackgroundExtensionView` |
| Where a sheet sits on the inner display | `.presentationPlacement(_:)` | `UISheetPresentationController.preferredPlacement` |
| Sidebar and detail | `NavigationSplitView` | `UISplitViewController` |

### How the system chooses horizontal or vertical bars

- **Inspectors** are always horizontal.
- **Split views with several columns showing:** the sidebar and content columns get horizontal bars, and the detail column gets the rail.
- **Sheets:**
  - On the outer display they're vertical by default.
  - On the inner display they're horizontal for centred or leading placements, and vertical for trailing ones.
- **Which view's preference wins:**
  - `NavigationStack` uses the top view.
  - `TabView` uses the selected tab.
  - `NavigationSplitView` uses the trailing-most column.

### How an item is drawn

- **In the rail:** icon only.
- **In a horizontal bar:** icon or title, preferring the icon.
- **In the overflow menu:** icon and title.
- **Never in the rail:** an item with only a title, or one with a custom view.

So write `Button("Settings", systemImage: "gearshape") { … }`, not `Button { } label: { Image(…) }`.

### ArrangementView rules

- **Split arrangement:**
  - Landscape puts the primary on the leading side. Portrait puts it on top.
  - **The closed phone in landscape (and tent) shows only the primary**, so make the primary the one worth seeing on its own.
- **Overlay arrangement:**
  - Flat, the primary sits on top of the secondary.
  - Folded in landscape, the secondary goes leading and the primary trailing. Folded in portrait, the secondary goes on top.
- **Keep navigation outside it.**
  - Don't put an arrangement view inside a `ScrollView`, `List`, grid or `NavigationSplitView`.
  - Don't put a `NavigationSplitView` or `TabView` inside one.
  - An `HStack`/`VStack` pair maps to `.split`, and a `ZStack` maps to `.overlay`.

### ReservedRegion notes

- Most apps never need it: split views, tab bars, alerts, context menus and sheets already avoid the fold and the cameras.
- **When to check:** in custom overlays, floating controls, explicit frames and custom `Layout`s. Check in the view that positions the content, so the coordinates match.
- **Frames:**
  - They're in the view's own coordinates, with (0, 0) at its top-leading corner.
  - They already include the region's margins.
  - They're mirrored for right-to-left by default. Pass `layoutDirectionBehavior: .fixed` for unmirrored ones.
- **Inactive regions:** pass `.includeInactive` and leave room for them, so the layout doesn't jump when someone folds the phone or starts the inner camera.
- **Custom `Layout`:** `bounds` in `placeSubviews` doesn't always start at (0, 0). Do the maths from zero, then add `bounds.origin` when placing.

## Patterns for a hand-rolled two-pane layout

Prefer `NavigationSplitView` or `ArrangementView` where they fit. When an app needs a home column with a page beside it, these patterns held up on a real device.

### Measure the container, not the device

```swift
@State private var wide = false

content
    // Open, the inner display is wider than it is tall, with room for two panes side by side.
    .onGeometryChange(for: Bool.self) { $0.size.width >= 700 } action: { wide = $0 }
```

- **Closed:** about 394pt wide inside the rail.
- **Tent:** the outer display in landscape is 678pt before the rail. It sits just under 700, so a width check alone barely separates it from open.
- **If tent gets its own layout**, detect it explicitly rather than nudging the threshold:

```swift
enum Shape { case narrow, tent, wide }

.onGeometryChange(for: Shape.self) { size in
    if size.width >= 700 { .wide }
    else if size.width > size.height { .tent }
    else { .narrow }
} action: { shape = $0 }
```

- **"Tent" really means "short and landscape"**, so the same layout suits any iPhone in landscape.
- **Open portrait** (about 669pt wide) lands in `narrow` with these numbers. Decide deliberately whether it should show one pane or two stacked.
- **Log the size and both size classes in every pose** in Device Hub before you settle on thresholds.

### Hide panes, don't remove them

Keep the leading pane in the hierarchy and hide it, so its scroll position survives folding and unfolding:

```swift
let showsHome = page == nil || wide && !fullScreen

ZStack(alignment: .topLeading) {
    home
        .frame(width: wide ? homeWidth : nil)
        .opacity(showsHome ? 1 : 0)
        .allowsHitTesting(showsHome)
        .accessibilityHidden(!showsHome)

    if let page {
        pageView(page)
            .transition(.move(edge: wide ? .trailing : .bottom))
            .padding(.leading, wide && showsHome ? homeWidth : 0)
    }
}
```

`if wide { … } else { … }` builds a different view tree. Folding then throws away scroll position, map camera, text field focus and so on.

### Apply both kinds of chrome, always

A page shown full screen puts Close and its title in the bar. Beside another pane, the bar belongs to the other pane, so the page floats its own controls instead. Apply both every time, with one of them empty, so folding doesn't rebuild the page:

```swift
enum PageChrome {
    case bar
    case pane(fullScreen: Binding<Bool>)
    var isBar: Bool { if case .bar = self { true } else { false } }
}

content
    .navigationTitle(chrome.isBar ? title : "")
    .toolbar {
        if chrome.isBar {
            ToolbarItem(placement: .topBarTrailing) { Button(role: .close, action: close) }
        }
    }
    .safeAreaInset(edge: .top, spacing: 0) {
        if case .pane(let fullScreen) = chrome {
            // Close, title and full screen, each in glass, e.g. `.glassEffect(.regular.interactive(), in: .circle)`
            PaneControls(title: title, fullScreen: fullScreen, close: close)
        }
    }
```

The full-screen button toggles both ways. Swap its symbol between `arrow.up.left.and.arrow.down.right` and `arrow.down.right.and.arrow.up.left`.

### Pitfalls seen on the device

- **Scrolling one pane drags the other.**
  - **Cause:** both panes share one navigation bar. When either pane scrolls, the bar minimises and takes the other pane's top edge, and anything in the bar, with it.
  - **Fix:** pin the bar while the panes are side by side.

  ```swift
  @ViewBuilder func barStaysPut(_ staysPut: Bool) -> some View {
      if #available(iOS 27.0, *) {
          toolbarMinimizationBehavior(staysPut ? .never : .automatic, for: .navigationBar)
      } else { self }
  }
  ```

- **A liquid glass "chin" appears at the top of a pane.**
  - **Cause:** the scroll edge effect draws a translucent band under the bar, even over a pane whose controls bring their own glass.
  - **Fix:** hide the top edge effect on panes that sit beside each other.

  ```swift
  .scrollEdgeEffectHidden(wide, for: .top)  // the leading pane
  .scrollEdgeEffectHidden(true, for: .top)  // a trailing pane with floating controls
  ```

- **A badge in the bar gets a second glass background.**
  - **Cause:** a view that brings its own glass, such as a status pill that turns solid on error, still gets the bar's shared background.
  - **Fix:** `.sharedBackgroundVisibility(.hidden)` on its `ToolbarItem`.
- **A column of cards stretches across the whole open screen.**
  - **Fix:** `frame(maxWidth: 640).frame(maxWidth: .infinity)` when a page gets the whole wide screen.
- **A page slides up from the bottom when it should come in beside its parent.**
  - **Fix:** `.transition(.move(edge: wide ? .trailing : .bottom))`.
- **Content is duplicated on both sides when open.**
  - **Fix:** split it, e.g. the hero and urgent cards on the leading side and the detail on the trailing side. Put it back together in one column when closed.
- **Toolbar items stay in a horizontal bar.**
  - **Cause:** they have no symbol, or they're a custom view.
  - **Fix:** give them both a title and a `systemImage`.
- **The app doesn't extend under the status bar and camera.**
  - **Cause:** it was built with Xcode 26 or earlier.
  - **Fix:** rebuild with the current Xcode.
