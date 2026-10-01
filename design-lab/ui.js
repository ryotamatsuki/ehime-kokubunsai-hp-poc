/* D2 enhancement only. Core content and links are present in HTML. */
(() => {
  "use strict";
  const query = () => new URLSearchParams(window.__INITIAL_QUERY__ || window.location.search);
  const getDirection = () => query().get("direction") === "poster" || document.documentElement.dataset.direction === "poster" ? "poster" : "editorial";
  const direction = getDirection();
  document.documentElement.dataset.direction = direction;

  const toggle = document.querySelector("[data-menu-toggle]");
  const nav = document.querySelector("[data-main-nav]");
  if (toggle && nav) {
    const media = window.matchMedia("(max-width: 1059px)");
    let open = false;
    const refresh = () => {
      toggle.hidden = !media.matches;
      nav.hidden = media.matches && !open;
      toggle.setAttribute("aria-expanded", String(media.matches && open));
      toggle.querySelector("[data-menu-label]").textContent = open ? "閉じる" : "メニュー";
    };
    toggle.addEventListener("click", () => { open = !open; refresh(); });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && open && media.matches) {
        open = false; refresh(); toggle.focus();
      }
    });
    nav.addEventListener("click", event => {
      if (event.target.closest("a") && media.matches) { open = false; refresh(); }
    });
    media.addEventListener("change", () => { open = false; refresh(); });
    refresh();
  }

  if (direction === "poster") {
    document.querySelectorAll("a[href]").forEach(anchor => {
      const href = anchor.getAttribute("href");
      if (!href || href.startsWith("#")) return;
      const url = new URL(href, "https://design-lab.invalid/");
      const file = url.pathname.split("/").pop();
      if (["event-search.html", "event-detail.html", "documents.html", "components.html"].includes(file)) {
        url.searchParams.set("direction", "poster");
        anchor.setAttribute("href", file + url.search + url.hash);
      } else if (file === "home-a.html") {
        anchor.setAttribute("href", "home-b.html" + url.search + url.hash);
      }
    });
  }

  const form = document.querySelector("[data-event-filters]");
  if (form) {
    const controls = ["q", "city", "genre", "support"].map(name => document.getElementById("filter-" + name));
    const cards = Array.from(document.querySelectorAll("[data-event-card]"));
    const count = document.querySelector("[data-result-count]");
    const empty = document.querySelector("[data-empty]");
    const results = document.querySelector("[data-results]");
    const update = (persist = true) => {
      const [keyword, city, genre, support] = controls.map(control => control.value.trim());
      const terms = keyword.toLocaleLowerCase("ja").split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(card => {
        const haystack = card.dataset.search.toLocaleLowerCase("ja");
        const match = terms.every(term => haystack.includes(term)) &&
          (!city || card.dataset.city === city) &&
          (!genre || card.dataset.genre === genre) &&
          (!support || (card.dataset.support || "").split("|").includes(support));
        card.hidden = !match;
        if (match) visible++;
      });
      count.textContent = String(visible);
      empty.hidden = visible !== 0;
      results.hidden = visible === 0;
      if (persist) {
        const params = new URLSearchParams();
        controls.forEach(control => { if (control.value.trim()) params.set(control.name, control.value.trim()); });
        if (direction === "poster") params.set("direction", "poster");
        const qs = params.toString() ? "?" + params.toString() : "";
        if (window.__INITIAL_QUERY__ !== undefined) window.__INITIAL_QUERY__ = qs;
        else window.history.replaceState(null, "", window.location.pathname + qs);
      }
    };
    const restore = () => {
      const params = query();
      controls.forEach(control => {
        const value = params.get(control.name) || "";
        if (control.tagName === "SELECT") {
          control.value = Array.from(control.options).some(option => option.value === value) ? value : "";
        } else control.value = value;
      });
      update(false);
    };
    form.addEventListener("submit", event => { event.preventDefault(); update(); });
    controls.forEach(control => control.addEventListener("change", () => update()));
    controls[0].addEventListener("input", () => update());
    document.querySelectorAll("[data-reset-filters]").forEach(button => {
      button.addEventListener("click", () => {
        controls.forEach(control => { control.value = ""; });
        update();
        controls[0].focus();
      });
    });
    window.addEventListener("popstate", restore);
    restore();
    document.querySelectorAll("[data-js-only]").forEach(element => { element.hidden = false; });
  }

  const detail = document.querySelector("[data-detail-title]");
  if (detail) {
    const events = window.EHIME_LAB_EVENTS || [];
    const params = query();
    const event = events.find(item => item.id === params.get("id")) || events.find(item => item.id === "craft") || events[0];
    if (event) {
      document.querySelectorAll("[data-detail-title]").forEach(node => { node.textContent = event.title; });
      document.querySelector("[data-detail-description]").textContent = event.description;
      document.querySelector("[data-detail-city]").textContent = event.city + "（サンプル）";
      document.querySelector("[data-detail-genre]").textContent = event.genre;
      const image = document.querySelector("[data-detail-photo]");
      image.src = "assets/photos/" + event.image + "-960.webp";
      image.srcset = [480, 960, 1440].map(w => "assets/photos/" + event.image + "-" + w + ".webp " + w + "w").join(", ");
      image.alt = event.alt;
      document.title = event.title + " | 愛媛大会（仮）";
      const supportList = document.querySelector("[data-detail-support]");
      supportList.replaceChildren(...event.support.map(label => {
        const item = document.createElement("li");
        item.className = "support-item";
        const title = document.createElement("strong");
        title.textContent = label + "（表示例）";
        const note = document.createElement("span");
        note.textContent = "実際の対応は正式決定後に案内します。";
        item.append(title, note);
        return item;
      }));
    }
  }
})();
