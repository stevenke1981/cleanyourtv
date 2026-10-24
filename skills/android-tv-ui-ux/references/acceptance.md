# Android TV acceptance record

Record only the rows the change can affect; the scope table below picks them. Use `PASS`, `FAIL` or `NOT_RUN` with one line of evidence each. Rows outside the scope need no entry and no reason. A checklist definition is not proof that it passed.

Record the commit, the screen and the TV model or emulator with its Android version. Add font scale, locale/RTL or accessibility settings only when a row tests them. Keep identifiers and private screenshots in ignored `work/` or `shots/`.

## Scope

| The change touches | Rows to record |
|---|---|
| Colours, drawables, text size or copy only | Contrast, Readability, Existing behavior |
| Layout, margins or a new view | The above plus Entry focus, Four directions, Safe area |
| Focus, key handling, Back or a dialog | Entry focus, Four directions, Back, Existing behavior; Repeated input if keys repeat or auto-advance |
| Data loading or list content | State transitions, Restoration, Existing behavior |
| Saved state or Activity lifecycle | Restoration, Recreation |
| Labels, roles or icon-only actions | Accessibility |
| Animation | Reduced motion |

Artwork, icons and banners are checked by [android-tv-image-assets](../../android-tv-image-assets/SKILL.md), not here.

## Rows

| Check | Procedure / expected observation |
|---|---|
| Entry focus | Cold-open and return; exactly one reachable action has a visible focus indicator. No animation-time focus theft. |
| Four directions | Reach every action in the changed area with Up/Down/Left/Right/OK from its edges; include an empty and a long list where the area has one. Scrolling reveals focused items. |
| Repeated input | Rapid presses and held D-pad do not skip into hidden UI, double-activate, lose focus or trap a row. |
| Restoration | Return from an app, popup or refresh to the same stable ID and scroll region; a removed item falls back to a usable target. |
| Recreation | Record runtime return separately from Activity/configuration/process recreation; restore state only to existing targets. |
| Back | Close popup/edit/reorder first, restore invoker, then follow the documented screen/root contract. HOME launcher has no finish/relaunch loop. An ordinary app reaches system Home. |
| State transitions | Each affected state (loading, content, empty, failure) has understandable text, a valid focus path and usable Back. Never focus a skeleton or missing tile. |
| Safe area | On one target mode, essential labels/actions and focus enlargement stay inside the safe bounds. Check another resolution only for pixel (`px`) dimensions or bitmaps. Full-bleed wallpaper remains full-bleed. |
| Readability | At about ten feet, changed titles and labels read clearly. Test large font scale or a long translation only when the change adds text or narrows its space. |
| Contrast | Compute changed foreground/background pairs, including focused and disabled states. Measure composited pixels only where text sits over wallpaper, a gradient or a translucent surface. |
| Accessibility | With TalkBack enabled, inspect names, roles, state and order of the changed controls; decorative artwork stays silent. |
| Reduced motion | Existing reduced-motion setting preserves feedback and navigation without essential bouncing or prolonged animation. |
| Existing behavior | The changed screen's other actions remain usable. |

Use the existing `tools/tv.py` screenshot/key workflow only when device operation is authorized; read its usage first. Real-remote long presses and accessibility-service buttons need a real press: injected keys alone do not prove them. Wait for the intended window and focus with a timeout before capturing evidence; a fixed delay is not proof of readiness. One screenshot can be evidence for several rows.

For a new `themes/` contribution, the repository requires a genuine Home screenshot from a real TV at 1280x720, JPEG, at most 300 KB; a generated mockup or emulator shot cannot satisfy that gate. With no actual TV/emulator operation, set the device rows to `NOT_RUN`.
