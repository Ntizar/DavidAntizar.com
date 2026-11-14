import io
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def leer(p):
    return io.open(os.path.join(RAIZ, p), encoding='utf-8').read()


def escribir(p, s):
    io.open(os.path.join(RAIZ, p), 'w', encoding='utf-8').write(s)


def rep(s, a, b, etiqueta=''):
    if a not in s:
        raise SystemExit('NO ENCONTRADO ' + (etiqueta or a[:60]))
    return s.replace(a, b)


# ══════════════════════════ 1) PORTADA ══════════════════════════
s = leer('index.html')

# — capa de efectos del sobre —
EFECTOS = r'''
/* ── capa de efectos: lo que lo hace parecer un objeto ── */
.escena{animation:flota 9s ease-in-out infinite}
@keyframes flota{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
/* el reflejo que sigue al ratón: la señal de que es lámina */
.pack__luz{
  position:absolute;inset:0;z-index:3;border-radius:12px;pointer-events:none;
  background:radial-gradient(40% 46% at var(--mx,30%) var(--my,16%),
    rgba(255,255,255,.85),rgba(255,255,255,.16) 46%,rgba(255,255,255,0) 74%);
  mix-blend-mode:screen;opacity:.5;transition:opacity .35s;
}
.pack:hover .pack__luz{opacity:.9}
/* un reflejo que pasa solo cada pocos segundos */
.pack__reflejo{
  position:absolute;inset:-40%;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:linear-gradient(112deg,rgba(255,255,255,0) 44%,rgba(255,255,255,.7) 50%,rgba(255,255,255,0) 56%);
  animation:reflejoAuto 7s ease-in-out infinite;
}
@keyframes reflejoAuto{
  0%,58%{opacity:0;transform:translateX(-75%)}
  68%{opacity:.85}
  100%{opacity:0;transform:translateX(75%)}
}
/* el portal gira: dos copias mezcladas en screen */
.pack__arte-giro{
  position:absolute;inset:-8%;width:116%;height:116%;object-fit:cover;
  opacity:.34;mix-blend-mode:screen;animation:giraPortal 64s linear infinite;
  -webkit-mask-image:radial-gradient(closest-side,#000 42%,transparent 76%);
  mask-image:radial-gradient(closest-side,#000 42%,transparent 76%);
}
@keyframes giraPortal{to{transform:rotate(360deg)}}
/* cremalleras con dientes redondeados */
.pack__cremallera{
  height:13px;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.95) 0 2px,rgba(146,154,168,.55) 2px 4px);
  box-shadow:inset 0 2px 0 rgba(255,255,255,.9),inset 0 -2px 2px rgba(60,68,84,.45);
}
.pack__tira::before{
  content:'';position:absolute;left:0;right:0;top:0;height:12px;z-index:1;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.95) 0 2px,rgba(146,154,168,.5) 2px 4px);
  box-shadow:inset 0 2px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(90,98,112,.4);
}
@media (prefers-reduced-motion:reduce){
  .escena{animation:none}
  .pack__reflejo,.pack__arte-giro{animation:none;opacity:.18}
}
'''
s = rep(s, '</style>', EFECTOS + '</style>', 'cierre de style')

# — nodos nuevos —
s = rep(s, '<span class="pack__aro" aria-hidden="true"></span>',
        '<span class="pack__aro" aria-hidden="true"></span>\n          <span class="pack__luz" aria-hidden="true"></span>\n          <span class="pack__reflejo" aria-hidden="true"></span>',
        'aro')

s = rep(s, '<span class="pack__arte"><img src="assets/cartas/pack-portal.webp" alt="Portal cósmico violeta y azul" width="760" height="760" decoding="async"></span>',
        '<span class="pack__arte"><img src="assets/cartas/pack-portal.webp" alt="Portal cósmico violeta y azul" width="760" height="760" decoding="async"><img class="pack__arte-giro" src="assets/cartas/pack-portal.webp" alt="" aria-hidden="true" width="760" height="760" decoding="async"></span>',
        'arte')

# — luz que sigue al puntero —
s = rep(s, "/* tirar de la pestaña hacia arriba (además del clic) */",
        """/* el reflejo sigue al puntero */
const luzPack = document.querySelector('.pack__luz');
if (luzPack && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce){
  pack.addEventListener('pointermove', (e) => {
    const r = pack.getBoundingClientRect();
    luzPack.style.setProperty('--mx', Math.round((e.clientX - r.left) / r.width * 100) + '%');
    luzPack.style.setProperty('--my', Math.round((e.clientY - r.top) / r.height * 100) + '%');
  });
}

/* tirar de la pestaña hacia arriba (además del clic) */""",
        'js tirar')

