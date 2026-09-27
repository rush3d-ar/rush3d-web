// Ficha de la Lámpara NAFTA (RUSH Originals): visor 3D + personalización + pedido por mail.
// Se compila con esbuild a /assets/nafta.js (ver src/README.md).
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {EffectComposer} from 'three/examples/jsm/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/examples/jsm/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/examples/jsm/postprocessing/OutputPass.js';

const ORDER_ENDPOINT = 'https://formsubmit.co/ajax/contacto.rush3d@gmail.com';
const MODEL_URL = '/models/nafta.glb';

/* ---------- Colores (hex publicados por Bambu Lab; Ice/Sky/Dark Blue y Nardo Gray aproximados;
   Ivory White y Charcoal ajustados porque Bambu declara #FFFFFF y #000000) ---------- */
const MATTE = [
  ['Ivory White','#ECE9E1'],['Bone White','#CBC6B8'],['Lemon Yellow','#F7D959'],['Mandarin Orange','#F99963'],
  ['Sakura Pink','#E8AFCF'],['Lilac Purple','#AE96D4'],['Plum','#950051'],['Scarlet Red','#DE4343'],
  ['Dark Red','#BB3D43'],['Apple Green','#C2E189'],['Grass Green','#61C680'],['Dark Green','#68724D'],
  ['Ice Blue','#A3D8E1'],['Sky Blue','#56B7E6'],['Marine Blue','#0078BF'],['Dark Blue','#042F56'],
  ['Desert Tan','#E8DBB7'],['Latte Brown','#D3B7A7'],['Caramel','#AE835B'],['Terracotta','#B15533'],
  ['Dark Brown','#7D6556'],['Dark Chocolate','#4D3324'],['Ash Gray','#9B9EA0'],['Nardo Gray','#757575'],['Charcoal','#26272A']
];
const WOOD = [['Black Walnut','#4F3F24'],['Rosewood','#4C241C'],['Clay Brown','#995F11'],['Classic Birch','#918669'],['White Oak','#D6CCA3'],['Ochre Yellow','#C98935']];
const LIGHTS = {warm:{hex:'#FFB46B',k:'2700K',label:'cálida'}, cold:{hex:'#E4ECFF',k:'6500K',label:'fría'}};

let raf = 0, visible = true;
const state = {body:'Scarlet Red', base:'White Oak', on:false, temp:'warm'};
const $ = (id) => document.getElementById(id);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const hexOf = (list, name) => list.find((x) => x[0] === name)[1];

function buildSwatches(el, list, key, nameEl, wood){
  list.forEach(([name, hex]) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 't-sw' + (wood ? ' t-sw--wood' : ''); b.style.setProperty('--c', hex);
    b.title = name; b.setAttribute('aria-label', name); b.setAttribute('aria-pressed', String(state[key] === name));
    b.addEventListener('click', () => {
      state[key] = name; nameEl.textContent = name;
      el.querySelectorAll('.t-sw').forEach((s) => s.setAttribute('aria-pressed', String(s.title === name)));
      applyColors();
    });
    el.appendChild(b);
  });
}
buildSwatches($('bodySw'), MATTE, 'body', $('bodyName'), false);
buildSwatches($('baseSw'), WOOD, 'base', $('baseName'), true);

/* ---------- Escena (misma receta que el rayo del inicio) ---------- */
const canvas = $('naftaCanvas'), host = $('naftaViewer');
let renderer;
try { renderer = new THREE.WebGLRenderer({canvas, antialias:true}); }
catch (e) { $('naftaLoading').textContent = 'Tu navegador no puede mostrar el modelo 3D'; }

const scene = new THREE.Scene(); scene.background = new THREE.Color('#0c0e12');
const cam = new THREE.PerspectiveCamera(30, 1, .1, 60);
const hemi = new THREE.HemisphereLight(0xdfe6ff, 0x1a0b08, .5); scene.add(hemi);
const key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(3, 5, 4); scene.add(key);
const rim = new THREE.DirectionalLight(0xff3b1f, 2.2); rim.position.set(-4, 2.5, -3); scene.add(rim);
const world = new THREE.Group(); scene.add(world);

const gc = document.createElement('canvas'); gc.width = gc.height = 512; const g = gc.getContext('2d');
g.fillStyle = '#16191e'; g.fillRect(0, 0, 512, 512); g.strokeStyle = 'rgba(255,255,255,0.06)'; g.lineWidth = 1;
for (let i = 0; i <= 512; i += 32){ g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); }
g.strokeStyle = 'rgba(255,59,31,0.35)'; g.lineWidth = 2; g.strokeRect(6, 6, 500, 500);
const gtex = new THREE.CanvasTexture(gc); gtex.colorSpace = THREE.SRGBColorSpace;
const bed = new THREE.Mesh(new THREE.BoxGeometry(3.4, .06, 3.4), new THREE.MeshStandardMaterial({map:gtex, roughness:.55, metalness:.2}));
bed.position.y = -.031; world.add(bed);

