'use strict';

// ── Constants ────────────────────────────────────────────────────────────────
const CANVAS_W   = 1400;
const CANVAS_H   = 760;
const RACK_W     = 56;
const RACK_H     = 26;
const WAVE_SPEED = 130;   // px/sec
const WAVE_MAX_R = 420;
const RING_GAP   = 38;    // px lag between concentric rings

const TECHS = {
  alpha:   { color: '#4da6ff', label: 'ALPHA',   defaultRack: 'A07' },
  bravo:   { color: '#ff6b6b', label: 'BRAVO',   defaultRack: 'B03' },
  charlie: { color: '#51cf66', label: 'CHARLIE', defaultRack: 'C10' },
  delta:   { color: '#ffd43b', label: 'DELTA',   defaultRack: 'D05' },
  echo:    { color: '#cc5de8', label: 'ECHO',    defaultRack: 'E12' },
  foxtrot: { color: '#ff922b', label: 'FOXTROT', defaultRack: 'F02' },
  golf:    { color: '#20c997', label: 'GOLF',    defaultRack: 'G08' },
  hotel:   { color: '#f06595', label: 'HOTEL',   defaultRack: 'H14' },
};

// ── State ────────────────────────────────────────────────────────────────────
let canvas, ctx, floorData, rackMap = {};
let techName = null, techColor = null, selectedRackId = null;
let waves = [];
let flashes = {};    // rackId → { alpha, color }
let ws = null, connected = false;
let lastTime = 0;
let simTimer = null;

// ── Init ─────────────────────────────────────────────────────────────────────
async function init() {
  canvas = document.getElementById('floor-canvas');
  ctx = canvas.getContext('2d');

  const res = await fetch('/floor.json');
  floorData = await res.json();
  floorData.racks.forEach(r => { rackMap[r.id] = r; });

  canvas.addEventListener('click', onCanvasClick);
  document.addEventListener('keydown', e => {
    if (e.code === 'Space' && techName) { e.preventDefault(); fireTap(); }
  });

  const params = new URLSearchParams(window.location.search);
  const tech = params.get('tech');
  selectTech(tech && TECHS[tech] ? tech : 'alpha');

  requestAnimationFrame(loop);
}

function selectTech(name) {
  techName    = name;
  techColor   = TECHS[name].color;
  selectedRackId = TECHS[name].defaultRack;

  const hudTech = document.getElementById('hud-tech');
  hudTech.textContent = TECHS[name].label;
  hudTech.style.color = techColor;

  const badge = document.getElementById('tech-badge');
  badge.style.display = 'flex';
  badge.style.borderColor = techColor + '44';
  const dot = document.getElementById('badge-dot');
  dot.style.background = techColor;
  dot.style.boxShadow = `0 0 6px ${techColor}88`;
  const badgeName = document.getElementById('badge-name');
  badgeName.textContent = TECHS[name].label;
  badgeName.style.color = techColor;

  document.getElementById('hud-rack').textContent = selectedRackId;

  const btn = document.getElementById('tap-btn');
  btn.disabled = false;
  btn.style.borderColor = techColor;
  btn.style.color       = techColor;

  connectWS();
}

// ── WebSocket ────────────────────────────────────────────────────────────────
function connectWS() {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new WebSocket(`${proto}//${location.host}`);

  ws.onopen = () => {
    connected = true;
    document.getElementById('conn-dot').style.background = '#51cf66';
    document.getElementById('conn-label').textContent = 'LIVE';
  };

  ws.onclose = () => {
    connected = false;
    document.getElementById('conn-dot').style.background = '#ff4444';
    document.getElementById('conn-label').textContent = 'OFFLINE';
    setTimeout(connectWS, 2000);
  };

  ws.onmessage = (e) => {
    const event = JSON.parse(e.data);
    if (event.type === 'tap') spawnWave(event);
  };
}

// ── Actions ──────────────────────────────────────────────────────────────────
function fireTap() {
  if (!techName || !selectedRackId || !ws || ws.readyState !== 1) return;
  const rack = rackMap[selectedRackId];
  ws.send(JSON.stringify({
    type: 'tap',
    techId: techName,
    rackId: selectedRackId,
    x: rack.x, y: rack.y,
    color: techColor,
  }));

  // Tactile feedback on button
  const btn = document.getElementById('tap-btn');
  btn.textContent = 'SENT';
  setTimeout(() => { btn.textContent = 'TASK DONE'; }, 600);
}

function onCanvasClick(e) {
  if (!techName) return;
  const rect  = canvas.getBoundingClientRect();
  const scaleX = CANVAS_W / rect.width;
  const scaleY = CANVAS_H / rect.height;
  const cx = (e.clientX - rect.left) * scaleX;
  const cy = (e.clientY - rect.top)  * scaleY;

  let best = null, bestDist = Infinity;
  floorData.racks.forEach(r => {
    const d = Math.hypot(r.x - cx, r.y - cy);
    if (d < bestDist && d < 48) { bestDist = d; best = r; }
  });

  if (best) {
    selectedRackId = best.id;
    document.getElementById('hud-rack').textContent = best.id;
  }
}

