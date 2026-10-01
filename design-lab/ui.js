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

  document.querySelectorAll("[data-js-only]").forEach(node => { node.hidden = false; });
  const persistChoice = (key, value) => {
    const params = query();
    params.set(key, value);
    if (direction === "poster") params.set("direction", "poster");
    const qs = "?" + params.toString();
    if (window.__INITIAL_QUERY__ !== undefined) window.__INITIAL_QUERY__ = qs;
    else window.history.replaceState(null, "", window.location.pathname + qs);
  };
  const updatePhoto = (node, name, alt) => {
    node.src = "assets/photos/" + name + "-960.webp";
    node.srcset = [480, 960, 1440].map(width => "assets/photos/" + name + "-" + width + ".webp " + width + "w").join(", ");
    node.alt = alt;
  };
  const cultureButtons = [...document.querySelectorAll("[data-culture]")];
  if (cultureButtons.length) {
    const cultures = {
      craft: {number:"01", genre:"工芸", title:"手を動かす。\n会話が生まれる。", description:"土に触れ、自分の手で形をつくる。工芸を入り口に、人と土地の物語に出会います。"},
      stage: {number:"02", genre:"舞台", title:"受け継いだ音が、\nいま、響きあう。", description:"地域の芸能と、新しい表現。舞台を囲む時間から、愛媛の文化に出会います。"},
      literature: {number:"03", genre:"文学", title:"まちを歩く。\n自分の言葉に出会う。", description:"いつもの景色を、いつもと違う言葉で。文学とまち歩きを通して、土地の物語を見つけます。"},
      food: {number:"04", genre:"食文化", title:"ひと皿の向こうに、\n土地の物語。", description:"食べる、話す、分かち合う。土地の味わいと、それを伝える人に出会います。"}
    };
    const activate = (key, announce = false, persist = true) => {
      if (!cultures[key]) key = "craft";
      const culture = cultures[key];
      const event = (window.EHIME_LAB_EVENTS || []).find(item => item.id === key);
      if (!event) return;
      cultureButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.culture === key)));
      updatePhoto(document.querySelector("[data-culture-photo]"), event.image, event.alt);
      document.querySelector("[data-culture-label]").textContent = culture.number + " / " + culture.genre;
      document.querySelector("[data-culture-title]").textContent = culture.title;
      document.querySelector("[data-culture-description]").textContent = culture.description;
      const search = document.querySelector("[data-culture-search]");
      search.setAttribute("href", "event-search.html?" + new URLSearchParams({genre:culture.genre}));
      search.firstChild.textContent = culture.genre + "の催しを探す ";
      document.querySelector("[data-culture-detail]").setAttribute("href", "event-detail.html?id=" + key);
      if (announce) document.querySelector("[data-culture-announcement]").textContent = culture.genre + "を選択しました。写真と案内を更新しました。";
      if (persist) persistChoice("culture", key);
    };
    cultureButtons.forEach(button => button.addEventListener("click", () => activate(button.dataset.culture, true)));
    const restore = () => activate(query().get("culture") || "craft", false, false);
    window.addEventListener("popstate", restore);
    restore();
  }
  const intentButtons = [...document.querySelectorAll("[data-intent]")];
  if (intentButtons.length) {
    const intents = {
      watch: {kicker:"01 / DISCOVER", word:"観る", title:"その「観たい」が、\n旅のはじまり。", description:"舞台、工芸、文学、食文化。気になる表現から、あなたの体験を探してください。", image:"event-stage-lanterns", alt:"海辺の屋外ステージと、文化公演を楽しむ観客のイメージ", label:"イベントを探す", href:"event-search.html?direction=poster"},
      make: {kicker:"02 / CREATE", word:"つくる", title:"あなたの表現を、\nここに持ちよろう。", description:"出演・出展、ボランティア、協賛。あなたらしい関わり方へ。募集内容と時期は、正式決定後にご案内します。", image:"family-culture-workshop", alt:"多世代が文化のワークショップを楽しむイメージ", label:"参加・募集の案内", href:"documents.html?direction=poster#participation"},
      together: {kicker:"03 / TOGETHER", word:"ともに", title:"楽しみたい気持ちに、\n入口をひらく。", description:"障害のある人もない人も。会場や情報のバリアフリー、参加に必要な支援を確認できます。実際の対応内容は正式決定後に掲載します。", image:"inclusive-art-gallery", alt:"作品を囲み、芸術を楽しむ人々のイメージ", label:"参加の支援を確認", href:"event-detail.html?direction=poster#support"}
    };
    const activate = (key, announce = false, persist = true) => {
      if (!intents[key]) key = "watch";
      const intent = intents[key];
      intentButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.intent === key)));
      document.querySelector("[data-intent-panel]").dataset.intentPanel = key;
      ["kicker", "word", "title", "description"].forEach(name => { document.querySelector("[data-intent-" + name + "]").textContent = intent[name]; });
      updatePhoto(document.querySelector("[data-intent-photo]"), intent.image, intent.alt);
      const link = document.querySelector("[data-intent-link]");
      link.setAttribute("href", intent.href);
      link.firstChild.textContent = intent.label + " ";
      if (announce) document.querySelector("[data-intent-announcement]").textContent = intent.word + "を選択しました。写真と案内を更新しました。";
      if (persist) persistChoice("intent", key);
    };
    intentButtons.forEach(button => button.addEventListener("click", () => activate(button.dataset.intent, true)));
    const restore = () => activate(query().get("intent") || "watch", false, false);
    window.addEventListener("popstate", restore);
    restore();
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
