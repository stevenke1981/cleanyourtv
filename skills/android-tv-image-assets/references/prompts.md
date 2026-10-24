# Built-in image_gen prompt examples

These are runnable prompt examples, not evidence that an image was generated. Use the tool exposed by the current Codex host. Save the exact submitted prompt and returned source. The requested dimensions describe intent; inspect the actual dimensions afterward.

## Wallpaper: dark aurora

Use `transparent_background: false`. For a brand-new image, omit edit/reference parameters.

```text
Use case: stylized-concept
Asset type: CleanYourTV Android TV wallpaper, landscape 16:9,
target export 1920x1080.
Primary request: a very dark atmospheric abstract aurora on nearly black
navy #070A14, with restrained soft teal and violet luminous wisps.
Composition: keep the upper-left clock/greeting area, upper-right utility
buttons, left-middle app title and lower-third dock zone dark and calm.
Subtle light may sit across the upper middle; no bright hotspots behind labels.
Style: minimal static ambient artwork, smooth organic light, low detail.
Constraints: no text, letters, numbers, logos, buttons, tiles, UI, people,
watermarks or borders. Opaque full-bleed background.
```

Check against `themes/aurora/screenshot.jpg` or the actual target screenshot. If light crosses the text area, request one focused revision such as: "Keep the same aurora palette and composition; darken the top 25% and left-middle text zone, without adding objects or text." Reinspect the result rather than assuming the wording guarantees contrast.

## Transparent original app-mark concept

Use `transparent_background: true`. This is a standalone mark concept, not a request to replace existing vector settings/input glyphs or third-party app logos.

```text
Use case: logo-brand
Asset type: original CleanYourTV icon master, square PNG, target 1024x1024.
Primary request: one bold front-facing rounded television silhouette with
a small four-point cleaning sparkle in its upper-right screen area.
Pale mint #CFFFCF face, restrained teal accent, dark navy screen interior.
Style: crisp flat vector-friendly geometry, strong silhouette at 16 px,
no thin detail or photorealism.
Composition: center the whole mark within the central 60% of the canvas,
with generous transparent padding for adaptive masks.
Constraints: real transparent alpha outside the mark; no solid app plate,
painted checkerboard, rectangle, external shadow, text, watermark or brand logo.
```

Inspect the alpha and edges on both light and dark surfaces. An icon showing a checkerboard baked into opaque pixels is a failure even if it looks transparent in a preview. If necessary, use a built-in edit with the original image as the edit target and ask to remove only the background/stray pixels, preserving the mark. Do not use a paid background-removal service as an unannounced fallback.

## TV banner artwork, then exact text

Use `transparent_background: false`. Keep the app name in the final banner even though the illustration source is text-free.

```text
Use case: logo-brand
Asset type: CleanYourTV Android TV launcher banner artwork, 16:9,
target export 320x180 at xhdpi, with a high-resolution source.
Primary request: restrained mint and teal television/cleaning mark on navy,
matching the approved icon, with quiet space for the exact app name.
Composition: simple mark at left and uncluttered wordmark space at right,
generous safe margins; no border that a launcher mask can clip.
Constraints: no generated lettering, UI, badges, claims or third-party logos.
```

Compose the approved app name from the actual string resource in each locale using a licensed font, export the correct density variants, then inspect spelling, cropping and readability at 320x180. If you instead ask the model to render the name, quote it verbatim and reject misspellings; do not label a text-free source as an accepted launcher banner.

## Example invocations

```text
Use $android-tv-ui-ux to define the remote focus and Back contract for the
app library, including empty and retry states. Keep the current Java UI.

Use $android-tv-image-assets to generate a dark aurora wallpaper and a
transparent original icon with built-in image_gen, then export Android PNGs
and an additional Windows .ico. Keep them as documentation examples.
```
