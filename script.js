(function () {
  const root = document.documentElement.dataset.root || "";

  const header = document.querySelector("[data-header]");
  const nav = document.querySelector("[data-nav]");
  const navToggle = document.querySelector("[data-nav-toggle]");

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  if (header) {
    const updateHeader = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
  }

  document.querySelectorAll("[data-site-search]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const input = form.querySelector("input[name='q']");
      const query = input ? input.value.trim() : "";
      const params = query ? "?q=" + encodeURIComponent(query) : "";
      window.location.href = root + "common/search.html" + params;
    });
  });

  const countdown = document.querySelector("[data-countdown]");
  if (countdown) {
    const target = new Date(countdown.dataset.countdown + "T00:00:00+09:00");
    const out = countdown.querySelector("[data-countdown-days]");
    const diff = target.getTime() - Date.now();
    const days = Math.max(0, Math.ceil(diff / 86400000));
    if (out) out.textContent = String(days);
  }

  document.querySelectorAll("[data-demo-form]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const status = form.querySelector("[data-form-status]");
      if (status) {
        status.textContent = "仮フォームのため送信は行われません。入力項目と確認導線のイメージです。";
      }
    });
  });

  document.querySelectorAll("[data-filter-list]").forEach((panel) => {
    const keyword = panel.querySelector("[data-filter-input]");
    const city = panel.querySelector("[data-filter-city]");
    const genre = panel.querySelector("[data-filter-genre]");
    const cards = Array.from(panel.querySelectorAll("[data-event-card]"));
    const empty = panel.querySelector("[data-filter-empty]");

    const applyFilter = () => {
      const q = keyword ? keyword.value.trim().toLowerCase() : "";
      const selectedCity = city ? city.value : "";
      const selectedGenre = genre ? genre.value : "";
      let count = 0;

      cards.forEach((card) => {
        const text = (card.dataset.text || "").toLowerCase();
        const matchText = !q || text.includes(q);
        const matchCity = !selectedCity || card.dataset.city === selectedCity;
        const matchGenre = !selectedGenre || card.dataset.genre === selectedGenre;
        const show = matchText && matchCity && matchGenre;
        card.hidden = !show;
        if (show) count += 1;
      });

      if (empty) empty.hidden = count !== 0;
    };

    [keyword, city, genre].forEach((control) => {
      if (control) control.addEventListener("input", applyFilter);
    });
  });

  const searchPage = document.querySelector("[data-search-page]");
  if (searchPage) {
    const input = searchPage.querySelector("[data-search-input]");
    const results = searchPage.querySelector("[data-search-results]");
    const params = new URLSearchParams(window.location.search);
    const initial = params.get("q") || "";
    if (input) input.value = initial;

    const render = () => {
      const query = input ? input.value.trim().toLowerCase() : "";
      const index = Array.isArray(window.SITE_SEARCH_INDEX) ? window.SITE_SEARCH_INDEX : [];
      const matches = index
        .filter((item) => {
          if (!query) return true;
          const haystack = [item.title, item.group, item.summary, (item.tags || []).join(" ")].join(" ").toLowerCase();
          return haystack.includes(query);
        })
        .slice(0, query ? 40 : 12);

      if (!results) return;
      if (!matches.length) {
        results.innerHTML = '<p class="search-result">該当するページはありません。別のキーワードで検索してください。</p>';
        return;
      }

      results.innerHTML = matches
        .map((item) => {
          const url = root + item.url;
          return [
            '<article class="search-result">',
            '<h3><a href="' + escapeAttr(url) + '">' + escapeHtml(item.title) + "</a></h3>",
            "<p>" + escapeHtml(item.summary) + "</p>",
            "<small>" + escapeHtml(item.group) + "</small>",
            "</article>",
          ].join("");
        })
        .join("");
    };

    if (input) input.addEventListener("input", render);
    render();
  }

  const accessTools = document.querySelector("[data-access-tools]");
  if (accessTools) {
    const fontButton = accessTools.querySelector("[data-font-plus]");
    const contrastButton = accessTools.querySelector("[data-contrast]");

    if (fontButton) {
      fontButton.addEventListener("click", () => {
        document.body.classList.toggle("large-text");
      });
    }

    if (contrastButton) {
      contrastButton.addEventListener("click", () => {
        document.body.classList.toggle("high-contrast");
      });
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function escapeAttr(value) {
    return escapeHtml(value);
  }
})();