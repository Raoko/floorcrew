# FloorCrew — Progress Log

## Project Overview
**Two robots for the CoreWeave Hackathon (March 23, 2026)**
1. **SO-101 Arm** — Imitation learning for DC tasks (optic seating)
2. **Escort Bot** — Person-following vendor escort on the DC floor

---

## Current Status

| Robot | Code | Hardware | Tested | Demo Ready |
|-------|------|----------|--------|------------|
| SO-101 Arm | Done | **Ordered 3/9** — ETA ~3/18 | No | No |
| Escort Bot | Done | **Ordered 3/9** — ETA ~3/11 | No | No |

---

## What's Been Done

### Session: 2026-03-09 (evening)

**Hardware Ordered**
- Freenove 4WD Smart Car Kit — Amazon — ETA 3/11
- Samsung 30Q 18650 batteries + charger — Amazon — ETA 3/11
- MakerFocus Pi Battery Pack 10000mAh — Amazon — ETA 3/11
- HiWonder LeRobot SO-ARM101 Kit — hiwonder.com — **ETA ~3/18 (long pole)**
- NexiGo N60 1080P Webcam — Amazon — ETA 3/11
- Total: ~$408

**Camera-Only Test Script**
- Created `escort-bot/test_camera.py` — runs person detection without motors or ultrasonic
- Two modes: headless (terminal only) and `--display` (live video with bounding boxes)
- Simulates steering output so you can validate detection + steering logic before chassis arrives
- Run: `python3 test_camera.py` (headless) or `python3 test_camera.py --display` (with video)

---

### Session: 2026-03-09

**Research**
- Found iRobot Create 3 repos (decided against — overkill for this use case)
- Evaluated chassis options: Freenove 4WD ($65), SunFounder PiCar-X ($82), Yahboom ($70)
- Chose Freenove 4WD as escort bot platform
- Evaluated detection approaches: MobileNet SSD v2 (TFLite) wins at ~20 FPS on Pi 5
- Decided to skip ROS 2 — too heavy for a single-Pi demo, gpiozero is enough
- Researched SO-101 arm: HiWonder kits ($270-$460), LeRobot framework, ACT policy
- Found forkable repos: mshakeelt/Human-Following-Robot, LeRobot hackathon repo

**Escort Bot — Scaffolded**
- `hackathon/escort-bot/main.py` — Full person-following logic (~150 lines). TFLite MobileNet SSD + gpiozero + HC-SR04 ultrasonic. Proportional steering with distance control.
- `hackathon/escort-bot/install.sh` — One-command Pi 5 setup (apt + pip + model download)
- `hackathon/escort-bot/requirements.txt` — picamera2, tflite-runtime, gpiozero, numpy, lgpio
- `hackathon/escort-bot/WIRING.md` — GPIO pin map, L298N wiring, HC-SR04 voltage divider, test commands
- `hackathon/escort-bot/showcase.html` — Project scope page (white/navy theme, animations, 3D)

**SO-101 Arm — Scaffolded**
- `hackathon/robotics-site/so101/record.py` — Record demos via leader-follower teleoperation. 3 tasks defined: optic_seating (50 eps), rack_inspection (30), cable_management (100).
- `hackathon/robotics-site/so101/train.py` — Train ACT policy. Supports cuda/mps/cpu.
- `hackathon/robotics-site/so101/deploy.py` — Deploy trained model for autonomous execution.
- `hackathon/robotics-site/so101/install.sh` — venv + LeRobot from source + deps
- `hackathon/robotics-site/so101/requirements.txt` — lerobot, torch, opencv, numpy, tensorboard
- `hackathon/robotics-site/so101/HARDWARE.md` — BOM, assembly notes, kit tiers, compute options
- `hackathon/robotics-site/so101/showcase.html` — Project scope page (white/navy, 3D image, animations)

**Config Updates**
- Updated `hackathon/CLAUDE.md` — registered escort-bot, updated focus check to show both robots
- Updated `memory/MEMORY.md` — FloorCrew = two robots, Pi 4/5 as escort platform

---

## Hardware Shopping List

