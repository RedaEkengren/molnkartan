// "Så mäts en webbplats": spelar upp mätning 2 för riktiga organisationer ur data.json.
// Värdarna är de som sidan kontaktade i mätningen (webbmatning.py), nätet är
// uppslaget som gjordes då, och utslaget är klassningen från webb_klassa.py.

const WEBBEXEMPEL = [
  { passar: o => o.fore_samtycke?.klass === "US-nät före samtycke" && o.fore_samtycke.gaInsamling },
  { passar: o => o.fore_samtycke?.klass === "bara EU/EES-nät före samtycke" && o.fore_samtycke.varder.length >= 3 },
  { passar: o => o.fore_samtycke?.klass === "US-nät före samtycke" && !o.fore_samtycke.ga && o.fore_samtycke.us.length <= 3 },
  { passar: o => o.fore_samtycke?.klass === "ingen tredjepart" },
];
const NAT = { "US": ["Amerikanskt nät", "var(--g)"], "EU/EES": ["EU/EES-nät", "var(--inga)"], "annat": ["Annat nät", "var(--annat)"] };
const VISA_HOGST = 7;

function startaWebbDemo(org, { webbEtikett, webbFarg }) {
  const adress = document.getElementById("wAdress"), lista = document.getElementById("wVarder");
  const utslag = document.getElementById("wUtslag"), namn = document.getElementById("wNamn");
  const laddar = document.getElementById("wLaddar");
  const lugn = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let synlig = true;
  new IntersectionObserver(([e]) => { synlig = e.isIntersecting; }).observe(lista);
  // Väntar ms millisekunder av synlig tid: står still när animationen är utanför skärmen.
  const vanta = ms => new Promise(klar => {
    if (lugn) return klar();
    let kvar = ms;
    (function tick() { if (synlig) kvar -= 40; kvar <= 0 ? klar() : setTimeout(tick, 40); })();
  });
  const el = (t, e = {}, ...b) => { const x = Object.assign(document.createElement(t), e); x.append(...b); return x; };

  async function visa(o) {
    const f = o.fore_samtycke;
    lista.replaceChildren();
    utslag.classList.remove("syns");
    namn.textContent = `${o.namn} · ${o.lan || "myndighet"}`;
    adress.textContent = "";
    laddar.style.width = "0%";
    for (const tecken of (f.sida || "").replace(/^https:\/\//, "").replace(/\/$/, "")) {
      adress.textContent += tecken;
      await vanta(lugn ? 0 : 28);
    }
    laddar.style.width = "100%";
    await vanta(700);

    // Amerikanska nät först, så de syns även när listan kortas.
    const varder = [...f.varder].sort((a, b) => (a.nat === "US" ? 0 : 1) - (b.nat === "US" ? 0 : 1));
    if (!varder.length) lista.append(el("li", { className: "tom", textContent: "Inga anrop till någon tredjepart." }));
    for (const v of varder.slice(0, VISA_HOGST)) {
      const [text, farg] = NAT[v.nat] || ["Okänt nät", "var(--okand)"];
      const li = el("li", {}, el("code", { textContent: v.v }),
        el("span", {}, v.lev ? el("small", { textContent: v.lev + " " }) : "", el("span", { className: "tagg", textContent: text, style: `background:${farg}` })));
      lista.append(li);
      requestAnimationFrame(() => li.classList.add("in"));
      await vanta(450);
    }
    if (varder.length > VISA_HOGST) lista.append(el("li", { className: "tom", textContent: `… och ${varder.length - VISA_HOGST} till` }));
    await vanta(600);

    utslag.replaceChildren(
      el("span", { className: "tagg", textContent: webbEtikett[f.klass], style: `background:${webbFarg[f.klass]}` }),
      f.gaInsamling ? " Google Analytics anropas innan besökaren svarat." : f.ga ? " Google Tag Manager laddas innan besökaren svarat." :
        f.klass === "ingen tredjepart" ? " Allt hämtas från kommunens egen webbplats." :
          f.klass === "US-nät före samtycke" ? ` ${f.us.length} ${f.us.length === 1 ? "värd" : "värdar"} på amerikanskt nät innan besökaren svarat.` :
            " Inga amerikanska nät innan besökaren svarat.",
    );
    utslag.classList.add("syns");
    await vanta(3200);
  }

  const slump = l => l[Math.floor(Math.random() * l.length)];
  (async function spela() {
    for (;;) {
      for (const ex of WEBBEXEMPEL) {
        const kandidater = org.filter(ex.passar);
        if (kandidater.length) await visa(slump(kandidater));
      }
      if (lugn) return;
    }
  })();
}
