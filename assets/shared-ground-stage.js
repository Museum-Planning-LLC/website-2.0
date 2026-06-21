// Shared Ground — interactive stage (from mark-walhimer.com installation)
const IMG_BASE = '../content/uploads/2026/shared-ground/';

let fsActive = false;
function openStageFullscreen() {
  const modal = document.getElementById('stage-modal');
  modal.style.display = 'flex';
  fsActive = true;
  const fc = document.getElementById('fs-canvas');
  fc.width = window.innerWidth;
  fc.height = window.innerHeight;
  modal.addEventListener('mousemove', fsMouse);
}
function closeStageFullscreen() {
  document.getElementById('stage-modal').style.display = 'none';
  document.getElementById('stage-modal').removeEventListener('mousemove', fsMouse);
  fsActive = false;
}
function fsMouse(e) {
  const fc = document.getElementById('fs-canvas');
  mouseX = e.clientX * (W / fc.offsetWidth);
  mouseY = e.clientY * (H / fc.offsetHeight);
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeStageFullscreen(); });

// ── IMAGE ARCHIVE WITH METADATA ───────────────────────────────────────
// community: which history this image belongs to
// themes: content tags driving contextual selection
// convergence: true = surfaces when histories approach each other
// include: false = present in archive, excluded from walls (KKK photo)
const ARCHIVE = [
  {
    src: IMG_BASE + '01-lucinda-davis-woman-of-black-and-creek-heritage.jpg',
    cap: 'Lucinda Davis — woman of Black and Creek heritage',
    era: '1800s', community: ['african-american','native-american'],
    themes: ['identity','land','witness','family'],
    emotional_register: 'dignity', convergence: true
  },
  {
    src: IMG_BASE + '02-creek-nation-portrait-c-1820s.jpg',
    cap: 'Creek Nation — portrait, c.1820s',
    era: '1820s', community: ['native-american'],
    themes: ['land','identity','before'],
    emotional_register: 'presence', convergence: false
  },
  {
    src: IMG_BASE + '03-mcintosh-treaty-with-creeks-float-1921-centennial-parade.jpg',
    cap: 'McIntosh & Treaty with Creeks Float — 1921 Centennial Parade',
    era: '1921', community: ['white'],
    themes: ['erasure','performance','land','ceremony','power'],
    emotional_register: 'appropriation', convergence: true
  },
  {
    src: IMG_BASE + '04-black-cotton-farming-family-henry-county.jpg',
    cap: 'Black cotton farming family — Henry County',
    era: '1890s', community: ['african-american'],
    themes: ['labor','family','land','cotton','dignity'],
    emotional_register: 'dignity', convergence: false
  },
  {
    src: IMG_BASE + '05-cotton-field-with-overseer-georgia.jpg',
    cap: 'Cotton field with overseer — Georgia',
    era: '1880s', community: ['white','african-american'],
    themes: ['labor','power','cotton','land','coercion'],
    emotional_register: 'power', convergence: true
  },
  {
    src: IMG_BASE + '06-green-tarpley-co-one-bale-cotton-mcdonough-ga-1918.jpg',
    cap: 'Green, Tarpley & Co. — one bale cotton, McDonough GA, 1918',
    era: '1918', community: ['white','african-american'],
    themes: ['commerce','cotton','labor','land','document'],
    emotional_register: 'transaction', convergence: true
  },
  {
    src: IMG_BASE + '07-camp-creek-wreck-henry-county.jpg',
    cap: 'Camp Creek Wreck — Henry County',
    era: '1900s', community: ['african-american','white'],
    themes: ['land','disaster','witness','infrastructure'],
    emotional_register: 'aftermath', convergence: true
  },
  {
    src: IMG_BASE + '08-peace-doves-1921-centennial-parade.jpg',
    cap: 'Peace Doves — 1921 Centennial Parade',
    era: '1921', community: ['white'],
    themes: ['ceremony','celebration','performance'],
    emotional_register: 'celebration', convergence: false
  },
  {
    src: IMG_BASE + '09-mammy-and-banjo-1921-centennial-parade.jpg',
    cap: 'Mammy and Banjo — 1921 Centennial Parade',
    era: '1921', community: ['white'],
    themes: ['erasure','performance','power','caricature'],
    emotional_register: 'erasure', convergence: true
  },
  {
    src: IMG_BASE + '10-mcdonough-georgia-aerial-view-c-1940s.jpg',
    cap: 'McDonough, Georgia — aerial view, c.1940s',
    era: '1940s', community: ['white','african-american'],
    themes: ['land','town','infrastructure','overview'],
    emotional_register: 'witness', convergence: true
  },
  {
    src: IMG_BASE + '11-courthouse-steps-1921-centennial-parade.jpg',
    cap: 'Courthouse Steps — 1921 Centennial Parade',
    era: '1921', community: ['white'],
    themes: ['ceremony','power','civic','land'],
    emotional_register: 'solemnity', convergence: false
  },
  {
    src: IMG_BASE + '12-mcdonough-service-station-standard-oil.jpg',
    cap: 'McDonough Service Station — Standard Oil',
    era: '1950s', community: ['white'],
    themes: ['commerce','infrastructure','daily life'],
    emotional_register: 'everyday', convergence: false
  },
  {
    src: IMG_BASE + '13-first-baptist-church-mcdonough-c-1940s.jpg',
    cap: 'First Baptist Church, McDonough — c.1940s',
    era: '1940s', community: ['white'],
    themes: ['religion','community','architecture','daily life'],
    emotional_register: 'solemnity', convergence: false
  },
  {
    src: IMG_BASE + '14-belles-of-1921-centennial-parade.jpg',
    cap: 'Belles of 1921 — Centennial Parade',
    era: '1921', community: ['white'],
    themes: ['ceremony','gender','performance','celebration'],
    emotional_register: 'celebration', convergence: false
  },
  {
    src: IMG_BASE + '15-transportation-float-1921-centennial-parade.jpg',
    cap: 'Transportation Float — 1921 Centennial Parade',
    era: '1921', community: ['white'],
    themes: ['ceremony','progress','infrastructure','celebration'],
    emotional_register: 'pride', convergence: false
  },
];

