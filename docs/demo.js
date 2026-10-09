// "Så mäts en kommun": spelar upp mätningen för riktiga organisationer ur data.json.
// Inget här är påhittat: kommandona är de som matning.py gör, svaren är de som
// sparades, och utslaget är klassningen från klassa_v2.py. Exemplen väljs efter
// vilken regel som slog till, så animationen följer med när datan ändras.
// Sista steget är kontrollen T2 (triangulering.py): svarar
// Exchange Online för domänen? Bara ja/nej visas, aldrig adressen den svarar med.

// Ett exempel per regel. Saknas en sort i datan hoppas den över.
const EXEMPEL = [
  { namn: "MX pekar på Microsoft", passar: o => o.epost === "MS" && o.signaler.S1 === "MS" && o.signaler.S7 === "MS",
    regel: "MX pekar på Microsoft (S1)" },
  { namn: "MX pekar på Google", passar: o => o.epost === "G" && o.signaler.S1 === "G",
    regel: "MX pekar på Google (S1)" },
  { namn: "Spamfilter framför", passar: o => o.epost === "MS" && o.signaler.S1 === "gateway/egen" && o.signaler.S2 === "MS" && o.signaler.S7 === "MS",
    regel: "spamfilter framför, men SPF och DKIM pekar på Microsoft (S2 + S7)" },
  { namn: "Inga molnsignaler i DNS", passar: o => o.epost === "inga molnsignaler" && o.exo === true,
    regel: "DNS visar inga molnsignaler (S1, S2, S7)" },
];

const LEVERANTOR = { MS: "Microsoft", G: "Google" };

function startaDemo(org, { etikett, farg, karta, kontrollDatum }) {
  const term = document.getElementById("term"), sig = document.getElementById("sig");
  const utslag = document.getElementById("utslag"), namnEl = document.getElementById("demoNamn");
  const prickar = document.getElementById("prickar");
  const lugn = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Varje organisation får en yta som fylls i när den mätts: kommunen på minikartan
  // när kartan finns, annars en prick. Regionerna har ingen yta på kartan.
  const ordning = [...org].sort((a, b) => a.lan.localeCompare(b.lan, "sv") || a.namn.localeCompare(b.namn, "sv"));
  let prick;
  if (karta) {
    const yta = term.closest(".demo-yta"), svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "karta minikarta");
    svg.setAttribute("aria-hidden", "true");
    yta.append(svg);
    yta.classList.add("med-karta");
    prickar.remove();
    const ytor = ritaKarta(svg, karta, { lanGranser: false });
    prick = new Map(ordning.filter(o => ytor.has(o.kod)).map(o => [o, ytor.get(o.kod)]));
  } else {
    prick = new Map(ordning.map(o => {
      const i = document.createElement("i");
      i.title = `${o.namn}: ${etikett[o.epost]}`;
      prickar.append(i);
      return [o, i];
    }));
  }
  const fyll = (el, f) => { if (el) el.style[el instanceof SVGElement ? "fill" : "background"] = f; };

  let synlig = true;
  new IntersectionObserver(([e]) => { synlig = e.isIntersecting; }).observe(term);
  // Väntar ms millisekunder av synlig tid: står still när animationen är utanför skärmen.
  const vanta = ms => new Promise(klar => {
    if (lugn) return klar();
    let kvar = ms;
    (function tick() { if (synlig) kvar -= 40; kvar <= 0 ? klar() : setTimeout(tick, 40); })();
  });

  function rad(klass, text = "") {
    const r = document.createElement("span");
    r.className = klass;
    r.textContent = text;
    term.append(r, "\n");
    term.scrollTop = term.scrollHeight;
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
    ["T2", "Exchange Online", "domänen registrerad?"],
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
    const lev = { MS: "MS", G: "G", "MS+G": "MS+G", ja: "MS", svarar: "MS" }[varde];
    tagg.textContent = varde === "ja" ? "finns" : varde === "svarar" ? "svarar" : varde === "gateway/egen" ? "spamfilter/egen"
      : varde === "MS+G" ? "båda" : LEVERANTOR[varde] || "inget";
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
    // Bara leverantörens del av svaret visas; resten innehåller tenantnamnet.
    rad(s.dkim && s.dkim !== "annan" ? "svar traff" : "svar", s.dkim === "annan" ? "→ annan leverantör" : s.dkim ? "…." + s.dkim : "(inget svar)");
    satt("S7", o.signaler.S7);
    await vanta(900);

    await skriv(`curl -s -o /dev/null -w "%{http_code}" login.microsoftonline.com/${d}/…`);
    rad(s.entra === 200 ? "svar traff" : "svar", String(s.entra));
    satt("S5", s.entra === 200 ? "ja" : "-");
    await vanta(700);

    if (o.exo !== null && o.exo !== undefined) {
      await skriv(`curl -s "outlook.office365.com/autodiscover/autodiscover.json?Email=test@${d}"`);
      rad(o.exo ? "svar traff" : "svar", o.exo ? "→ outlook.office365.com" : "→ en annan server");
      satt("T2", o.exo ? "svarar" : "-");
      await vanta(900);
    }

    sig.querySelectorAll("li").forEach(x => x.classList.remove("aktiv"));
    utslag.replaceChildren(
      Object.assign(document.createElement("span"), { className: "tagg", textContent: etikett[o.epost], style: `background:${farg[o.epost]}` }),
      `${exempel.regel}.` + (o.epost === "G" && o.signaler.S7 === "MS" ? " DKIM pekar ändå på Microsoft: e-posten skickas troligen därifrån." : "")
        + (o.exo === true && o.epost !== "MS" ? ` Men domänen är registrerad i Microsofts Exchange Online (kontroll ${kontrollDatum}).` : "")
        + (o.exo === true && o.epost === "MS" ? ` Domänen är också registrerad i Exchange Online (kontroll ${kontrollDatum}).` : ""),
    );
    utslag.classList.add("syns");
    const p = prick.get(o);
    fyll(p, farg[o.epost]);
    p?.classList.add("ny");
    await vanta(2600);
    p?.classList.remove("ny");
  }

  async function fyllResten(gjorda) {
    namnEl.textContent = `… och samma regler för alla ${org.length}`;
    const kvar = ordning.filter(o => !gjorda.has(o));
    const steg = Math.max(1, Math.ceil(kvar.length / 60));
    for (let i = 0; i < kvar.length; i += steg) {
      for (const o of kvar.slice(i, i + steg)) fyll(prick.get(o), farg[o.epost]);
      await vanta(30);
    }
  }

  const slump = lista => lista[Math.floor(Math.random() * lista.length)];
  (async function spela() {
    for (;;) {
      prick.forEach(el => fyll(el, ""));
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