const pc = document.createElement('canvas'); pc.width = pc.height = 256; const p = pc.getContext('2d');
const rg = p.createRadialGradient(128, 128, 10, 128, 128, 128);
rg.addColorStop(0, 'rgba(255,255,255,1)'); rg.addColorStop(.35, 'rgba(255,255,255,.45)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
p.fillStyle = rg; p.fillRect(0, 0, 256, 256);
const glowTex = new THREE.CanvasTexture(pc);
const pool = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 3.2), new THREE.MeshBasicMaterial({map:glowTex, transparent:true, blending:THREE.AdditiveBlending, depthWrite:false, opacity:0}));
pool.rotation.x = -Math.PI / 2; pool.position.y = .002; world.add(pool);
const halo = new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex, transparent:true, blending:THREE.AdditiveBlending, depthWrite:false, opacity:0}));
world.add(halo);
const bulb = new THREE.PointLight(0xffb46b, 0, 6, 1.6); world.add(bulb);
const spill = new THREE.PointLight(0xffb46b, 0, 5, 1.8); world.add(spill);

/* ---------- Materiales: líneas de capa + luz que atraviesa la pared según su espesor ---------- */
const S = {uGlow:{value:0}, uLight:{value:new THREE.Color(LIGHTS.warm.hex)}, uAlb:{value:new THREE.Color()}, uLayer:{value:.0075}, uK:{value:.62}};
const shadeMat = new THREE.MeshStandardMaterial({roughness:.88, metalness:0, side:THREE.DoubleSide});
shadeMat.onBeforeCompile = (sh) => {
  Object.assign(sh.uniforms, S);
  sh.vertexShader = sh.vertexShader
    .replace('#include <common>', '#include <common>\nattribute float thick;\nvarying float vThick;\nvarying vec3 vWPos;')
    .replace('#include <project_vertex>', '#include <project_vertex>\nvThick = thick;\nvWPos = (modelMatrix * vec4(transformed,1.0)).xyz;');
  sh.fragmentShader = sh.fragmentShader
    .replace('#include <common>', '#include <common>\nvarying float vThick;\nvarying vec3 vWPos;\nuniform float uGlow;\nuniform vec3 uLight;\nuniform vec3 uAlb;\nuniform float uLayer;\nuniform float uK;')
    .replace('#include <color_fragment>', '#include <color_fragment>\nfloat lf = fract(vWPos.y / uLayer);\nfloat ridge = smoothstep(0.0,0.35,lf)*smoothstep(1.0,0.65,lf);\ndiffuseColor.rgb *= mix(0.86,1.0,ridge);')
    .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\nfloat tr = exp(-vThick * 8.0 * uK);\ntotalEmissiveRadiance += uLight * uAlb * tr * uGlow * 2.1;');
};
const W = {uLayer:{value:.0075}};
const woodMat = new THREE.MeshStandardMaterial({roughness:.78, metalness:0});
woodMat.onBeforeCompile = (sh) => {
  Object.assign(sh.uniforms, W);
  sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWPos;').replace('#include <project_vertex>', '#include <project_vertex>\nvWPos = (modelMatrix * vec4(transformed,1.0)).xyz;');
  sh.fragmentShader = sh.fragmentShader
    .replace('#include <common>', '#include <common>\nvarying vec3 vWPos;\nuniform float uLayer;\nfloat h1(float n){return fract(sin(n*127.1)*43758.5453);}')
    .replace('#include <color_fragment>', '#include <color_fragment>\nfloat li = floor(vWPos.y / uLayer);\nfloat lf = fract(vWPos.y / uLayer);\nfloat ridge = smoothstep(0.0,0.35,lf)*smoothstep(1.0,0.65,lf);\nfloat band = mix(0.88,1.1,h1(li)) * mix(0.9,1.0,h1(floor(li/6.0)+3.0));\ndiffuseColor.rgb *= band * mix(0.84,1.0,ridge);');
};

const lc = new THREE.Color(), tint = new THREE.Color();
function updateLightColors(){
  lc.set(LIGHTS[state.temp].hex);
  S.uLight.value.copy(lc);
  tint.copy(lc).multiply(new THREE.Color(hexOf(MATTE, state.body)));
  bulb.color.copy(lc); spill.color.copy(tint);
  pool.material.color.copy(tint); halo.material.color.copy(lc);
}
function applyColors(){
  shadeMat.color.set(hexOf(MATTE, state.body));
  woodMat.color.set(hexOf(WOOD, state.base));
  S.uAlb.value.set(hexOf(MATTE, state.body));
  updateLightColors(); kick();
}