// Filtered pools by community / convergence
const PHOTOS = ARCHIVE.filter(p => p.include !== false);
const poolA   = PHOTOS.filter(p => p.community.includes('african-american') || p.community.includes('native-american'));
const poolB   = PHOTOS.filter(p => p.community.includes('white') && !p.convergence);
const poolC   = PHOTOS.filter(p => p.convergence);

// All photos for the archive reel (excluding KKK per artist decision)
const REEL_PHOTOS = PHOTOS;

// Populate archive reel
const reel = document.getElementById('reel');
REEL_PHOTOS.forEach(p => {
  const d = document.createElement('div');
  d.className = 'reel-frame';
  d.innerHTML = `<img src="${p.src}" alt="${p.cap}"/><div class="reel-cap">${p.cap}<br><span style="opacity:0.5;font-size:10px">${p.era} · ${p.emotional_register}</span></div>`;
  reel.appendChild(d);
});

// ── CANVAS / DEMO ─────────────────────────────────────────────────────
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const W = 1280, H = 620;
canvas.width = W; canvas.height = H;

// Load all images
const imgMap = {};
PHOTOS.forEach(p => {
  const i = new Image(); i.src = p.src; imgMap[p.src] = i;
});

function loadedImg(p) { return imgMap[p.src]; }
function pick(pool, exclude) {
  const choices = pool.filter(p => p !== exclude);
  return choices[Math.floor(Math.random() * choices.length)] || pool[0];
}

// Two bodies — A (mouse-controlled), B (autonomous)
let bodyA = { x: W * 0.25, y: H * 0.5 };
let bodyB = { x: W * 0.75, y: H * 0.5 };
let mouseX = W * 0.25, mouseY = H * 0.5;

// B wanders
let bTarget = { x: W * 0.75, y: H * 0.5 };
let bWander = 0;

// Current photo selections — drawn from tagged pools
let photoA = poolA[0];
let photoB = poolB[0];
let photoC = poolC[0];

// State label
const centerLabel = document.getElementById('label-center');
const labelA = document.getElementById('label-a');
const labelB = document.getElementById('label-b');

