# Master AI Prompt Log — Pigeon & Rat

**Coding agent:** Claude (Anthropic), working in the Claude desktop app. It was connected to:
- **Unreal Editor 5.8** through the *Unreal MCP* toolsets: BlueprintTools (graph DSL read/write), SceneTools, AssetTools, ObjectTools, SlateInspector, EditorApp, Logs, ConfigSettings.
- My Windows folders, through the desktop file bridge.

**Other AI:** Tripo AI (3D models) and ElevenLabs (music and SFX).

Prompts are quoted in the language I typed them in (Mandarin), with an English gloss. They are in chronological order and grouped by phase. "AI →" lines summarise what the agent did.


---

## Phase 0 — Scaffolding (grey-box prototype)

| # | Prompt (gloss) | AI → |
|---|---|---|
| 0.1 | Build a Crossy-Road-like NYC street where the player **jaywalks**: lanes of taxis, buses and bikes, a pedestrian signal, sidewalks. | Created the `JWalkDemo` grey-box: road, curbs, lane dashes, `BP_NYC_LaneSpawner` (per-lane vehicle loop with car-following gaps), `BP_NYC_Signal`, `BP_NYC_Pedestrian`, and buildings made of instanced façade blueprints. |
| 0.2 | Make the player hop tile by tile; getting hit by a car costs a life. | `BP_NYC_Pigeon` pawn: grid hop (200 × 400 cm tiles) with a hop arc, `Die` / `Respawn`, lives, score. |

## Phase 1 — HUD design (design canvas, HTML mock-ups)

| # | Prompt (gloss) | AI → |
|---|---|---|
| 1.1 | 「PIGEON & RAT 左上角是標題，右上角放一隻老鼠頭然後生命值」 *(title top-left, rat head and lives top-right)* | Redrew the HUD board. |
| 1.2 | 「How to play 寫太複雜了，風格要像紅燈那樣，黑底…不用點收集，老鼠碰到就可以直接收集…最下面寫 watch out! if you cross the road」 *(simplify How to Play; traffic-light style, black panel; touching food collects it; "watch out" footer)* | New How-to-Play panel. |
| 1.3–1.7 | Minimap iterations: 「只要一個三角形箭頭裡面有個老鼠頭」 → 「圓形，尖角朝上放 Nest icon…放畫面左下角」 → 「圖可以變成左右了…Nest 改成 Home 的 icon 像對話框」 → 「太寬了…背景黑色有透明度…食物都在同一排在圓點上方」 → 「食物消失就消失…老鼠頭做成三角形在原點上跑」 *(a triangle arrow with the rat head → a circle with the nest icon pointing up, bottom-left → horizontal strip with a Home speech-bubble icon → narrower, translucent black, foods in one row above the dots → collected food disappears; the rat head itself becomes the triangle marker)* | Six layout revisions; the final strip map is what ships. |
| 1.8 | 「收集到的食物會直接在食物上面打勾然後顏色變淺」 *(collected food gets a tick and turns pale)* | Menu-card state for collected food. |
| 1.9 | 「問號旁邊想放一個 Home icon…返回 Menu，暫停或 Exit」 *(a Home icon next to the "?" that opens Menu / Pause / Exit)* | 🏠 and ❓ buttons, bottom-right. |

## Phase 2 — Comic-style screens