### Escort Bot (~$113) — Ordered 2026-03-09
- [x] Freenove 4WD Smart Car Kit — ~$65 (Amazon) — ETA 3/11
- [x] Samsung 30Q 18650 batteries + charger (2-pack) — ~$18 (Amazon) — ETA 3/11
- [x] MakerFocus Pi Battery Pack 10000mAh — ~$30 (Amazon) — ETA 3/11
- [x] Raspberry Pi 5 — already owned

### SO-101 Arm (~$295) — Ordered 2026-03-09
- [x] HiWonder LeRobot SO-ARM101 Kit — ~$270 (hiwonder.com) — **ETA ~3/18 (ships from China, 6 biz days)**
- [x] NexiGo N60 1080P Webcam — ~$25 (Amazon) — ETA 3/11
- [x] Raspberry Pi 5 or laptop — already owned

### Total: ~$408 (ordered)

---

## Key Decisions Made

| Decision | Chose | Over | Why |
|----------|-------|------|-----|
| Escort platform | Pi 5 + Freenove chassis | iRobot Create 3 | Already own Pi, $65 vs $300 |
| Detection model | MobileNet SSD v2 (TFLite) | YOLO, HOG | 20 FPS on Pi 5, no training needed |
| Motor framework | gpiozero | ROS 2 | One file, zero setup overhead |
| Arm kit | HiWonder SO-ARM101 | Seeed Studio + 3D print | Faster, all parts included |
| Training policy | ACT (Action Chunking) | Diffusion, RL | LeRobot default, works with 50 demos |
| Demo task | Optic seating | Cable management, rack inspection | Most tractable, clear success/fail |

---

## What's Next

### Immediate (this week)
1. [x] Order Freenove kit + batteries + power bank — **Done 3/9**
2. [x] Order SO-ARM101 DIY kit + webcam — **Done 3/9**
3. [ ] Sign up for hackathon (deadline: March 12) — **3 DAYS LEFT**
4. [ ] Camera-only detection test on Pi 5 (validate pipeline before hardware arrives)

### Week of March 16
4. [ ] Assemble Freenove chassis + wire motors/ultrasonic (~3.5 hrs)
5. [ ] Flash Pi 5, run escort-bot install.sh (~45 min)
6. [ ] First escort bot test — person detection + motor control
7. [ ] Assemble SO-101 arms (~2-3 hrs)
8. [ ] Install LeRobot, calibrate servos (~1 hr)

### Week of March 20-22
9. [ ] Tune escort bot on DC floor (Kp, speed, thresholds) (~2-4 hrs)
10. [ ] Record 50 optic seating demonstrations (~1-2 hrs)
11. [ ] Train ACT policy (~2-4 hrs, runs unattended)
12. [ ] Evaluate + retrain if needed (~2 hrs)
13. [ ] Demo polish — clean wiring, signage, camera feeds
14. [ ] Record 2-3 min demo video

### March 23 — Demo Day

---

## File Map

```
hackathon/
├── CLAUDE.md                          # Hackathon root config
├── PROGRESS.md                        # THIS FILE — single source of truth
├── escort-bot/
│   ├── main.py                        # Person-following robot brain
│   ├── test_camera.py                 # Camera-only detection test (no motors)
│   ├── install.sh                     # Pi 5 setup
│   ├── requirements.txt
│   ├── WIRING.md                      # GPIO + wiring diagrams
│   └── showcase.html                  # Scope page (CodePen-ready)
├── robotics-site/
│   ├── index.html                     # FloorCrew landing page
│   ├── so101-real.png                 # Arm photo
│   ├── guide-render.png
│   ├── CLAUDE.md                      # Robotics site config
│   └── so101/
│       ├── record.py                  # Record demos
│       ├── train.py                   # Train ACT policy
│       ├── deploy.py                  # Deploy autonomous
│       ├── install.sh                 # LeRobot setup
│       ├── requirements.txt
│       ├── HARDWARE.md                # BOM + assembly
│       └── showcase.html              # Scope page (CodePen-ready)
└── floorcrew-app/
    ├── index.html                     # Dashboard (FastAPI + vanilla JS)
    └── api/server.py                  # Backend
```
