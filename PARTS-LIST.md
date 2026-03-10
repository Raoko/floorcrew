# FloorCrew — Complete Parts List

> **Last updated:** 2026-03-09
> **Budget estimate:** ~$430–$455 total (before owned items)
> **Hackathon date:** March 23, 2026

Legend: ✅ = Owned | 🛒 = Need to buy | ⏳ = Ordered, waiting

---

## ROBOT 1: SO-101 Arm (Manipulation Bot)

### Option A: HiWonder Pre-Built Kit (RECOMMENDED)

- [ ] 🛒 **SO-ARM101 DIY Kit** — ~$270
  - Source: https://www.hiwonder.com/products/lerobot-so-101
  - Includes ALL of the following:
    - 6x Follower arm servos (HX-30HM / STS3215) — 30kg.cm @ 12V
    - 6x Leader arm servos (HX-10HM) — lighter, for teleoperation
    - 2x BusLinker V3.0 servo controller (USB-to-serial)
    - 1x 12V 5A power supply (barrel jack, follower arm)
    - 1x 5V power supply (leader arm)
    - 4x Table clamps (2 per arm)
    - Full set 3D-printed structural parts (ABS/PLA arm links + brackets)
    - Screws, cables, assembly hardware (M2/M3)

### Option B: DIY Build (requires 3D printer)

