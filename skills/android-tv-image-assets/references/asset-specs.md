# Asset formats and project boundaries

Checked against official Android sources on 2026-10-23. Recheck these links when preparing a release. The current manifest points to `@mipmap/ic_launcher` and `@drawable/banner`; it currently uses `mipmap-xhdpi/ic_launcher.jpg` and `drawable-nodpi/banner.jpg`. Those existing files are context, not targets for automatic replacement.

## Android assets

The [official TV icon/banner guide](https://developer.android.com/design/ui/tv/guides/system/tv-app-icon-guidelines) requires both `android:icon` and `android:banner`. A square launcher icon and a 16:9 banner serve different surfaces. Its density sizes are:

| Density | Square launcher minimum | TV banner | Suggested directory |
|---|---|---|---|
| mdpi | 80x80 | 160x90 | `mipmap-mdpi` |
| hdpi | 120x120 | 240x135 | `mipmap-hdpi` |
| xhdpi | 160x160 | 320x180 | `mipmap-xhdpi` |
| xxhdpi | 240x240 | 480x270 | `mipmap-xxhdpi` |
| xxxhdpi | 320x320 | 640x360 | `mipmap-xxxhdpi` |

For legacy/fallback resources provide the xhdpi 320x180 banner and at least a 160x160 icon. [TV app quality TV-LB/TV-BN](https://developer.android.com/docs/quality-guidelines/tv-app-quality) also checks the banner's app name. Put the exact localized app name in each supported-language banner; a text-free wallpaper cannot substitute. Prefer deterministic text composition from the actual licensed project font after generation, then visually verify spelling at final size. A banner preview without that name is unfinished.

Keep raster PNG masters with alpha for standalone icons/foregrounds; preserve Android VectorDrawable XML when the source is vector. SVG may be an editable source, but it must be imported/converted to a supported Android drawable rather than referenced raw in the manifest. [Android drawable resources](https://developer.android.com/guide/topics/resources/drawable-resource) support bitmap and XML drawables; PNG is the lossless choice here. Opaque wallpaper/banner exports can be JPEG where appropriate. PNG masters are not Windows ICO files.

Adaptive icons are recommended for API 26+ and use XML plus separate foreground/background layers, usually in `mipmap-anydpi-v26`. Keep the background opaque and the foreground alpha; retain legacy fallbacks as needed. The TV guide describes a 72x72 safe zone; the [general adaptive icon guide](https://developer.android.com/develop/ui/views/launch/icon_design_adaptive) describes a 108x108 dp layer canvas and a central 66x66 dp safe region for important artwork. Use the central 66 dp region as this project's conservative cross-launcher target and inspect real masks; do not confuse dp with export pixels. Extend background art to the layer edges. Never put a complete square app plate in the foreground. TV does not support themed icons, so a monochrome layer is not a TV requirement. Adaptive banners are also recommended in the TV guide; use its template and retain the legacy 16:9 fallback instead of inventing adaptive banner XML from an icon example.

## Wallpaper and in-app icons

The existing [theme contract](../../../themes/README.md) asks for dark 1920x1080 wallpaper at about/below 300 KB each. Keep a full-quality source separately; export `wallpaper.jpg` only for an actual theme. Decode cost matters on 1 GB TVs: a 1920x1080 RGBA bitmap is about 7.9 MiB before caches. Avoid giant master art in runtime resources, video backgrounds or a new blur effect.

Use a dark quiet composition, with no baked-in clock, app name or buttons. Measure white labels over the final wallpaper and the actual dim/surface settings. The existing `wallpaper_dim` key can provide a scrim for a future theme; it is not a reason to change global defaults. Android resource names must use lowercase ASCII letters, digits and underscores. Existing `ic_*.xml` UI vectors remain editable; generated raster app marks do not imply replacing them.

## Optional Windows ICO export

ICO is an additional Windows/desktop deliverable requested by the user. It is not required by Android launcher, adaptive icon or TV banner formats. Export from the approved square RGBA PNG master into an actual ICO container with 16, 24, 32, 48, 64, 128 and 256 px entries. Preserve alpha, reopen every embedded size and inspect its silhouette. The local helper checks both the container entries and decoded sizes; copying a filename extension is insufficient. Keep it in `exports/desktop/` or a documentation example directory, outside `launcher/app/src/main/res`.

## Conversion helper

The helper uses Python and Pillow only for local image processing. Install its small, pinned [requirements](../scripts/requirements.txt) into an isolated local environment. It contains no network/API client and does not ask for credentials. From the repository root, with that environment's Python:

```powershell
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py check source-icon.png --kind icon
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py export-icon source-icon.png work/icon-exports
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py check work/icon-exports/cyt_icon.ico --kind ico
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py preview-icon work/icon-exports/cyt_icon.ico work/icon-inspection.png
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py wallpaper source-wallpaper.png work/wallpaper.jpg
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py check work/wallpaper.jpg --kind wallpaper
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py check work/wallpaper.jpg --kind wallpaper --dim 60
python .agents/skills/android-tv-image-assets/scripts/tv_assets.py check approved-banner.png --kind banner
```

The helper rejects existing outputs; choose a new versioned directory. Wallpaper resizing uses a central 16:9 crop and records the crop and any upscaling; inspect composition afterward. For a wallpaper contrast screen, `check --kind wallpaper` reports the minimum white-text ratio across pixels; `--dim` simulates the existing uniform black scrim without editing the image. File `status: PASS` describes format/size only; `contrast_screen_status` is separate and can fail. This conservative full-image result is not a measurement of every actual UI state/surface or proof of ten-foot readability.
