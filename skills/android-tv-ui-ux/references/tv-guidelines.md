# TV design and implementation notes

Official sources were checked on 2026-10-23. Recheck API signatures against the target project's pinned versions when implementing. Numbers labelled project convention below are starting points for inspection, not Android certification requirements.

## Remote navigation and focus

The [TV navigation guide](https://developer.android.com/training/tv/get-started/navigation) and [navigation design guide](https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv) require predictable four-direction navigation and access to every actionable element. Start with Android's directional search; add explicit neighbors only where spatial ordering is ambiguous. Test short rows, incomplete last rows, wrapping, scrolling, RTL and rapid/repeated key presses. A focus move must scroll its target into view; neither decoration nor a disabled action should trap navigation.

The [TV focus system](https://developer.android.com/design/ui/tv/guides/styles/focus-system) describes scale, outline, glow and colour. Give focused, pressed, selected and disabled states different meanings. A persistent selected tab is not necessarily the current remote focus. Keep the focus outline/glass visible above artwork, with room for scale and glow inside clipping ancestors. Do not rely on colour alone.

In this repository, inspect these existing owners before changing behavior:

| Concern | Existing owner under `launcher/app/src/main/` |
|---|---|
| Tile identity, return focus, Home and Back | `java/com/gathin/tvhome/MainActivity.java` (`lastFocusedKey`, `focusTile`, `onTileFocused`) |
| Grid directional moves | `java/com/gathin/tvhome/GridNavigation.java` |
| Tile binding and artwork | `java/com/gathin/tvhome/AppAdapter.java`, `HeroArt.java` |
| Library loading and empty content | `java/com/gathin/tvhome/LibraryLoads.java`, `AppLibraryDialog.java` |
| Focus animation and reduced motion | `java/com/gathin/tvhome/GlassView.java`, `Motion.java`; existing theme keys |
| Margins, labels and localized layouts | `res/layout/`, `res/layout-iw/`, `res/values*/` |

Restore by stable package/item identity after returning from an app, dismissing a dialog or refreshing the library. If that item disappeared, choose the nearest surviving item, then a reachable library/settings action when there are no items. Request focus after the target is attached and laid out; do not steal focus on every data bind or animation frame. Record runtime return, configuration change and process recreation as separate cases.

## Back and the HOME role

The [official Back guidance](https://developer.android.com/training/tv/get-started/navigation#back-navigation) calls for a predictable route back, without confirmation gating or menu loops. Dismiss the current popup/edit/reorder mode before leaving its parent and restore its invoker. Make Cancel available alongside a destructive action.

This project's main Activity is HOME: `MainActivity.onBackPressed()` deliberately does nothing at the root. Preserve that behavior while respecting each dialog/edit-mode owner; do not copy ordinary app code that starts HOME or repeatedly finishes/relaunches itself. A separately built ordinary TV app should unwind to its root and system Home. Distinguish those roles before defining a Back contract. Do not add an on-screen Back button by default or consume all Back events globally.

## Ten-foot readability and safe area

The [Compose TV layout guide](https://developer.android.com/training/tv/playback/compose/layouts) uses landscape layouts, `dp` dimensions and `sp` type, intended for viewing at about ten feet. Keep essential controls and text within an overscan-safe area: its 960 x 540 dp example leaves 48 dp horizontally and 27 dp vertically (5% per edge). This is a safe-area starting point, not a fixed 48 physical pixels at every resolution. Let decorative backgrounds extend to all edges. Include the focused enlargement and glow when checking clipping.

The [TV typography guide](https://developer.android.com/design/ui/tv/guides/styles/typography) favors clear, sufficiently large sans-serif text with substantial strokes and distinguishable glyphs. Keep the existing Outfit identity where readable; do not force Roboto or mobile font sizes into this launcher. Project starting points for a new screen: 18-24 sp body/actions, 28-40 sp titles; confirm at actual viewing distance, text scaling and with long translations. Avoid long paragraphs, thin weights and text embedded in wallpaper.

## Contrast, accessibility and motion

The [Android accessibility guide](https://developer.android.com/guide/topics/ui/accessibility/apps) recommends at least 4.5:1 for smaller text and 3:1 for qualifying large text (18 sp normal or 14 sp bold). Use 4.5:1 for all operational labels here as a conservative project target. Use at least 3:1 for meaningful icons and control indicators against adjacent surfaces, following [Android's accessibility design guidance](https://developer.android.com/design/ui/mobile/guides/foundations/accessibility). Check actual composited pixels: a palette ratio alone does not establish contrast over a wallpaper, gradient or translucent pill. Scrims or opaque surfaces are valid remedies.

The [TV accessibility guide](https://developer.android.com/training/tv/accessibility) calls for TalkBack support, useful labels and text scaling. Give icon-only actions localized names, expose roles, checked/disabled state and meaningful errors, and avoid announcing decorative art. In Views, inspect `contentDescription`, accessibility importance and grouping; in Compose inspect semantics. Screen-reader focus is separate from D-pad focus and must also be tested. Test large text without cutting off actions. Keep status comprehensible without colour or motion; use the existing `reduced_motion` switch rather than inventing a second animation system.

## Loading, empty and error states

The [Android UI state guidance](https://developer.android.com/topic/architecture/ui-layer) and [loading-state reference](https://developer.android.com/topic/libraries/architecture/paging/load-state) distinguish loading, content and failure. The following are project UX conventions applied to the local app library, package/artwork loading and configuration errors; they do not require adding Paging, network access or a new state framework:

| State | Display and remote contract |
|---|---|
| Initial loading | A concise status, stable layout, and reachable escape/settings where applicable; skeletons are decorative and not focusable. |
| Refresh with content | Keep usable items and their focused ID; show unobtrusive progress. Do not bounce focus to the first item. |
| Empty | Explain that no eligible apps/items are present, distinguish filters/removed apps, offer an existing library/settings action. No focus request to a nonexistent tile. |
| Error | Plain-language cause and recovery action (Retry or existing Settings); preserve content where safe. If Retry is absent/unavailable, explain the alternative. Back remains usable. |
| Ready after recovery | Restore the original ID if still available; otherwise use the documented fallback, with no automatic launch or repeated error loop. |

## Compose for TV, only for an authorized Compose surface

[Compose for TV](https://developer.android.com/training/tv/playback/compose) provides `androidx.tv.material3` components with TV focus behavior; mobile Material components and their theme are not interchangeable. Use general Compose foundation lazy layouts with TV Material controls; do not copy deprecated TV lazy-layout tutorials or blindly upgrade dependencies.

For [initial focus](https://developer.android.com/develop/ui/compose/touch-input/focus/request-focus), remember a `FocusRequester`, attach it before the focus target, and request focus in a controlled effect once the target exists. For [runtime restoration](https://developer.android.com/develop/ui/compose/touch-input/focus/focus-restoration), use `focusRestorer` on the group/container; lazy lists already form groups, ordinary Row/Column containers also need `focusGroup`. Provide a real, attached fallback. The overload differs in older Compose versions, so confirm the signature rather than pasting current examples into an older build. Use stable lazy item keys and save the selected ID/scroll position for [state recreation](https://developer.android.com/develop/ui/compose/state-saving); `focusRestorer` alone does not provide process-death persistence. Use lifecycle-aware Back handling that respects the current overlay and navigation owner.
