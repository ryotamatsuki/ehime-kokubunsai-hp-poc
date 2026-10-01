/* A single progressively enhanced experience. All cultural stories have static routes. */
(() => {
  'use strict';
  const data = window.EHIME_V2_DATA;
  if (!data || !Array.isArray(data.events)) return;
  const events = new Map(data.events.map(event => [event.id, event]));
  const routes = window.EHIME_V2_ROUTES || {};
  const storageKey = 'ehime-v2-culture-notes';
  const initialQuery = () => new URLSearchParams(window.__POC_QUERY__ !== undefined ? window.__POC_QUERY__ : location.search);
  const sanitize = value => [...new Set(Array.isArray(value) ? value.filter(id => events.has(id)) : [])].slice(0, events.size);
  let storageAvailable = true;
  let saved;
  try {
    saved = sanitize(JSON.parse(localStorage.getItem(storageKey) || '[]'));
  } catch (_) { storageAvailable = false; saved = []; }
  if (Array.isArray(window.__POC_NOTEBOOK__)) saved = sanitize(window.__POC_NOTEBOOK__);
  const initial = initialQuery();
  if (initial.has('saved')) saved = sanitize(initial.get('saved').split(','));
  const status = document.querySelector('[data-global-status]');
  const announce = message => { if (status) status.textContent = message; };
  const setQuery = params => {
    const next = params.toString() ? '?' + params.toString() : '';
    if (window.__POC_QUERY__ !== undefined) window.__POC_QUERY__ = next;
    else history.replaceState(null, '', location.pathname + next + location.hash);
  };
  const persist = () => {
    try { localStorage.setItem(storageKey, JSON.stringify(saved)); }
    catch (_) { storageAvailable = false; }
    const params = initialQuery();
    params.set('saved', saved.join(','));
    setQuery(params);
    if (window.__POC_OFFLINE__) window.parent.postMessage({type:'ehime-v2-notebook', ids:saved}, '*');
  };
  const preserveLinks = () => {
    document.querySelectorAll('a[href]').forEach(anchor => {
      const href = anchor.getAttribute('href');
      if (!href || href.startsWith('#') || /^(https?:|mailto:|tel:|data:|blob:)/.test(href)) return;
      const url = new URL(href, 'https://poc.invalid/');
      if (!url.pathname.endsWith('.html')) return;
      const [plain] = href.split(/[?#]/);
      url.searchParams.set('saved', saved.join(','));
      anchor.setAttribute('href', plain + '?' + url.searchParams.toString() + url.hash);
    });
  };
  const storageNote = () => {
    const element = document.querySelector('[data-storage-status]');
    if (element) element.textContent = storageAvailable ? '' : 'この環境ではブラウザーへの保存を利用できません。ページ内の移動では選択を引き継ぎます。文化帖は「持ちかえる」から保存できます。';
  };
  const titleFor = id => events.get(id)?.title || '';
  const cultureThemes = () => data.cultures.filter(culture => saved.some(id => events.get(id).culture === culture.id));
  const culturalMark = () => {
    const active = new Set(cultureThemes().map(culture => culture.id));
    const symbols = {
      craft:'<circle cx="50" cy="48" r="25" fill="none" stroke="#183c9e" stroke-width="5"/><path d="M26 42q24-24 48 0" fill="none" stroke="#183c9e" stroke-width="7"/>',
      literature:[5,7,5].map((n,col) => Array.from({length:n},(_,i) => '<circle cx="'+(35+col*15)+'" cy="'+(18+i*9)+'" r="2.5" fill="#183c9e"/>').join('')).join(''),
      food:'<path d="M23 42q27-32 54 0-27 32-54 0z" fill="#183c9e"/><path d="M17 68q16-13 32 0t32 0M17 78q16-13 32 0t32 0" fill="none" stroke="#183c9e" stroke-width="3"/>',
      art:'<path d="M23 80V33a18 18 0 0 1 36 0v47z" fill="#183c9e"/><path d="M59 35h20v45H59z" fill="#b33227"/>',
    };
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 106"><rect width="400" height="106" fill="#f5f2ea"/>' +
      data.cultures.map((culture,index) => '<g transform="translate('+(index*100)+' 0)">' + (active.has(culture.id) ? symbols[culture.id] : '<circle cx="50" cy="49" r="23" fill="none" stroke="#b4b8bd"/>') + '<text x="50" y="98" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#183c9e">'+culture.number+'</text></g>').join('') + '</svg>';
  };
  const renderNotebook = focusIndex => {
    const list = document.querySelector('[data-notebook-list]');
    if (!list) return;
    list.replaceChildren();
    saved.forEach(id => {
      const event = events.get(id);
      const article = document.createElement('article'); article.className = 'notebook-item';
      const copy = document.createElement('div');
      const label = document.createElement('span'); label.className = 'status' + (event.kind === 'verified' ? ' status--verified' : '');
      label.textContent = event.kind === 'verified' ? '確認済み / ' + event.status : '架空の掲載例';
      const h3 = document.createElement('h3');
      const anchor = document.createElement('a'); anchor.href = routes[event.page] || event.page; anchor.textContent = event.title;
      h3.append(anchor);
      const meta = document.createElement('p'); meta.textContent = event.city + ' / ' + event.genre + ' / ' + event.date;
      const note = document.createElement('p'); note.textContent = event.kind === 'sample' ? 'この催しへの申込みはできません。' : event.booking;
      copy.append(label, h3, meta, note);
      const remove = document.createElement('button'); remove.className = 'remove-note'; remove.type = 'button';
      remove.textContent = '削除'; remove.dataset.remove = id; remove.setAttribute('aria-label', event.title + 'を文化帖から削除');
      remove.addEventListener('click', () => {
        const index = saved.indexOf(id); saved = saved.filter(item => item !== id); persist(); update(index);
        announce(event.title + 'を文化帖から削除しました。');
      });
      article.append(copy, remove); list.append(article);
    });
    const empty = document.querySelector('[data-notebook-empty]'); if (empty) empty.hidden = saved.length !== 0;
    const counter = document.querySelector('[data-notebook-count]'); if (counter) counter.textContent = String(saved.length);
    const pattern = document.querySelector('[data-notebook-pattern]'); if (pattern) pattern.innerHTML = culturalMark();
    const themes = document.querySelector('[data-notebook-themes]');
    if (themes) themes.textContent = saved.length ? '文化のしるし：' + cultureThemes().map(culture => culture.word).join('、') : '気になる文化を集めると、表紙のしるしが変わります。';
    document.querySelectorAll('[data-export],[data-share]').forEach(button => { button.disabled = saved.length === 0; });
    document.querySelector('[data-notebook-status]').textContent = saved.length + '件の催しを文化帖に保存しています。';
    if (focusIndex !== undefined) {
      const buttons = list.querySelectorAll('[data-remove]');
      if (buttons.length) buttons[Math.min(focusIndex, buttons.length - 1)].focus();
      else empty.querySelector('a')?.focus();
    }
  };
  const update = focusIndex => {
    document.querySelectorAll('[data-book-count]').forEach(el => {
      el.textContent = String(saved.length);
      el.closest('a')?.setAttribute('aria-label', '文化帖。' + saved.length + '件の催しを保存しています。');
    });
    document.querySelectorAll('[data-save]').forEach(button => {
      const on = saved.includes(button.dataset.save);
      button.hidden = false; button.setAttribute('aria-pressed', String(on));
      button.querySelector('[data-save-label]').textContent = on ? '文化帖から削除' : '文化帖に追加';
      button.setAttribute('aria-label', titleFor(button.dataset.save) + (on ? 'を文化帖から削除' : 'を文化帖に追加'));
    });
    renderNotebook(focusIndex); preserveLinks(); storageNote();
  };
  document.querySelectorAll('[data-save]').forEach(button => {
    button.addEventListener('click', () => {
      const id = button.dataset.save; if (!events.has(id)) return;
      const on = saved.includes(id);
      saved = on ? saved.filter(item => item !== id) : [...saved, id];
      persist(); update();
      announce(titleFor(id) + (on ? 'を文化帖から削除しました。' : 'を文化帖に追加しました。') + saved.length + '件保存しています。');
      if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        button.classList.remove('is-updated');
        window.requestAnimationFrame(() => button.classList.add('is-updated'));
      }
    });
  });
  document.querySelectorAll('[data-js-only]').forEach(el => { el.hidden = false; });
  if (window.__POC_OFFLINE__) document.querySelector('[data-share]')?.setAttribute('hidden','');
  const menu = document.querySelector('[data-menu]');
  const navigation = document.querySelector('[data-navigation]');
  if (menu && navigation) {
    const compact = window.matchMedia('(max-width: 700px)');
    const close = returnFocus => {
      menu.setAttribute('aria-expanded','false'); navigation.hidden = compact.matches;
      menu.querySelector('[data-menu-label]').textContent = 'メニュー';
      if (returnFocus) menu.focus();
    };
    const resize = () => { menu.hidden = !compact.matches; close(false); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded',String(open)); navigation.hidden = !open;
      menu.querySelector('[data-menu-label]').textContent = open ? '閉じる' : 'メニュー';
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') close(true);
    });
    navigation.addEventListener('click', event => { if (event.target.closest('a') && compact.matches) close(false); });
    if (compact.addEventListener) compact.addEventListener('change',resize);
    else compact.addListener(resize);
    resize();
  }
  const form = document.querySelector('[data-filters]');
  let restoreFilters;
  if (form) {
    const controls = ['q','city','genre','support','kind'].map(name => document.getElementById('filter-' + name));
    const cards = [...document.querySelectorAll('[data-event-card]')];
    const filter = write => {
      const [text, city, genre, support, kind] = controls.map(control => control.value.trim());
      const terms = text.toLocaleLowerCase('ja').split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(card => {
        const match = terms.every(term => card.dataset.search.toLocaleLowerCase('ja').includes(term)) &&
          (!city || card.dataset.city === city) && (!genre || card.dataset.genre === genre) &&
          (!support || card.dataset.support.split('|').includes(support)) && (!kind || card.dataset.kind === kind);
        card.hidden = !match; if (match) visible++;
      });
      document.querySelector('[data-count]').textContent = String(visible);
      document.querySelector('[data-result-status]').textContent = visible + '件の催しが見つかりました。';
      document.querySelector('[data-empty]').hidden = visible !== 0;
      document.querySelector('[data-results]').hidden = visible === 0;
      if (write) {
        const params = initialQuery();
        controls.forEach(control => { params.delete(control.name); if (control.value.trim()) params.set(control.name, control.value.trim()); });
        setQuery(params);
      }
      preserveLinks();
    };
    restoreFilters = () => {
      const params = initialQuery();
      controls.forEach(control => {
        const value = params.get(control.name) || '';
        control.value = control.tagName === 'SELECT' ? ([...control.options].some(option => option.value === value) ? value : '') : value;
      });
      filter(false);
    };
    form.addEventListener('submit', event => { event.preventDefault(); filter(true); });
    controls[0].addEventListener('input', () => filter(true));
    controls.slice(1).forEach(control => control.addEventListener('change', () => filter(true)));
    document.querySelectorAll('[data-reset]').forEach(button => button.addEventListener('click', () => {
      controls.forEach(control => { control.value = ''; }); filter(true); controls[0].focus();
    }));
    restoreFilters();
  }
  const xml = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
  const wrap = (text, size) => { const characters = [...text]; const lines = []; while (characters.length) lines.push(characters.splice(0,size).join('')); return lines; };
  const makeExport = () => {
    const height = 365 + saved.length * 175;
    const mark = culturalMark().replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 106">','<svg x="800" y="58" width="330" height="88" viewBox="0 0 400 106">');
    const pieces = [`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="${height}" viewBox="0 0 1200 ${height}"><rect width="1200" height="${height}" fill="#f5f2ea"/>${mark}<g font-family="sans-serif" fill="#151d36"><text x="64" y="65" font-size="20" letter-spacing="3">EHIME / MY CULTURE NOTES</text><text x="64" y="144" fill="#183c9e" font-size="56" font-weight="700">わたしの、文化帖。</text><text x="64" y="196" font-size="22">愛顔えひめの文化祭2028 / 本大会 2028.10.22 — 12.03</text><text x="64" y="235" font-size="18">文化帖は予約ではありません。掲載例は架空の催しです。開催情報は公式案内をご確認ください。</text><path d="M64 265h1072" stroke="#183c9e"/>`];
    saved.forEach((id, index) => {
      const event = events.get(id); const y = 307 + index * 175;
      const kind = event.kind === 'verified' ? '確認済み / ' + event.status : '架空の掲載例';
      pieces.push(`<text x="64" y="${y}" fill="#183c9e" font-size="16">${xml(String(index + 1).padStart(2,'0') + ' / ' + kind)}</text>`);
      wrap(event.title,32).forEach((line,lineIndex) => pieces.push(`<text x="64" y="${y+43+lineIndex*36}" font-size="29" font-weight="700">${xml(line)}</text>`));
      pieces.push(`<text x="64" y="${y+112}" font-size="18">${xml(event.city + ' / ' + event.genre + ' / ' + event.date)}</text><path d="M64 ${y+141}h1072" stroke="#b4b8bd"/>`);
    });
    pieces.push(`<text x="64" y="${height-30}" font-size="15">DESIGN PoC / 確認日 2026.10.01 / 文化帖の内容はお使いのブラウザー内で生成しました。</text></g></svg>`);
    return pieces.join('');
  };
  document.querySelector('[data-export]')?.addEventListener('click', () => {
    if (!saved.length) return;
    const blob = new Blob([makeExport()],{type:'image/svg+xml;charset=utf-8'});
    const url = URL.createObjectURL(blob); const anchor = document.createElement('a');
    anchor.href = url; anchor.download = 'ehime-culture-notes.svg'; document.body.append(anchor); anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url),1000); announce('文化帖をSVGファイルで持ちかえられます。');
  });
  document.querySelector('[data-share]')?.addEventListener('click', async () => {
    if (!saved.length || window.__POC_OFFLINE__) return;
    const url = new URL(location.href); url.search = ''; url.hash = ''; url.searchParams.set('saved',saved.join(','));
    const fallback = document.querySelector('[data-share-fallback]');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(url.href); fallback.hidden = true; announce('文化帖のリンクをコピーしました。');
    } catch (_) {
      fallback.hidden = false; const input = document.getElementById('share-url'); input.value = url.href; input.focus(); input.select();
      announce('リンクを選択してコピーしてください。');
    }
  });
  window.addEventListener('popstate', () => {
    const params = initialQuery();
    if (params.has('saved')) { saved = sanitize(params.get('saved').split(',')); persist(); }
    update(); restoreFilters?.();
  });
  persist(); update();
})();