const stage = document.getElementById('stage');
stage.addEventListener('mousemove', e => {
  const r = canvas.getBoundingClientRect();
  mouseX = (e.clientX - r.left) * (W / r.width);
  mouseY = (e.clientY - r.top) * (H / r.height);
});

let alphaA = 0, alphaB = 0, alphaC = 0;
let targetAlphaA = 0, targetAlphaB = 0, targetAlphaC = 0;
let lastPhotoSwitch = 0;
let tick = 0;

function lerp(a, b, t) { return a + (b - a) * t; }

function draw(ts) {
  requestAnimationFrame(draw);
  tick++;

  // Ease History A toward mouse
  bodyA.x = lerp(bodyA.x, mouseX, 0.06);
  bodyA.y = lerp(bodyA.y, mouseY, 0.06);

  // B wanders autonomously
  bWander += 0.008;
  bTarget.x = W * 0.62 + Math.sin(bWander * 0.7) * W * 0.18;
  bTarget.y = H * 0.5 + Math.cos(bWander * 0.5) * H * 0.25;
  bodyB.x = lerp(bodyB.x, bTarget.x, 0.018);
  bodyB.y = lerp(bodyB.y, bTarget.y, 0.018);

  // Distance between bodies
  const dx = bodyA.x - bodyB.x;
  const dy = bodyA.y - bodyB.y;
  const dist = Math.sqrt(dx * dx + dy * dy);
  const maxDist = W * 0.75;
  const proximity = 1 - Math.min(dist / maxDist, 1); // 0=far, 1=together

  // Metadata-driven photo switching
  // Diverging: each history shows its own community pool
  // Converging: convergence pool surfaces between them
  if (ts - lastPhotoSwitch > 3200) {
    lastPhotoSwitch = ts;
    let photoAChanged = false, photoBChanged = false;
    if (proximity < 0.35) {
      photoA = pick(poolA, photoA); photoAChanged = true;
      photoB = pick(poolB, photoB); photoBChanged = true;
    } else {
      photoC = pick(poolC, photoC);
    }
    updateSound(proximity, photoAChanged, photoBChanged);
  } else {
    updateSound(proximity, false, false);
  }

  // Alpha targets based on proximity
  if (proximity < 0.25) {
    targetAlphaA = 1; targetAlphaB = 1; targetAlphaC = 0;
  } else if (proximity > 0.7) {
    targetAlphaA = 0.4; targetAlphaB = 0.4; targetAlphaC = 1;
  } else {
    targetAlphaA = 0.85; targetAlphaB = 0.85; targetAlphaC = proximity;
  }
  alphaA = lerp(alphaA, targetAlphaA, 0.025);
  alphaB = lerp(alphaB, targetAlphaB, 0.025);
  alphaC = lerp(alphaC, targetAlphaC, 0.025);

  // Update state label
  if (proximity < 0.2) {
    centerLabel.textContent = 'separating — histories diverging';
    centerLabel.style.color = 'rgba(200,168,130,0.5)';
  } else if (proximity > 0.65) {
    centerLabel.textContent = 'converging — something new surfaces';
    centerLabel.style.color = 'var(--accent)';
  } else {
    centerLabel.textContent = 'in motion — the archive listens';
    centerLabel.style.color = 'rgba(200,168,130,0.7)';
  }

  // Corner labels reflect current image metadata
  if (labelA) labelA.textContent = `History A · ${photoA.era} · ${photoA.emotional_register}`;
  if (labelB) labelB.textContent = `History B · ${photoB.era} · ${photoB.emotional_register}`;

  // ── DRAW ────────────────────────────────────────────────────────
  ctx.fillStyle = '#070705';
  ctx.fillRect(0, 0, W, H);

  const imgA = loadedImg(photoA);
  const imgB = loadedImg(photoB);
  const imgC = loadedImg(photoC);

  // Left zone — History A's history
  if (imgA && imgA.complete) {
    ctx.save();
    ctx.globalAlpha = alphaA * 0.72;
    ctx.beginPath();
    ctx.rect(0, 0, W * 0.5, H);
    ctx.clip();
    drawFit(imgA, 0, 0, W * 0.5, H);
    // Sepia
    ctx.globalCompositeOperation = 'multiply';
    ctx.globalAlpha = alphaA * 0.22;
    ctx.fillStyle = 'rgb(160,110,40)';
    ctx.fillRect(0, 0, W * 0.5, H);
    ctx.restore();
  }

  // Right zone — History B's history
  if (imgB && imgB.complete) {
    ctx.save();
    ctx.globalAlpha = alphaB * 0.72;
    ctx.beginPath();
    ctx.rect(W * 0.5, 0, W * 0.5, H);
    ctx.clip();
    drawFit(imgB, W * 0.5, 0, W * 0.5, H);
    ctx.globalCompositeOperation = 'multiply';
    ctx.globalAlpha = alphaB * 0.22;
    ctx.fillStyle = 'rgb(160,110,40)';
    ctx.fillRect(W * 0.5, 0, W * 0.5, H);
    ctx.restore();
  }

  // Center — convergence image blooms between them
  if (alphaC > 0.05 && imgC && imgC.complete) {
    const cx = (bodyA.x + bodyB.x) * 0.5;
    const cy = (bodyA.y + bodyB.y) * 0.5;
    const radius = proximity * W * 0.42;
    ctx.save();
    ctx.globalAlpha = alphaC * 0.9;
    const clip = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
    clip.addColorStop(0, 'rgba(0,0,0,1)');
    clip.addColorStop(0.7, 'rgba(0,0,0,0.85)');
    clip.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.clip();
    drawFit(imgC, cx - radius, cy - radius, radius * 2, radius * 2);
    ctx.restore();
  }

  // Vertical dividing line — fades as bodies converge
  ctx.save();
  ctx.globalAlpha = (1 - proximity) * 0.2;
  ctx.strokeStyle = 'rgba(200,168,130,0.6)';
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 8]);
  ctx.beginPath();
  ctx.moveTo(W * 0.5, 0);
  ctx.lineTo(W * 0.5, H);
  ctx.stroke();
  ctx.restore();

  // Vignette
  const vg = ctx.createRadialGradient(W/2, H/2, H*0.2, W/2, H/2, H*0.9);
  vg.addColorStop(0, 'rgba(0,0,0,0)');
  vg.addColorStop(1, 'rgba(0,0,0,0.65)');
  ctx.fillStyle = vg;
  ctx.fillRect(0, 0, W, H);

  // Grain
  if (tick % 3 === 0) addGrain(0.55);

  // Draw history markers
  drawHistory(bodyA, 'rgba(200,168,130,0.9)', 'A');
  drawHistory(bodyB, 'rgba(240,237,230,0.4)', 'B');

  // Connection thread between bodies — glows as they approach
  if (proximity > 0.1) {
    ctx.save();
    ctx.globalAlpha = proximity * 0.3;
    ctx.strokeStyle = 'rgba(200,168,130,0.8)';
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 6]);
    ctx.beginPath();
    ctx.moveTo(bodyA.x, bodyA.y);
    ctx.lineTo(bodyB.x, bodyB.y);
    ctx.stroke();
    ctx.restore();
  }
}
requestAnimationFrame(draw);