# — la carta y el enlace —
s = rep(s, "nombre:'Una tarde con Agorazein'", "nombre:'Una tarde conmigo y mis colegas'", 'nombre carta')
s = rep(s, "url:'agorazein.html'", "url:'subasta.html'", 'url carta')
s = rep(s, '<a href="agorazein.html">La subasta del 17N</a>', '<a href="subasta.html">La subasta del 17N</a>', 'noscript')
escribir('index.html', s)

# ══════════════════════════ 2) LA SUBASTA ══════════════════════════
s = leer('agorazein.html')

s = rep(s, '<title>Una tarde con Agorazein — subasta</title>', '<title>Una tarde conmigo y mis colegas — subasta</title>', 'title')
s = rep(s, 'content="Subasta de una tarde: martes 17 de noviembre, de 18:00 a 00:00, con la entrada del concierto de Agorazein incluida. Sale por 50 €. La puja cierra el lunes 16 a las 18:00."',
        'content="Subasta de una tarde: martes 17 de noviembre, de 18:00 a 00:00, con la entrada de un concierto incluida. Sale por 50 €. La puja cierra el lunes 16 a las 18:00."', 'desc')
s = rep(s, '<meta property="og:title" content="Una tarde con Agorazein — subasta">', '<meta property="og:title" content="Una tarde conmigo y mis colegas — subasta">', 'og title')
s = rep(s, 'content="Martes 17N, de 18:00 a 00:00. Entrada incluida. Sale por 50 €. Una sola plaza."', 'content="Martes 17N, de 18:00 a 00:00. Entrada de concierto incluida. Sale por 50 €. Una sola plaza."', 'og desc')
s = rep(s, 'https://davidantizar.com/agorazein.html', 'https://davidantizar.com/subasta.html', 'canonical')

s = rep(s, 'href="agorazein.html"', 'href="subasta.html"', 'enlace vuelta') if 'href="agorazein.html"' in s else s

s = rep(s, '<span class="carta-grande__nombre">Una tarde con Agorazein</span>',
        '<span class="carta-grande__nombre">Una tarde conmigo y mis colegas</span>', 'nombre grande')

s = rep(s, '''      <h1 class="titular">Subasto mi tarde del martes
        <span>Sale por 50 €. Se lleva seis horas conmigo y mi gente, y la entrada del concierto de Agorazein va incluida.</span>
      </h1>''',
        '''      <h1 class="titular">Una tarde conmigo y mis colegas
        <span>Sale por 50 €. Seis horas conmigo y mi gente, y te invitamos a un concierto con la entrada incluida.</span>
      </h1>''', 'h1')

s = rep(s, 'Hay un concierto de Agorazein en Madrid, cerca de Goya, y alrededor una gente que hace cosas raras e interesantes para ganarse la vida.',
        'Hay un concierto en Madrid, cerca de Goya, y alrededor una gente que hace cosas raras e interesantes para ganarse la vida.', 'entrada')
s = rep(s, '<p class="plan__que">Agorazein</p>', '<p class="plan__que">Un concierto</p>', 'plan')
s = rep(s, '<p class="plan__det">Vamos en grupo y no te suelto. Tu entrada va incluida en la puja.</p>',
        '<p class="plan__det">Vamos en grupo y no te suelto. La entrada va incluida en la puja.</p>', 'plan det')
s = rep(s, '(Agorazein, entrada incluida)', '(entrada incluida)', 'cuerpo mail')

if 'agorazein' in s.lower():
    resto = [l for l in s.split('\n') if 'agorazein' in l.lower()]
    raise SystemExit('QUEDA AGORAZEIN: ' + ' | '.join(resto)[:300])

escribir('subasta.html', s)

# — redirección desde la url vieja —
escribir('agorazein.html', '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=subasta.html">
<link rel="canonical" href="https://davidantizar.com/subasta.html">
<title>La subasta</title>
</head>
<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#05070A;color:#F7F3EA;font-family:system-ui,sans-serif">
<p><a href="subasta.html" style="color:#E0B25C">Esta página se ha mudado aquí</a></p>
</body>
</html>
''')

print('ok: portada, subasta.html y redirección')