// ── Simulate (demo) ──────────────────────────────────────────────────────────
function toggleSimulate() {
  const btn = document.getElementById('sim-btn');
  if (simTimer) {
    clearInterval(simTimer);
    simTimer = null;
    btn.classList.remove('active');
    btn.textContent = 'SIMULATE';
    return;
  }
  btn.classList.add('active');
  btn.textContent = 'STOP';

  const techKeys   = Object.keys(TECHS);
  const rackIds    = floorData.racks.map(r => r.id);

  simTimer = setInterval(() => {
    const techKey = techKeys[Math.floor(Math.random() * techKeys.length)];
    const rackId  = rackIds[Math.floor(Math.random() * rackIds.length)];
    const rack    = rackMap[rackId];
    spawnWave({
      type: 'tap',
      techId: techKey,
      rackId,
      x: rack.x, y: rack.y,
      color: TECHS[techKey].color,
    });
  }, 420);
}

// ── Wave system ──────────────────────────────────────────────────────────────
function spawnWave({ x, y, color, rackId }) {
  // 3 concentric rings with staggered starts
  waves.push({ x, y, color, r: 0,           maxA: 0.85 });
  waves.push({ x, y, color, r: -RING_GAP,   maxA: 0.50 });
  waves.push({ x, y, color, r: -RING_GAP*2, maxA: 0.25 });
  flashes[rackId] = { alpha: 1.0, color };
}

// ── Animation loop ───────────────────────────────────────────────────────────
function loop(time) {
  const dt = Math.min((time - lastTime) / 1000, 0.1);
  lastTime = time;
  update(dt);
  render();
  requestAnimationFrame(loop);
}

function update(dt) {
  waves = waves.filter(w => w.r < WAVE_MAX_R);
  waves.forEach(w => { w.r += WAVE_SPEED * dt; });

  Object.keys(flashes).forEach(id => {
    flashes[id].alpha -= dt * 1.8;
    if (flashes[id].alpha <= 0) delete flashes[id];
  });
}

// ── Render ───────────────────────────────────────────────────────────────────
function render() {
  ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);

  // Background
  ctx.fillStyle = '#0a0f1c';
  ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

  drawPodLabels();
  drawAisleLines();
  drawColumnNumbers();

  // Waves (behind racks)
  waves.forEach(drawWave);

  // Racks
  floorData.racks.forEach(drawRack);

  // Row labels
  drawRowLabels();
}

function drawPodLabels() {
  ctx.font = '9px Courier New';
  ctx.letterSpacing = '3px';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';
  floorData.pods.forEach(pod => {
    ctx.fillStyle = '#1a2540';
    ctx.fillText(pod.label, 20, pod.y);
  });
  ctx.letterSpacing = '0px';
}

function drawAisleLines() {
  // Subtle horizontal separators between pods
  const aisleY = [210, 380, 550];
  ctx.strokeStyle = '#111828';
  ctx.lineWidth = 1;
  aisleY.forEach(y => {
    ctx.beginPath();
    ctx.setLineDash([4, 8]);
    ctx.moveTo(80, y);
    ctx.lineTo(CANVAS_W - 20, y);
    ctx.stroke();
  });
  ctx.setLineDash([]);
}

function drawColumnNumbers() {
  ctx.font = '8px Courier New';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = '#1a2540';
  for (let col = 1; col <= 14; col++) {
    const x = 120 + (col - 1) * 90;
    ctx.fillText(String(col).padStart(2, '0'), x, 30);
  }
}

function drawRowLabels() {
  ctx.font = '11px Courier New';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const rows = ['A','B','C','D','E','F','G','H'];
  const ys   = [90, 155, 265, 330, 440, 505, 615, 680];
  rows.forEach((r, i) => {
    ctx.fillStyle = '#253550';
    ctx.fillText(r, 60, ys[i]);
  });
}

function drawRack(rack) {
  const { x, y, id } = rack;
  const isSelected = id === selectedRackId;
  const flash = flashes[id];
  const hw = RACK_W / 2, hh = RACK_H / 2;

  // Flash glow under the rack
  if (flash && flash.alpha > 0) {
    ctx.save();
    ctx.globalAlpha = Math.max(0, flash.alpha) * 0.7;
    ctx.shadowColor = flash.color;
    ctx.shadowBlur  = 24;
    ctx.fillStyle   = flash.color;
    roundRect(ctx, x - hw, y - hh, RACK_W, RACK_H, 3);
    ctx.fill();
    ctx.restore();
  }

  // Rack body
  ctx.fillStyle   = isSelected ? '#15213a' : '#0f1828';
  ctx.strokeStyle = isSelected ? techColor  : '#1c2b44';
  ctx.lineWidth   = isSelected ? 1.5 : 1;
  roundRect(ctx, x - hw, y - hh, RACK_W, RACK_H, 3);
  ctx.fill();
  ctx.stroke();

  // Rack label
  ctx.font         = '8px Courier New';
  ctx.textAlign    = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle    = isSelected ? (techColor + 'cc') : '#1e3050';
  ctx.fillText(id, x, y);
}

function drawWave(w) {
  if (w.r <= 0) return;
  const opacity = Math.max(0, w.maxA * (1 - w.r / WAVE_MAX_R));
  if (opacity <= 0) return;

  ctx.save();
  ctx.globalAlpha = opacity;
  ctx.strokeStyle = w.color;
  ctx.shadowColor = w.color;
  ctx.shadowBlur  = 10;
  ctx.lineWidth   = 1.5;
  ctx.beginPath();
  ctx.arc(w.x, w.y, w.r, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y,     x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h,     x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y,         x + r, y);
  ctx.closePath();
}