- [ ] 🛒 Feetech STS3215 servos x6 (follower) — ~$120 — AliExpress / RobotShop
- [ ] 🛒 Feetech STS3215 servos x6 (leader) — ~$100 — AliExpress
- [ ] 🛒 BusLinker V3.0 board x2 — ~$30 — HiWonder / AliExpress
- [ ] 🛒 3D-printed parts (STLs from https://github.com/TheRobotStudio/SO-ARM100) — ~$35 filament
- [ ] 🛒 12V 5A DC power supply — ~$12 — Amazon
- [ ] 🛒 5V 3A power supply — ~$8 — Amazon
- [ ] 🛒 Table C-clamps x4 (2" opening min) — ~$10 — Amazon / hardware store
- [ ] 🛒 M2 + M3 screw assortment kit — ~$8 — Amazon
- [ ] 🛒 Servo extension cables x6 (3-pin, 20cm) — ~$5 — Amazon

### Arm Add-ons (needed regardless of option)

- [ ] 🛒 **USB webcam (arm-mounted)** — ~$25 — Logitech C270 or similar, 1080p, OpenCV-compatible
- [ ] 🛒 USB-C data cable (to laptop, 6ft) — ~$8 — Amazon
- [ ] 🛒 Webcam mount/bracket — ~$5 — 3D-print or flex gooseneck clamp
- [ ] 🛒 Cable ties (small, 100-pack) — ~$3 — Amazon

**Arm subtotal (Option A + add-ons): ~$311**

---

## ROBOT 2: Escort Bot (Person-Following Mobile Robot)

### Compute (OWNED)

- [x] ✅ **Raspberry Pi 5** (8GB) — OWNED
- [x] ✅ **Raspberry Pi 4** — OWNED (backup)
- [x] ✅ **Raspberry Pi Pico** — OWNED (not ideal for CV)
- [ ] 🛒 MicroSD card 32GB+ (Class 10 / A2) — ~$8 — Amazon (Samsung EVO Select or SanDisk Extreme)
- [ ] 🛒 **Raspberry Pi 5 Active Cooler (OFFICIAL)** — ~$5
  - Amazon: https://www.amazon.com/Raspberry-Pi-Active-Cooler/dp/B0CLXZBR5P
  - PWM temp-controlled blower + aluminum heatsink + thermal tape
  - REQUIRED — TFLite CV workload will thermal throttle Pi 5 without cooling

> **Pi 5 OS Setup Guide:** See [`escort-bot/PI-SETUP.md`](escort-bot/PI-SETUP.md)
> **OS:** Raspberry Pi OS Lite (64-bit) — Bookworm. Only official OS for Pi 5. Lite = headless, no desktop wasting RAM.
> **Imager download:** https://downloads.raspberrypi.com/imager/imager_latest.dmg

### Chassis + Drivetrain

- [ ] 🛒 **Freenove 4WD Smart Car Kit** — ~$65
  - Amazon: https://www.amazon.com/Freenove-Raspberry-Tracking-Avoidance-Ultrasonic/dp/B07YD2LT9D
  - Kit includes (VERIFIED from Freenove docs):
    - **Smart Car Board** — integrated motor driver PCB (replaces standalone L298N)
    - **Connection Board** — PCB V1.0/V2.0, bridges Pi GPIO to smart car board
    - **HC-SR04 ultrasonic sensor** + servo mount for panning
    - **Pi Camera** (CSI ribbon, Pi3/4 and Pi5 compatible versions)
    - **2x Servo motors** — pan-tilt assembly for camera + ultrasonic
    - **Infrared line tracking module** (XH-2.54-5Pin)
    - **2x Photoresistors** — light tracing
    - **LEDs + Buzzer** — built into board
    - 4x DC geared motors with aluminum brackets
    - 4x Mecanum wheels (A-B-A-B configuration)
    - Battery holder (18650 x2, 7.4V nominal)
    - All hardware: M2/M2.5/M3 screws, nuts, standoffs
  - **NOT included:** Raspberry Pi, 2x 18650 batteries, battery charger

### ~~Motor Control~~ — INCLUDED IN KIT

- [x] ~~L298N motor driver~~ — **NOT NEEDED** — Kit has integrated Smart Car Board motor driver
- [ ] 🛒 Jumper wires M-F x20 (20cm) — ~$5 — Amazon (still useful for custom wiring)
- [ ] 🛒 Jumper wires M-M x10 (20cm) — ~$3 — Amazon

**Wiring: handled by kit's Connection Board → Smart Car Board. Custom GPIO map only needed if bypassing kit PCB.**

### ~~Sensors~~ — INCLUDED IN KIT

- [x] ~~HC-SR04P ultrasonic sensor~~ — **NOT NEEDED** — Kit includes HC-SR04 + servo mount

### ~~Vision~~ — INCLUDED IN KIT

- [x] ~~USB webcam / Pi Camera~~ — **NOT NEEDED** — Kit includes Pi Camera (CSI)
- [x] ~~Camera mount~~ — **NOT NEEDED** — Kit includes pan-tilt assembly

### Power

- [ ] 🛒 **18650 Li-ion batteries (4-pack)** — ~$13
  - Amazon: https://www.amazon.com/QOJH-18650-Rechargeable-Landscape-Flashlight/dp/B0D5YYRCYV
  - QOJH 3.7V 3000mAh, button top, protected
- [ ] 🛒 **18650 dual-slot charger** — ~$9
  - Amazon: https://www.amazon.com/ACEBOTT-Battery-Dual-Slot-Rechargeable-Batteries/dp/B0DHKNC1Z1
  - ACEBOTT smart charger, auto-shutoff, US plug
- [ ] 🛒 **USB-C power bank (Pi power)** — ~$22
  - Amazon: https://www.amazon.com/Anker-Travel-Ready-Technology-High-Speed-Output%EF%BC%89%EF%BC%891pack/dp/B0D5CLSMFB
  - Anker PowerCore 10K, 10000mAh, 5V/3A USB-C
- [ ] 🛒 Short USB-C cable (6-12 inches, power bank → Pi) — ~$5 — Amazon

**Power architecture:**
```
Pi 5       ← USB-C power bank (separate, clean 5V/3A)
Motors     ← 18650 x2 in series (7.4V) through Smart Car Board
Sensors    ← Pi 5V rail (via Connection Board)
CRITICAL   → Common GND between Pi and Smart Car Board!
```

### Misc Hardware

- [ ] 🛒 Zip ties (assorted pack) — ~$3
- [ ] 🛒 Double-sided foam tape (1 roll) — ~$5
- [ ] 🛒 Half-size breadboard — ~$4
- [ ] 🛒 Electrical tape (1 roll) — ~$3
- [ ] 🛒 Velcro strips x4 — ~$5
- [ ] Rubber bands x5 — ~$0 (around the house)

**Escort bot subtotal: ~$140** (saved ~$37 — motor driver, ultrasonic, camera all in kit)

---

## SHARED / DEMO EQUIPMENT

- [x] ✅ **Laptop** (Mac M-series for training + demo) — OWNED
- [ ] 🛒 USB-A hub (4-port, if laptop is USB-C only) — ~$12 — Amazon
- [ ] 🛒 Ethernet cable (for SSH into Pi) — ~$5 — Amazon
- [ ] 🛒 HDMI cable + portable monitor (optional, Pi debug) — ~$0-30
- [ ] Extension cord / power strip (demo day) — bring from home
- [ ] Sample optic / fiber tray (arm demo task) — grab from DC floor
- [ ] Hard hat / safety vest (demo realism) — already have from DC

**Shared subtotal: ~$17-47**

---

## COST SUMMARY

| Category | Estimate |
|----------|----------|
| SO-101 Arm (HiWonder kit + add-ons) | ~$311 |
| Escort Bot (all parts — kit covers driver/sensor/camera) | ~$145 |
| Shared / Demo gear | ~$17-47 |
| **GRAND TOTAL** | **~$468-498** |
| Minus owned items (Pi 5, Pi 4, laptop, DC gear) | -$0 saved (no price on owned) |

### Savings from Freenove kit overlap:
Motor driver (~$10) + HC-SR04P (~$4) + webcam/camera (~$20) + camera mount (~$3) = **~$37 saved**

---

## ORDER PRIORITY (what to buy first)

1. **HiWonder SO-101 Kit** — longest ship time (~5-7 days), order ASAP
2. **Freenove 4WD Kit** — Amazon Prime, 1-2 days
3. **Batteries + charger** — need charged before demo day
4. **Everything else** — Amazon Prime, order by March 18 latest

---

## RESOURCE LINKS

| Resource | URL |
|----------|-----|
| HiWonder SO-101 Kit | https://www.hiwonder.com/products/lerobot-so-101 |
| SO-ARM100 STLs (3D print) | https://github.com/TheRobotStudio/SO-ARM100 |
| LeRobot (HuggingFace) | https://github.com/huggingface/lerobot |
| LeRobot SO-101 docs | https://huggingface.co/docs/lerobot/en/so101 |
| Freenove 4WD GitHub | https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi |
| Haoran Xu build log | https://www.linkedin.com/pulse/lets-build-ai-hack-lerobot-so101-haoran-xu-onaqc/ |
| iRobot Create 3 (alt escort) | https://github.com/iRobotEducation/create3_docs |
