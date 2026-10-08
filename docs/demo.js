// "Så mäts en kommun": spelar upp mätningen för riktiga organisationer ur data.json.
// Inget här är påhittat: kommandona är de som matning.py gör, svaren är de som
// sparades, och utslaget är klassningen från klassa_v2.py. Exemplen väljs efter
// vilken regel som slog till, så animationen följer med när datan ändras.

// Ett exempel per regel. Saknas en sort i datan hoppas den över.
const EXEMPEL = [
  { namn: "MX pekar på Microsoft", passar: o => o.epost === "MS" && o.signaler.S1 === "MS" && o.signaler.S7 === "MS",
    regel: "MX pekar på Microsoft (S1)" },
  { namn: "MX pekar på Google", passar: o => o.epost === "G" && o.signaler.S1 === "G",
    regel: "MX pekar på Google (S1)" },
  { namn: "Spamfilter framför", passar: o => o.epost === "MS" && o.signaler.S1 === "gateway/egen" && o.signaler.S2 === "MS" && o.signaler.S7 === "MS",
    regel: "spamfilter framför, men SPF och DKIM pekar på Microsoft (S2 + S7)" },
];

const LEVERANTOR = { MS: "Microsoft", G: "Google" };

function startaDemo(org, { etikett, farg }) {
  const term = document.getElementById("term"), sig = document.getElementById("sig");
  const utslag = document.getElementById("utslag"), namnEl = document.getElementById("demoNamn");
  const prickar = document.getElementById("prickar");
  const lugn = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // En prick per organisation, i länsordning, som fylls i när den mätts.
  const ordning = [...org].sort((a, b) => a.lan.localeCompare(b.lan, "sv") || a.namn.localeCompare(b.namn, "sv"));
  const prick = new Map(ordning.map(o => {
    const i = document.createElement("i");
    i.title = `${o.namn}: ${etikett[o.epost]}`;
    prickar.append(i);
    return [o, i];
  }));

  let synlig = true;
  new IntersectionObserver(([e]) => { synlig = e.isIntersecting; }).observe(term);
  const vanta = ms => new Promise(klar => {
    if (lugn) return klar();
    const slut = performance.now() + ms;
    (function tick() { (synlig && performance.now() >= slut) ? klar() : requestAnimationFrame(tick); })();
  });

  function rad(klass, text = "") {
    const r = document.createElement("span");
    r.className = klass;
    r.textContent = text;
    term.append(r, "\n");
    return r;
  }
  async function skriv(kommando) {
    const r = rad("prompt", "$ ");
    const text = document.createElement("span");
    text.className = "markor";
    r.append(text);
    for (const tecken of kommando) {
      text.textContent += tecken;
      await vanta(lugn ? 0 : 22);
    }
    text.className = "";
    await vanta(350);
  }

  const SIGNALER = [
    ["S1", "MX", "vem tar emot e-posten"],
    ["S2", "SPF", "vem får skicka i kommunens namn"],
    ["S7", "DKIM", "vem signerar e-posten"],
    ["S5", "Microsoft-konto", "finns en Entra-tenant"],
  ];
  const sigRad = {};
  for (const [kod, namn, forklaring] of SIGNALER) {
    const li = document.createElement("li");
    const vanster = document.createElement("span");
    vanster.innerHTML = `<b>${kod} ${namn}</b><small>${forklaring}</small>`;
    const tagg = document.createElement("span");
    tagg.className = "tagg";
    li.append(vanster, tagg);
    sig.append(li);
    sigRad[kod] = { li, tagg };
  }
  function satt(kod, varde) {
    const { li, tagg } = sigRad[kod];
    sig.querySelectorAll("li").forEach(x => x.classList.remove("aktiv"));
    li.classList.add("aktiv");
    const lev = { MS: "MS", G: "G", ja: "MS" }[varde];
    tagg.textContent = varde === "ja" ? "finns" : varde === "gateway/egen" ? "spamfilter/egen" : LEVERANTOR[varde] || "inget";
    tagg.style.background = lev ? farg[lev] : "var(--okand)";
    tagg.style.opacity = 1;
  }
  function nollstall() {
    term.textContent = "";
    utslag.classList.remove("syns");
    for (const { li, tagg } of Object.values(sigRad)) { li.classList.remove("aktiv"); tagg.style.opacity = 0; }
  }

  async function mat(o, exempel) {
    nollstall();
    namnEl.textContent = `${o.namn} · ${o.lan}`;
    const d = o.doman, s = o.svar;

    await skriv(`dig +short MX ${d}`);
    s.mx.slice(0, 2).forEach(h => rad("svar traff", h));
    if (s.mx.length > 2) rad("svar", `… och ${s.mx.length - 2} till`);
    satt("S1", o.signaler.S1);
    await vanta(900);

    await skriv(`dig +short TXT ${d} | grep spf`);
    const spf = rad("svar", s.spf ? `"v=spf1 … include:` : `"v=spf1 …"`);
    if (s.spf) spf.append(Object.assign(document.createElement("span"), { className: "traff", textContent: s.spf }), ` …"`);
    satt("S2", o.signaler.S2);
    await vanta(900);

    await skriv(`dig +short CNAME selector1._domainkey.${d}`);
    rad(s.dkim ? "svar traff" : "svar", s.dkim ? "…" + s.dkim.replace(/\.$/, "").split("._domainkey.")[1] : "(inget svar)");
    satt("S7", o.signaler.S7);
    await vanta(900);

    await skriv(`curl -s -o /dev/null -w "%{http_code}" login.microsoftonline.com/${d}/…`);
    rad(s.entra === 200 ? "svar traff" : "svar", String(s.entra));
    satt("S5", s.entra === 200 ? "ja" : "-");
    await vanta(700);

    sig.querySelectorAll("li").forEach(x => x.classList.remove("aktiv"));
    utslag.replaceChildren(
      Object.assign(document.createElement("span"), { className: "tagg", textContent: etikett[o.epost], style: `background:${farg[o.epost]}` }),
      `${exempel.regel}.` + (o.epost === "G" && o.signaler.S7 === "MS" ? " DKIM pekar ändå på Microsoft: e-posten skickas troligen därifrån." : ""),
    );
    utslag.classList.add("syns");
    const p = prick.get(o);
    p.style.background = farg[o.epost];
    p.classList.add("ny");
    await vanta(2600);
    p.classList.remove("ny");
  }

  async function fyllResten(gjorda) {
    namnEl.textContent = `… och samma regler för alla ${org.length}`;
    const kvar = ordning.filter(o => !gjorda.has(o));
    const steg = Math.max(1, Math.ceil(kvar.length / 60));
    for (let i = 0; i < kvar.length; i += steg) {
      for (const o of kvar.slice(i, i + steg)) prick.get(o).style.background = farg[o.epost];
      await vanta(30);
    }
  }

  const slump = lista => lista[Math.floor(Math.random() * lista.length)];
  (async function spela() {
    for (;;) {
      prick.forEach(i => { i.style.background = ""; });
      const gjorda = new Set();
      for (const ex of EXEMPEL) {
        const kandidater = org.filter(ex.passar);
        if (!kandidater.length) continue;
        const o = slump(kandidater);
        gjorda.add(o);
        await mat(o, ex);
      }
      await fyllResten(gjorda);
      if (lugn) return;
      await vanta(5000);
    }
  })();
}