/* ---------- Luz ---------- */
let glow = 0, glowTarget = 0;
function setLight(on){
  state.on = on; glowTarget = on ? 1 : 0;
  $('lightBtn').setAttribute('aria-pressed', String(on));
  $('lightLbl').textContent = on ? 'Apagar luz' : 'Prender luz';
  $('hudState').innerHTML = on ? `Luz <b>${LIGHTS[state.temp].label} · ${LIGHTS[state.temp].k}</b>` : 'Luz <b>apagada</b>';
  kick();
}
function setTemp(t){
  state.temp = t;
  $('warmBtn').setAttribute('aria-pressed', String(t === 'warm'));
  $('coldBtn').setAttribute('aria-pressed', String(t === 'cold'));
  updateLightColors(); setLight(true);
}
$('lightBtn').addEventListener('click', () => setLight(!state.on));
$('warmBtn').addEventListener('click', () => setTemp('warm'));
$('coldBtn').addEventListener('click', () => setTemp('cold'));

/* ---------- Render ---------- */
let composer, bloom;
if (renderer){
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
  scene.environmentIntensity = .55;
  composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, cam));
  bloom = new UnrealBloomPass(new THREE.Vector2(512, 512), 0, .5, .9); composer.addPass(bloom);
  composer.addPass(new OutputPass());

  const loader = new GLTFLoader(); loader.setMeshoptDecoder(MeshoptDecoder);
  loader.load(MODEL_URL, (gltf) => {
    const root = gltf.scene;
    root.traverse((o) => {
      if (!o.isMesh) return;
      const geo = o.geometry;
      if (geo.attributes.color){
        const c = geo.attributes.color, t = new Float32Array(c.count);
        for (let i = 0; i < c.count; i++) t[i] = c.getX(i);
        geo.setAttribute('thick', new THREE.BufferAttribute(t, 1)); geo.deleteAttribute('color');
        o.material = shadeMat;
      } else {
        if (!geo.attributes.normal) geo.computeVertexNormals();
        o.material = woodMat;
      }
    });
    const holder = new THREE.Group(); holder.add(root);
    root.rotation.x = -Math.PI / 2; holder.scale.setScalar(.012);
    world.add(holder); holder.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(holder);
    holder.position.x -= (box.min.x + box.max.x) / 2; holder.position.z -= (box.min.z + box.max.z) / 2; holder.position.y -= box.min.y;
    const H = box.max.y - box.min.y;
    bulb.position.set(0, H * .42, 0); spill.position.set(0, H * .5, 0);
    halo.position.set(0, H * 1.02, 0); halo.scale.setScalar(H * .9);
    cam.position.set(3.9, 2.9, 5.3).multiplyScalar(H / 2.2); cam.lookAt(0, H * .42, 0);
    $('naftaLoading').classList.add('is-done');
    applyColors();
  }, undefined, () => { $('naftaLoading').textContent = 'No se pudo cargar el modelo'; });
}

let rotY = -.5, vel = 0, drag = false, lastX = 0;
const mouse = new THREE.Vector2(), smooth = new THREE.Vector2();
canvas.addEventListener('pointerdown', (e) => { drag = true; lastX = e.clientX; canvas.setPointerCapture(e.pointerId); kick(); });
canvas.addEventListener('pointermove', (e) => {
  const r = canvas.getBoundingClientRect();
  mouse.set((e.clientX - r.left) / r.width * 2 - 1, (e.clientY - r.top) / r.height * 2 - 1);
  if (drag){ vel += (e.clientX - lastX) * .0022; lastX = e.clientX; }
  kick();
});
const up = () => { drag = false; };
canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
canvas.addEventListener('pointerleave', () => mouse.set(0, 0));

function resize(){
  if (!renderer) return;
  const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return;
  renderer.setSize(w, h, false); composer.setSize(w, h); bloom.setSize(w, h);
  cam.aspect = w / h; cam.fov = w / h < .95 ? 34 : 30; cam.updateProjectionMatrix(); kick();
}
new ResizeObserver(resize).observe(host); resize();