// Mirror main canvas to fullscreen modal when active
function fsDrawMirror() {
  if (fsActive) {
    const fc = document.getElementById('fs-canvas');
    if (!fc) { requestAnimationFrame(fsDrawMirror); return; }
    if (fc.width !== window.innerWidth || fc.height !== window.innerHeight) {
      fc.width = window.innerWidth;
      fc.height = window.innerHeight;
    }
    const fctx = fc.getContext('2d');
    fctx.drawImage(document.getElementById('c'), 0, 0, fc.width, fc.height);
    const cl = document.getElementById('label-center');
    const ml = document.getElementById('modal-label-center');
    if (cl && ml) ml.textContent = cl.textContent;
  }
  requestAnimationFrame(fsDrawMirror);
}
requestAnimationFrame(fsDrawMirror);

function drawHistory(b, color, label) {
  ctx.save();
  ctx.globalAlpha = 0.9;
  // Outer ring
  ctx.beginPath();
  ctx.arc(b.x, b.y, 18, 0, Math.PI * 2);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.stroke();
  // Inner dot
  ctx.beginPath();
  ctx.arc(b.x, b.y, 3, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
  // Label
  ctx.font = "300 9px 'IBM Plex Mono'";
  ctx.fillStyle = color;
  ctx.letterSpacing = '0.1em';
  ctx.fillText(label, b.x + 24, b.y + 4);
  ctx.restore();
}

function drawFit(img, x, y, w, h) {
  const scale = Math.max(w / img.width, h / img.height);
  const sw = img.width * scale, sh = img.height * scale;
  ctx.drawImage(img, x + (w - sw) / 2, y + (h - sh) / 2, sw, sh);
}

let _gc = null, _gx = null;
function addGrain(s) {
  if (!_gc) { _gc = document.createElement('canvas'); _gc.width = 256; _gc.height = 256; _gx = _gc.getContext('2d'); }
  const id = _gx.createImageData(256, 256); const d = id.data;
  for (let i = 0; i < d.length; i += 4) {
    const v = (Math.random() * 2 - 1) * 50 * s;
    d[i] = d[i+1] = d[i+2] = 128 + v;
    d[i+3] = Math.random() * 22 * s;
  }
  _gx.putImageData(id, 0, 0);
  ctx.globalAlpha = s * 0.12;
  for (let y = 0; y < H; y += 256) for (let x = 0; x < W; x += 256) ctx.drawImage(_gc, x, y);
  ctx.globalAlpha = 1;
}

// ── PIANO SOUND — Salamander Grand, pentatonic, event-triggered ──────
// C pentatonic: C D E G A — no wrong notes, any combo sounds consonant
// History A owns the left hand (low register)
// History B owns the right hand (mid register)  
// Convergence events bloom in the upper register
let piano = null;
let soundOn = true;
let pianoReady = false;

const pentatonicA = ['C2','D2','E2','G2','A2','C3','D3','E3'];
const pentatonicB = ['G3','A3','C4','D4','E4','G4'];
const pentatonicBloom = ['C5','E5','G5','A5'];

let lastConvergeState = false; // was it converging last frame?

function buildPiano() {
  if (pianoReady) return;
  pianoReady = true;
  piano = new Tone.Sampler({
    urls: {
      C2:'C2.mp3', 'D#2':'Ds2.mp3', 'F#2':'Fs2.mp3', A2:'A2.mp3',
      C3:'C3.mp3', 'D#3':'Ds3.mp3', 'F#3':'Fs3.mp3', A3:'A3.mp3',
      C4:'C4.mp3', 'D#4':'Ds4.mp3', 'F#4':'Fs4.mp3', A4:'A4.mp3',
      C5:'C5.mp3', 'D#5':'Ds5.mp3', 'F#5':'Fs5.mp3', A5:'A5.mp3',
    },
    release: 4,
    baseUrl: 'https://tonejs.github.io/audio/salamander/',
  }).toDestination();
  Tone.getDestination().volume.value = -8;
}

function playNote(pool, velocity) {
  if (!soundOn || !pianoReady || !piano) return;
  const note = pool[Math.floor(Math.random() * pool.length)];
  piano.triggerAttackRelease(note, '2n', Tone.now(), velocity);
}

// Called by the draw loop on specific events
function onPhotoA() { playNote(pentatonicA, 0.25 + Math.random() * 0.15); }
function onPhotoB() { playNote(pentatonicB, 0.25 + Math.random() * 0.15); }
function onConverge() { playNote(pentatonicBloom, 0.3 + Math.random() * 0.15); }

function toggleSound() {
  soundOn = !soundOn;
  updateSoundBtn();
}

function updateSoundBtn() {
  const btn = document.getElementById('sound-btn');
  if (!btn) return;
  btn.textContent = soundOn ? '◼ sound on' : '▶ sound off';
  btn.style.color = soundOn ? 'rgba(200,168,130,0.9)' : 'rgba(200,168,130,0.35)';
}

function updateSound(proximity, photoAChanged, photoBChanged) {
  // Convergence event: crossing the threshold fires a bloom note
  const isConverging = proximity > 0.65;
  if (isConverging && !lastConvergeState) onConverge();
  lastConvergeState = isConverging;

  // Photo change events fire their history's note
  if (photoAChanged) onPhotoA();
  if (photoBChanged) onPhotoB();
}

document.addEventListener('click', () => {
  Tone.start();
  buildPiano();
}, { once: true });
