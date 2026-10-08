// Ljust/mörkt läge. Utan val följer sidan systemet; valet sparas i webbläsaren.
(function () {
  const rot = document.documentElement;
  try { const val = localStorage.getItem("tema"); if (val === "ljust" || val === "morkt") rot.dataset.tema = val; } catch (e) {}
  const morktNu = () => rot.dataset.tema ? rot.dataset.tema === "morkt" : matchMedia("(prefers-color-scheme: dark)").matches;
  document.addEventListener("DOMContentLoaded", () => {
    const knapp = document.querySelector(".temaknapp");
    if (!knapp) return;
    const etikett = () => knapp.setAttribute("aria-label", morktNu() ? "Byt till ljust läge" : "Byt till mörkt läge");
    etikett();
    knapp.addEventListener("click", () => {
      rot.dataset.tema = morktNu() ? "ljust" : "morkt";
      try { localStorage.setItem("tema", rot.dataset.tema); } catch (e) {}
      etikett();
    });
  });
})();
