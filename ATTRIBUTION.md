# Asset Attribution Sheet and AI Tools Inventory — Pigeon & Rat

## 1. Generative AI models and tools used

| Area | Tool / model | How it was used |
|---|---|---|
| Code and Blueprints | **Claude** (Anthropic) in the Claude desktop app, connected to Unreal Editor 5.8 through the **Unreal MCP** toolsets | Wrote and edited every Blueprint graph (text DSL), materials, level layout (editor Python), project and packaging settings, the demo-capture autopilot, and the docs |
| UI and 2D art | **Claude** (HTML/SVG mock-ups on a design canvas, rendered to PNG with headless Chromium) | HUD icons, How-to-Play panel, Start / Game Over / Street Clear / Donate comic screens, rat and pigeon style references |
| 3D models | **Tripo AI** (tripo3d.ai, Image-to-3D) | Rat, pigeon, pizza slice, hot dog, soda can, strawberry cheesecake. 6 models × 45 credits = 270 credits. |
| 3D processing | Blender 4 (bpy), scripted by Claude | Decimation, scale, pivot, texture colour grading (`Tools/blender/`) |
| Music and SFX | **ElevenLabs** | Street ambience music bed, win sting, lose sting. Prompt direction: *"New York street background sounds, NYC jazz vibe"*. |
| Procedural SFX | Python / numpy (written by Claude) | 0.13 s rat-squeak chirp |
| Video | Unreal screenshots + ffmpeg (scripted by Claude) | 30 s gameplay demo (`Docs/PigeonRat_Demo_30s.mp4`) |

## 2. Asset licence table

| Asset(s) | Location | Source | Licence / terms | Notes |
|---|---|---|---|---|
| Rat, Pigeon, Pizza, HotDog, Soda, Cheesecake meshes and textures | `Content/NYCrossing/Assets3D/*` | Tripo AI | [Tripo Terms of Service](https://www.tripo3d.ai/terms) | Generated on Tripo's **free plan**. ⚠️ **Free-plan models are public** on Tripo's platform and come with limited rights; commercial use needs a paid plan. This project is non-commercial coursework. |
| Street ambience, Win, Lose | `Content/NYCrossing/Audio/S_Ambience`, `S_Win`, `S_Lose` | ElevenLabs | [ElevenLabs Terms](https://elevenlabs.io/terms-of-use) | Under ElevenLabs' rules, free-plan output may be published **non-commercially with attribution** ("elevenlabs.io"). It is credited here, in the README and in-repo. If generated on a paid plan, a commercial licence applies. |
| Rat squeak | `Content/NYCrossing/Audio/S_Squeak` | Procedurally synthesised (numpy) | Original, part of this project | — |
| UI textures and comic screens | `Content/NYCrossing/UI/*` | Generated as code by Claude under my art direction | Original, part of this project | Uses the fonts below |
| Fonts: **Bangers**, **Share Tech Mono**, **Inter** | baked into the UI textures | Google Fonts | SIL Open Font License 1.1 | — |
| Blueprints, materials, level | `Content/NYCrossing/*`, `Content/JWalkDemo/*` | Made in this project (AI-assisted) | Original, part of this project | Uses engine basic shapes (`/Engine/BasicShapes`) |
| Unreal Engine 5.8 and engine content | — | Epic Games | [Unreal Engine EULA](https://www.unrealengine.com/eula) | Packaged build includes engine runtime |
| Blender | tool only | Blender Foundation | GPL (output is unrestricted) | — |
| ffmpeg | tool only | FFmpeg project | LGPL/GPL (tool only) | — |

## 3. Reference items (inspiration)

- **Gameplay references:** *Frogger* (Konami, 1981) and *Crossy Road* (Hipster Whale, 2014) for lane-crossing; the famous NYC "Pizza Rat" viral video (2015) for the theme.
- **Target look:** American comic books — Ben-Day halftone dots, burst balloons, bold Bangers lettering. Low-poly toy-like city with saturated taxi yellow.
- **Target sound:** a busy Manhattan street (horns, chatter) under a light NYC jazz bed; short arcade-style win / lose stings; a cartoon squeak per hop.
- **Moodboard:** `Docs/media/concept_rat.jpg`, `Docs/media/concept_pigeon.jpg`, and the design-canvas boards (`Docs/media/screen_*.jpg`).