| # | Prompt (gloss) | AI → |
|---|---|---|
| 2.1 | 「開始畫面…左邊放上老鼠過街鴿子正在搶她食物的圖，右邊放上 PIGEON & RAT 標題…Play…Exit」 *(start screen: left art of the rat crossing while a pigeon grabs its food; right: title, Play, Exit)* | Start-screen layout. |
| 2.2 | 「風格可以改得像美式漫畫風一點」 *(make it more American comic)* | Halftone dots, burst shapes ("SNATCH!"), speech bubbles, Bangers font. |
| 2.3 | 「藍色背景可以放上紐約街頭疊印上去…Play Exit 放大」 *(overprint a NYC street on the blue background; bigger Play / Exit)* | Overprinted skyline; bigger buttons. |
| 2.4 | 「依照一樣的風格和邏輯重新設計失敗和成功下一關的頁面」 → 「圖像在左右兩側，正中間是成功或失敗」 *(redesign the fail and success screens in the same style → art on both sides, result in the middle)* | Game Over ("SPLAT!", "THANKS!" taxi) and Clear ("YUM!", "HOME SWEET HOME!") screens. |
| 2.5 | 「過關的寫 Street Clear! Next Area 你覺得這樣寫清楚嗎…讓玩家有種真的是老鼠…前進下一區偷食物」 *(is "Street Clear! Next Area" clear? I want the player to feel like a rat moving on to raid the next block)* | Suggested **STREET CLEAR! / NEXT BLOCK →** plus a subtitle such as "W 34TH ST · RAIDED!". |
| 2.6 | Donate page: 「donate more and play more…China town…阿北拿掃把趕老鼠」 → 「不要寫中文，不要這麼紅…Noodle dumpling 雞腿 Rice…阿北一臉驚嚇…也有鴿子要搶食…Want to play in Asian district? The next block is still being built. help the rat get past Uncle and his broom!」 *(a donate page set in Chinatown with an uncle chasing the rat with a broom → no Chinese text, less red, shop signs Noodle / Dumpling / Chicken / Rice, a shocked uncle, a pigeon also stealing food, and the given copy)* | Donate comic and copy. |

## Phase 3 — Tripo 3D assets

| # | Prompt (gloss) | AI → |
|---|---|---|
| 3.1 | 「我想用 Tripo AI 生成模型，然後想問你給你什麼檔案好」 *(what files should I give you from Tripo?)* | Recommended FBX with textures. |
| 3.2 | 「起司全部改成 Cheese cake，然後生成兩張圖…你覺得用哪種老鼠和鴿子好」 *(rename cheese to cheesecake; make two reference images; which rat and pigeon style is better?)* | Renamed cheese to cheesecake everywhere; drew rat and pigeon style references (`Docs/media/concept_*.jpg`). |
| 3.3 | 「檔案給你 fbx 可以嗎」「那要 for Blender、Mixamo 還是哪個」「紋理分辨率多少好」 *(is FBX OK? which export variant? what texture resolution?)* | Answered: plain FBX, not rigged; 2K textures are enough for small props. |

**Tripo generation log.** Route: **tripo3d.ai directly, Image-to-3D**. I uploaded a reference image for each object; there was no text prompt. I downloaded the FBX and imported it through the Blender pipeline. Credits: **45 credits per model × 6 models = 270 credits**.

| Asset | Input | Tripo download folder (auto-named) | Credits |
|---|---|---|---|
| Rat | reference image (image-to-3D) | `cartoon+mouse+3d+model/` | 45 |
| Pigeon | reference image | `bird+cartoon+3d+model/` | 45 |
| Pizza slice | reference image | `pizza+slice+3d+model/` | 45 |
| Hot dog | reference image | `hot+dog+3d+model/` | 45 |
| Soda can | reference image | `red+soda+can+3d+model/` | 45 |
| Strawberry cheesecake | reference image | `strawberry+cheesecake+3d+model/` | 45 |
| **Total** | | | **270** |

## Phase 4 — Implement everything in Unreal

