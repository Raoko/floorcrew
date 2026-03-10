"""
FloorCrew Dashboard — FastAPI WebSocket Server
Serves mock data for arm status, escort bot, scan logs, training state.
Replace mock generators with real hardware interfaces when ready.
"""

import asyncio
import json
import math
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="FloorCrew Dashboard")

# Serve frontend
ROOT = Path(__file__).parent.parent

@app.get("/")
async def index():
    return FileResponse(ROOT / "index.html")

# ── Mock Data Generators ────────────────────────────────────

def mock_arm_state(t: float) -> dict:
    """Simulate SO-ARM101 joint angles + gripper cycling through a pick sequence."""
    cycle = t % 12  # 12-second loop
    phase = "idle"
    gripper = "open"
    optic = False

    # Simulate a pick-place cycle
    if cycle < 2:
        phase = "idle"
        joints = [0, 0, 0, 0, 0, 0]
    elif cycle < 4:
        phase = "reaching"
        p = (cycle - 2) / 2
        joints = [
            -40 * p,
            -3 * p,
            -2 * p,
            5 * math.sin(p * math.pi) * 2,
            0,
            0,
        ]
    elif cycle < 5:
        phase = "gripping"
        gripper = "closing"
        joints = [-40, -3, -2, 0, 0, 0]
    elif cycle < 5.5:
        phase = "gripping"
        gripper = "closed"
        optic = True
        joints = [-40, -3, -2, 0, 0, 0]
    elif cycle < 8:
        phase = "transiting"
        p = (cycle - 5.5) / 2.5
        optic = True
        gripper = "closed"
        joints = [
            -40 + 88 * p,
            -3 + 6 * p,
            -2 + 4 * p,
            3 * math.sin(p * math.pi),
            0,
            0,
        ]
    elif cycle < 9:
        phase = "inserting"
        optic = True
        gripper = "closed"
        joints = [48, 3, 2, 0, 0, 0]
    elif cycle < 9.5:
        phase = "releasing"
        gripper = "open"
        optic = False
        joints = [48, 3, 2, 0, 0, 0]
    else:
        phase = "retracting"
        p = (cycle - 9.5) / 2.5
        joints = [48 * (1 - p), 3 * (1 - p), 2 * (1 - p), 0, 0, 0]

    # Add slight noise for realism
    joints = [round(j + random.uniform(-0.3, 0.3), 1) for j in joints]

    return {
        "type": "arm",
        "phase": phase,
        "gripper": gripper,
        "holding_optic": optic,
        "joints": {
            "base": joints[0],
            "shoulder": joints[1],
            "elbow": joints[2],
            "wrist_pitch": joints[3],
            "wrist_roll": joints[4],
            "wrist_yaw": joints[5],
        },
        "torque_avg": round(12 + random.uniform(-1, 1), 1),
        "temp_c": round(38 + random.uniform(-2, 3), 1),
        "cycle_count": int(t / 12),
        "accuracy_mm": round(0.8 + random.uniform(-0.1, 0.1), 2),
    }


def mock_escort_state(t: float) -> dict:
    """Simulate escort bot cycling through a vendor escort sequence."""
    cycle = t % 30  # 30-second loop
    phase = "idle"
    scan_pct = 0
    alert = None

    if cycle < 3:
        phase = "idle"
        location = "charging_bay"
        vendor = None
    elif cycle < 5:
        phase = "dispatched"
        location = "aisle_a"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
    elif cycle < 12:
        phase = "escorting"
        location = "aisle_a"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
    elif cycle < 14:
        phase = "arrived"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
    elif cycle < 20:
        phase = "scanning"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
        scan_pct = min(100, int(((cycle - 14) / 6) * 100))
    elif cycle < 22:
        phase = "monitoring"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
        scan_pct = 100
        if 20.5 < cycle < 21.5:
            alert = {"ru": "RU-25", "type": "brief_contact", "status": "checking"}
        elif 21.5 <= cycle < 22:
            alert = {"ru": "RU-25", "type": "brief_contact", "status": "cleared"}
    elif cycle < 24:
        phase = "verified"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
        scan_pct = 100
    else:
        phase = "returning"
        location = "aisle_a"
        vendor = None

    return {
        "type": "escort",
        "phase": phase,
        "location": location,
        "vendor": vendor,
        "target_rack": "CAB-B3",
        "authorized_ru": "RU-24",
        "scan_progress": scan_pct,
        "alert": alert,
        "battery_pct": max(20, 95 - int(t / 10)),
        "nodes_scanned": min(5, int(scan_pct / 20)),
    }


MOCK_SCANS = [
    {
        "id": "scan-001",
        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
        "vendor": "TechCo Field Eng.",
        "ticket": "INC-40821",
        "rack": "CAB-B3",
        "authorized_ru": "RU-24",
        "result": "clean",
        "unauthorized": 0,
        "nodes_scanned": 5,
        "flags": ["RU-22 PSU amber"],
        "duration_s": 285,
    },
    {
        "id": "scan-002",
        "timestamp": (datetime.now() - timedelta(hours=7)).isoformat(),
        "vendor": "NetServ Inc.",
        "ticket": "INC-40798",
        "rack": "CAB-A2",
        "authorized_ru": "RU-16",
        "result": "clean",
        "unauthorized": 0,
        "nodes_scanned": 8,
        "flags": [],
        "duration_s": 340,
    },
    {
        "id": "scan-003",
        "timestamp": (datetime.now() - timedelta(days=1, hours=2)).isoformat(),
        "vendor": "DataLink Corp.",
        "ticket": "INC-40712",
        "rack": "CAB-B1",
        "authorized_ru": "RU-30",
        "result": "flagged",
        "unauthorized": 1,
        "nodes_scanned": 6,
        "flags": ["RU-29 unauthorized contact — not resolved", "RU-30 optic swapped"],
        "duration_s": 410,
    },
]


def mock_training_state(t: float) -> dict:
    """Simulate training pipeline state."""
    # Cycle through states over time
    stage_cycle = int(t / 60) % 4
    stages = ["idle", "recording", "uploading", "training"]
    stage = stages[stage_cycle]

    episodes = int(t / 15) % 50
    if stage == "recording":
        progress = (t % 60) / 60 * 100
    elif stage == "uploading":
        progress = min(100, (t % 60) / 30 * 100)
    elif stage == "training":
        progress = min(100, (t % 60) / 50 * 100)
    else:
        progress = 0

    return {
        "type": "training",
        "stage": stage,
        "episodes_recorded": episodes,
        "current_progress": round(progress, 1),
        "model": "ACT-v1",
        "policy": "act",
        "last_loss": round(0.15 - 0.001 * min(episodes, 40) + random.uniform(-0.005, 0.005), 4),
        "gpu": "A100-80G" if stage == "training" else None,
        "cost_so_far": round(episodes * 0.12, 2),
    }


# ── WebSocket endpoint ──────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    start = time.time()

    # Send scan history once on connect
    await ws.send_json({"type": "scan_history", "scans": MOCK_SCANS})

    try:
        while True:
            t = time.time() - start

            # Send all state updates
            await ws.send_json(mock_arm_state(t))
            await ws.send_json(mock_escort_state(t))
            await ws.send_json(mock_training_state(t))

            await asyncio.sleep(0.1)  # 10Hz update rate
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
