// Sverigekartan: kommunerna färgade efter vald mätning. Gränser: SCB, Digitala gränser (CC0).
// Regionerna har ingen egen yta och syns bara i tabellen.

const SVG = "http://www.w3.org/2000/svg";

function ritaKarta(svg, karta, { lanGranser = true } = {}) {
  svg.setAttribute("viewBox", karta.viewBox);
  const ytor = new Map();
  const g = document.createElementNS(SVG, "g");
  for (const [kod, k] of Object.entries(karta.kommuner)) {
    const p = document.createElementNS(SVG, "path");
    p.setAttribute("d", k.d);
    p.dataset.kod = kod;
    g.append(p);
    ytor.set(kod, p);
  }
  svg.append(g);
  if (lanGranser) {
    const lg = document.createElementNS(SVG, "g");
    lg.setAttribute("class", "langrans");
    for (const l of Object.values(karta.lan)) {
      const p = document.createElementNS(SVG, "path");
      p.setAttribute("d", l.d);
      lg.append(p);
    }
    svg.append(lg);
  }
  return ytor;
}

function startaKarta(org, karta, vyer) {
  const svg = document.getElementById("karta"), info = document.getElementById("kartInfo");
  const flikar = document.getElementById("kartFlikar"), legend = document.getElementById("kartLegend");
  const ytor = ritaKarta(svg, karta);
  const perKod = new Map(org.filter(o => o.kod).map(o => [o.kod, o]));
  let vy = vyer[0];

  function farga() {
    for (const [kod, p] of ytor) {
      const o = perKod.get(kod), [etikett, farg] = o ? vy.varde(o) : ["Saknas", "var(--linje)"];
      p.style.fill = farg;
      p.dataset.etikett = etikett;
    }
    legend.replaceChildren(...vy.legend.map(([namn, farg]) => {
      const antal = [...perKod.values()].filter(o => vy.varde(o)[0] === namn).length;
      const s = document.createElement("span");
      s.innerHTML = `<i style="background:${farg}"></i>`;
      s.append(`${namn} (${antal})`);
      return s;
    }));
  }
  function visaInfo(kod) {
    const o = perKod.get(kod);
    if (!o) return;
    ytor.forEach(p => p.classList.toggle("vald", p.dataset.kod === kod));
    info.replaceChildren();
    const rubrik = document.createElement("b");
    rubrik.textContent = `${o.namn} · ${o.lan}`;
    info.append(rubrik);
    for (const v of vyer) {
      const rad = document.createElement("div"), [etikett, farg] = v.varde(o);
      rad.innerHTML = `<span></span><span class="tagg"></span>`;
      rad.children[0].textContent = v.namn;
      rad.children[1].textContent = etikett;
      rad.children[1].style.background = farg;
      info.append(rad);
    }
    const lank = document.createElement("a");
    lank.href = "#tabell";
    lank.textContent = "Visa i tabellen";
    lank.onclick = () => { const sok = document.getElementById("sok"); sok.value = o.namn; sok.dispatchEvent(new Event("input")); };
    info.append(lank);
  }

  for (const v of vyer) {
    const knapp = document.createElement("button");
    knapp.type = "button";
    knapp.textContent = v.namn;
    knapp.setAttribute("aria-pressed", v === vy);
    knapp.onclick = () => {
      vy = v;
      flikar.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === knapp));
      farga();
    };
    flikar.append(knapp);
  }
  svg.addEventListener("mouseover", e => e.target.dataset.kod && visaInfo(e.target.dataset.kod));
  svg.addEventListener("click", e => e.target.dataset.kod && visaInfo(e.target.dataset.kod));
  farga();
  visaInfo(perKod.has("0180") ? "0180" : [...perKod.keys()][0]);
}