| # | Prompt (gloss) | AI → |
|---|---|---|
| 4.1 | 「根據以上幫我在 Unreal 修改，我也附上我生成的 3D 模型，但 3D 模型的風格有點不一致，幫我稍微調整」 *(build all of the above in Unreal; here are my Tripo models; their styles don't quite match, adjust them a little)* | **Assets:** Blender bpy pipeline (`Tools/blender/proc.py`, `grade.py`); `M_ToonMaster` plus one material instance per model. **Rat player:** `BP_NYC_Rat`, a child of the pigeon pawn, with the pigeon parts hidden. **Pigeon thief:** `BP_NYC_PigeonThief`, which swoops at the rat while it carries food, steals within 130 cm, then leaves for 6–11 s. **Food:** `BP_NYC_PizzaBench` with FoodType 1–4 and 3–6 s respawn. **Game flow:** ResetGame builds a shuffled 5-item order; a state machine runs menu / play / pause / game over / clear / donate. **HUD:** `BP_NYC_HUD` canvas HUD with hit-box buttons. **Save:** best score in `BP_NYC_Save`. |
| 4.2 | 「大概還要多久」 *(about how much longer?)* | Status update. |

## Phase 5 — Playtest refinements

| # | Prompt (gloss) | AI → |
|---|---|---|
| 5.1 | 「我到對面去之後我沒辦法轉回頭，回頭就會被車撞。Hotdog 不要直接寫 Hotdog，做一個熱狗招牌在攤位前面，也不要有板子在地上。我想要按下往上的箭頭可以爬到攤位上」 *(after crossing I can't turn back without getting hit; replace the "Hotdog" text with a hot dog sign in front of the stand; no board on the ground; I want ↑ to climb onto the stand)* | **Camera flip:** CamBase eases 90° → 270° while carrying, and the hop directions multiply by −1, so ↑ is always forward. **Hot dog stand:** removed the text sign and goal pad; added a pole with the Tripo hot dog on top. **Climbing:** `TryHop` climbs onto the cart at (0, 1960, 167); the hot dog pickup requires being on the cart. |
| 5.2 | 「那現在也是可以爬上椅子拿其他的食物嗎…可樂和其他的食物現在在哪」 *(can I also climb benches to get other food? where are the cola and the other foods?)* | Explained the layout: only the cart is climbable. |
| 5.3 | 「現在會有鴿子嗎…關卡有一點難，可以在每次過完馬路一次再增加路上的車流或人潮」 *(is there a pigeon now? the level is a bit hard; add more traffic or pedestrians each time I finish a crossing)* | `ApplyTraffic`: lane time dilation rises with Crossings. |
| 5.4 | 「記得繼續執行…過一次馬路才會多人和多一點車的那個邏輯」 *(remember to keep going on the "more people and cars after each crossing" logic)* | `LaneSpawner.AddCar` adds +1 car in about 60% of lanes, up to +3 per lane. `ApplyTraffic` adds +1 pedestrian per crossing (+2 from the 3rd crossing on), up to 9; on reset `TrimCars` removes the extras and destroys the extra pedestrians. Pedestrians now **step on the rat** (−1 heart). |
| 5.5 | 「食物都放得太規律了，可以四處放，長椅也是太規律。有些會放在街道的箱子上，有些放在地上，有些放在垃圾桶…不只會有一條斑馬線，左右也增加」 *(food and benches are too regular; scatter them: some on street boxes, some on the ground, some on trash cans; add crosswalks on the left and right too)* | `Tools/level_layout.py`, run through the editor Python console: **9 pickups** on the ground, crates, a crate stack, trash cans and benches; decorative props; crosswalks at x = ±1500, with the lane dashes underneath hidden; pedestrians spread over the 3 crosswalks. |
| 5.6 | 「總共要有三條命，一開始的第一次過馬路再次變簡單一點」 *(3 lives in total; make the very first crossing easier again)* | Confirmed Lives = 3 (already set in `ResetGame`). The first crossing uses traffic factor 0.5; afterwards it is `min(0.7 + 0.05·n, 1.2)`. |

## Phase 6 — Audio

| # | Prompt (gloss) | AI → |
|---|---|---|
| 6.1 | 「背景音樂我要用這個，然後當老鼠往前一格會發出啾一聲，然後失敗或關卡成功都會有一個遊戲關卡聲音」 *(use this as background music; a squeak on every hop forward; a game sound on failure and on level success)* + 3 ElevenLabs MP3s | MP3 → WAV. Ambience made seamless by crossfade (28 s loop). Squeak synthesised (0.13 s chirp). Imported as SoundWaves. `BGM_StreetAmbience` AmbientSound loops. `PlaySound2D` hooks in `TryHop` (squeak, random pitch) and `FinishRound` (win / lose). |

**ElevenLabs prompts.** I generated 3 tracks, all in the same direction: *"New York street background sounds, NYC jazz vibe"*.

| Track | Prompt (paraphrased) | File |
|---|---|---|
| Background | NYC street ambience with a jazzy New York vibe | `NYC_street_ambience.mp3` → `S_Ambience` |
| Fail | short NYC-jazz "lost game" sting over street sound | `Lost_game.mp3` → `S_Lose` |
| Success | short NYC-jazz "win game" sting | `Win_Game.mp3` → `S_Win` |

## Phase 7 — Trailer / demo capture

| # | Prompt (gloss) | AI → |
|---|---|---|
| 7.1 | 「根據以上改完，給我一個 30 秒的小 Demo 影片」 *(after these changes, make me a short 30-second demo video)* | `Tools/demo_autopilot_capture.py`. An **autopilot** reads the rat's order, finds the nearest needed food, and checks every lane's vehicles and the pedestrians before each hop. The game runs at **0.35× slow motion** while a screenshot is taken every frame. ffmpeg retimes the frames to real time, at about 22 fps → 30 fps. The audio track is rebuilt from the event log: ambience plus a squeak at each logged hop. |

**Trailer shot list (current 30 s cut, all real gameplay):** 0–2.5 s start screen (hook) → 2.5–9 s first crossing past a bus → 9.6 s grab food → 10–15 s carry home under the PIGEON! warning → 15.9 s delivery tick → 16–31 s second run with a JAYWALK combo → fade.
✏️ TODO for the PG3 trailer: add image-to-video **generated shots** from the key art, plus an end title card ("Pigeon & Rat · Download on GitHub"), and list those shot prompts here.

## Phase 8 — Ship

| # | Prompt (gloss) | AI → |
|---|---|---|
| 8.1 | 「幫我這些打包成一個可以直接上傳到 Github 讓人家下載就可以點開玩的檔案」 *(package all this into a file I can upload to GitHub that people can download and just open to play)* | Set the default map and game mode; Shipping; cook only `L_NYCrossing`; ran UAT BuildCookRun (see below); test-launched the build; zipped it. |
| 8.2 | 「下一步把它上傳到 Github，我新建的 game-Pigeon-and-Rat-UE」 *(next, upload it to GitHub, to the game-Pigeon-and-Rat-UE repo I just made)* | This repo: source, `.gitignore`, docs, and a Release containing the zip. |
| 8.3 | 「幫我寫一下 Readme…發想過程…遊戲簡介、玩法、一些圖…Credit」 *(write the README: ideation process, game intro, how to play, some images, credits)* | README.md, this log, ATTRIBUTION.md. |
| 8.4 | 「Donate 可以連到 https://chenyingju.com/contact-form」 *(the Donate button can link to https://chenyingju.com/contact-form)* | Rewrote `DoDonate` → `LaunchURL`, recompiled, and re-packaged the build. |

### Packaging
```bat
RunUAT.bat BuildCookRun -project="...\MyProject.uproject" -noP4 -platform=Win64 ^
  -clientconfig=Shipping -installed -nocompile -nocompileuat -nocompileeditor -skipbuildeditor ^
  -cook -stage -package -pak -iostore -compressed -prereqs -nodebuginfo ^
  -archive -archivedirectory="...\Build_Package"
```

---

## Error recovery log

| What broke | Cause found | How it was re-prompted or fixed |
|---|---|---|
| Tripo FBX import: *"all polygons degenerate"*, and the meshes were tiny | The raw meshes were extremely dense and in metres | Blender script: decimate to about 12k triangles, ×100 scale, pivot at the bottom; re-imported as `_cm` meshes and repointed every reference |
| The 6 models had mismatched styles | Different lighting and saturation in the Tripo textures | `grade.py` texture grading plus one shared toon master material with a rim light |
| Function arguments silently ignored; food was invisible | In the Blueprint DSL, positional literal arguments were dropped or bound to *self* | Rule: always pass keyword pins (`:Vis true`, `:Text`, `:Show`). This fixed the invisible-food bug. |
| Placed actors did not show new components | Instances kept stale component data after the template changed | Re-placed the actors with the same transform and properties |
| Node-type errors (`Math|Integer|Max`, `vector+vector`, `EventReceiveHitBoxClick`, switch on Name) | Wrong node IDs for this engine version | Used `select`, `+`, `EventHitBoxClicked`, and if-chains on names |
| `SetCustomTimeDilation` on another actor failed | It is a self-only variable setter | Added `SetFactor(F)` inside `BP_NYC_LaneSpawner` and called that instead |
| Could not remove actors / the game reset itself | Editing or compiling while Play-In-Editor was running re-instanced the actors | Always stop PIE before editing the level or compiling |
| **WAV import refused** ("TextureFactory does not support .wav") | The texture import tool was the wrong factory | Typed `py …AssetImportTask…` into the editor console to import the audio |
| Editor console stopped accepting commands | An auto-import notification stole keyboard focus | Dismissed the dialog, re-focused the console box |
| Level script crashed half-way (`rerun_construction_scripts` doesn't exist) and the bench groups moved twice | An unavailable API, plus a non-idempotent script | Rewrote it to place benches at absolute positions, cleaning the `NYCrossing/Props` folder first, so re-runs are safe |
| Demo autopilot: the rat jittered left and right | ←/→ are camera-relative; with the camera facing +Y, screen-right is world −X | Corrected the mapping; made the food target "sticky" |
| Demo capture: a 10 s gap and about 9 fps | A first-frame hitch, plus editor CPU throttling in the background | Waited for the hitch to pass; turned off "Use less CPU when in background"; slow-motion capture at 0.35× |
| **Packaging #1:** "Win64 SDK not found" | The `GameplayStateTree` plugin made the BP project count as a C++ project, which needs the Windows SDK | Disabled that unused plugin |
| **Packaging #2:** the same, then *MyProjectEditor.target not found* | The editor-only **ModelContextProtocol / AllToolsets** plugins also forced a code build; stale temp `.Target.cs` files remained | The packaging script strips those plugins from the `.uproject` for the duration of the build, deletes `Intermediate/Source`, then restores the file. BUILD SUCCESSFUL in 3 min. |

---

## Analytical reflection

The AI handled the volume of engine work. It wrote and rewrote around fifteen Blueprints through a text DSL: the grid movement, the pigeon AI, the traffic spawner with car-following, the HUD hit-boxes, the save game. It also wrote Python that laid out the level, a Blender pipeline that normalised six Tripo models, and the packaging scripts. It worked fast and never got tired of the tenth minimap revision.

What I did was the part the AI cannot judge on its own. I decided what this game is *about*: a rat stealing lunch on a real New York block. I decided what "comic" should look like, and when a screen was "too red" or "too regular". Most of all, I playtested. Every important change came from me actually playing: the moment I couldn't turn back after crossing, the stand that needed a real hot dog I could climb, the first crossing that was too punishing, the food that sat in a too-tidy row. The AI could not have found these, because it does not feel frustration.

Compared with PG2 in the browser, the engine changed the division of labour. In the browser, the AI could write a whole game in one file and I could read it. In Unreal, the work is spread across assets, Blueprints, materials, level actors and project settings, and much of it is invisible as text. That made the AI's tool access (MCP into the editor) essential. It also produced a new class of bugs: stale instances, PIE re-instancing, plugins that silently turned my project into a C++ project at packaging time. Those failures showed me that in an engine, my job shifts from "reviewing code" to directing, testing and catching what the engine does behind the AI's back.

*(about 290 words)*
