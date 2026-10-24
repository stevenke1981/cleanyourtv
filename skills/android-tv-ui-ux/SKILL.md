---
name: android-tv-ui-ux
description: Design or refine CleanYourTV Android TV UI/UX, remote D-pad navigation, focus restoration, Back behavior, ten-foot readability, accessible states, and theme acceptance. Use for TV screens or UX changes; use android-tv-image-assets for generated artwork and icon exports.
---

# Android TV UI/UX

Read the repository's `AGENTS.md` and the files being changed. This launcher is plain Java with RecyclerView, minSdk 26, no Compose and no INTERNET permission. Keep that architecture and the small APK budget; a Compose reference is not authorization to migrate it.

## Route the request

- For colours, wallpaper, dock or columns, read `themes/README.md` and use existing theme keys first. Keep untested concepts outside `themes/`: a theme there requires a genuine real-TV screenshot.
- For navigation or screen behavior, read [TV guidelines](references/tv-guidelines.md), then inspect `MainActivity.java`, `GridNavigation.java`, `AppAdapter.java` and the relevant dialog/layout. Change only the requested behavior.
- For a separate TV app outside `launcher/`, use the guidelines and the checklist but skip the launcher file table and the HOME rules; that app's Back reaches system Home.
- For a separately authorized Compose TV surface, read the Compose section of the guidelines and check its actual dependency versions before choosing APIs.
- For background art, launcher icons, banners or `.ico` exports, use [android-tv-image-assets](../android-tv-image-assets/SKILL.md).

## Work through the screen

1. Identify the screen, user goal, entry focus, directional neighbors, scroll behavior, Back destination and focus-restoration key. Use stable app/package or item IDs, not list indices alone.
2. Specify default, focused, pressed, selected and disabled appearances. Selection and focus are different. Preserve a visible focus indicator during animation and at every edge.
3. Specify loading, content, empty and error states, including the reachable action and what happens to focus when data changes. Preserve useful existing content on refresh.
4. Check the safe margins, text size, contrast, screen-reader labels and motion that the change affects. Reuse the project's existing motion/theme controls.
5. Apply the smallest change and run the checks it affects. Fix observed errors and retest locally; finish with one light diff check.

Use the [acceptance checklist](references/acceptance.md) to record evidence. Its scope table picks the rows a change affects; a colour or copy change needs three rows, not the whole list. Report PASS, FAIL or NOT_RUN per recorded row. Static inspection, a mockup or a generated image does not establish D-pad or real-TV acceptance.

For this HOME launcher, preserve its existing root Back behavior; ordinary app guidance to exit to system Home must not relaunch Home recursively. Do not change Home interception or install safety as a side effect of UX work.

Return the changed files, relevant checks and actual device/emulator evidence. Leave UI acceptance NOT_RUN when no device was operated. Do not deploy, install, push a theme, publish or use GitHub Actions unless separately authorized; this skill does not grant those actions.