function frame(){
  raf = 0;
  glow += (glowTarget - glow) * .08; if (Math.abs(glowTarget - glow) < .002) glow = glowTarget;
  S.uGlow.value = glow;
  const dim = 1 - glow * .78;
  scene.environmentIntensity = .55 * dim; key.intensity = 2.4 * dim; rim.intensity = 2.2 * (1 - glow * .6); hemi.intensity = .5 * dim;
  bulb.intensity = glow * 9; spill.intensity = glow * 3.2;
  pool.material.opacity = glow * .55; halo.material.opacity = glow * .35;
  bloom.strength = glow * .38;
  if (!reduce) rotY += .0022;
  rotY += vel; vel *= .92;
  smooth.lerp(mouse, .05);
  world.rotation.y = rotY + smooth.x * .25; world.rotation.x = smooth.y * .05;
  composer.render();
  const moving = !reduce || Math.abs(vel) > 1e-4 || glow !== glowTarget || drag || smooth.distanceTo(mouse) > 1e-3;
  if (visible && !document.hidden && moving) raf = requestAnimationFrame(frame);
}
function kick(){ if (renderer && !raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
new IntersectionObserver(([e]) => { visible = e.isIntersecting; kick(); }, {threshold:.01}).observe(host);
document.addEventListener('visibilitychange', kick);
kick();

/* ---------- Pedido ---------- */
const form = $('orderForm');
const toggleLoc = () => { $('locWrap').hidden = !$('f-envio').checked; };
form.addEventListener('change', (e) => { if (e.target.name === 'entrega') toggleLoc(); });
toggleLoc();
function check(id, errId, ok, msg){ $(id).closest('.t-field').classList.toggle('is-bad', !ok); $(errId).textContent = ok ? '' : msg; return ok; }

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  $('formErr').textContent = '';
  const name = $('f-name').value.trim(), mail = $('f-mail').value.trim(), wa = $('f-wa').value.trim(), loc = $('f-loc').value.trim();
  const envio = $('f-envio').checked, msg = $('f-msg').value.trim();
  const ok = [
    check('f-name', 'e-name', name.length >= 3, 'Escribí tu nombre y apellido.'),
    check('f-mail', 'e-mail', /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail), 'Revisá el mail, parece incompleto.'),
    check('f-wa', 'e-wa', wa.replace(/\D/g, '').length >= 8, 'Poné un WhatsApp con código de área.'),
    envio ? check('f-loc', 'e-loc', loc.length >= 3, 'Necesitamos la localidad para cotizar el envío.') : true,
  ].every(Boolean);
  if (!ok){ form.querySelector('.is-bad input')?.focus(); return; }

  const entrega = envio ? `Envío a ${loc}` : 'Retiro en José León Suárez';
  const payload = {
    _subject: `Pedido RUSH Originals · Lámpara NAFTA · ${name}`,
    _template: 'table',
    _captcha: 'false',
    _honey: $('f-hp').value,
    _autoresponse: `Hola ${name.split(' ')[0]}, recibimos tu pedido de la Lámpara NAFTA (pantalla ${state.body}, base ${state.base}). Te escribimos por WhatsApp en menos de 24 h con el precio y las formas de pago. Gracias por elegir un RUSH Original. — Rush 3D`,
    Producto: 'Lámpara NAFTA (RUSH Originals)',
    Pantalla: `Bambu Lab PLA Matte · ${state.body}`,
    Base: `Bambu Lab PLA Wood · ${state.base}`,
    Nombre: name,
    email: mail,
    WhatsApp: wa,
    Entrega: entrega,
    Comentario: msg || '—',
  };
  const btn = $('orderBtn'); btn.disabled = true; $('orderBtnLbl').textContent = 'Enviando…';
  try {
    const res = await fetch(ORDER_ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json', Accept:'application/json'}, body:JSON.stringify(payload)});
    const data = await res.json().catch(() => ({}));
    if (!res.ok || String(data.success) !== 'true') throw new Error(data.message || 'send failed');
    $('sBody').textContent = state.body; $('sBase').textContent = state.base; $('sEntrega').textContent = entrega; $('sMail').textContent = mail;
    form.hidden = true; $('sent').hidden = false;
    $('sent').scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block:'nearest'});
    try { window.gtag?.('event', 'generate_lead', {item_name:'Lámpara NAFTA', pantalla:state.body, base:state.base}); } catch (_) {}
    try { window.fbq?.('track', 'Lead', {content_name:'Lámpara NAFTA'}); } catch (_) {}
    try { window.clarity?.('event', 'pedido_nafta'); } catch (_) {}
  } catch (err) {
    $('formErr').textContent = 'No pudimos enviar el pedido. Probá de nuevo en un rato o escribinos por WhatsApp.';
  } finally {
    btn.disabled = false; $('orderBtnLbl').textContent = 'Enviar pedido';
  }
});
$('backBtn').addEventListener('click', () => { $('sent').hidden = true; form.hidden = false; });
