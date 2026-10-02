/* Local PoC controls for retained information. No form content is transmitted. */
(() => {
  'use strict';
  const routes=window.EHIME_V2_ROUTES||{};
  const revealReading=id=>{
    const node=document.getElementById(id);if(!node)return;
    for(let parent=node.parentElement;parent;parent=parent.parentElement){if(parent.tagName==='DETAILS')parent.open=true;}
  };
  document.querySelectorAll('[data-open-reading]').forEach(anchor=>anchor.addEventListener('click',()=>revealReading(anchor.hash.slice(1))));
  addEventListener('hashchange',()=>revealReading(decodeURIComponent(location.hash.slice(1))));
  if(location.hash)revealReading(decodeURIComponent(location.hash.slice(1)));
  document.querySelectorAll('[data-local-demo-form]').forEach(form=>{
    form.querySelectorAll('[data-local-demo-submit]').forEach(button=>button.disabled=false);
    form.addEventListener('submit',event=>{
      event.preventDefault();
      const status=form.querySelector('[data-form-status]')||form.appendChild(document.createElement('p'));
      status.setAttribute('role','status');status.textContent='仮フォームのため送信は行われません。入力項目と確認導線の表示例です。';
    });
  });
  document.querySelectorAll('[data-legacy-filter]').forEach(panel=>{
    const controls=['[data-filter-input]','[data-filter-city]','[data-filter-genre]'].map(q=>panel.querySelector(q));
    const cards=[...panel.querySelectorAll('[data-legacy-event-card]')];
    const apply=()=>{
      const [q,city,genre]=controls.map(n=>n?.value.trim()||'');let count=0;
      cards.forEach(card=>{
        const match=(!q||card.textContent.toLocaleLowerCase('ja').includes(q.toLocaleLowerCase('ja')))&&(!city||card.dataset.city===city)&&(!genre||card.dataset.genre===genre);
        card.hidden=!match;if(match)count++;
      });
      const empty=panel.querySelector('[data-filter-empty]');if(empty)empty.hidden=count!==0;
    };
    controls.forEach(control=>control?.addEventListener('input',apply));apply();
  });
  const search=document.querySelector('[data-search-page]');
  if(search){
    const input=search.querySelector('[data-search-input]'),list=search.querySelector('[data-search-results]');
    const index=window.EHIME_V2_SITE_INDEX||[];
    if(input)input.value=new URLSearchParams(window.__POC_QUERY__??location.search).get('q')||'';
    const render=()=>{
      const words=(input?.value||'').trim().toLocaleLowerCase('ja').split(/\s+/).filter(Boolean);
      const rows=index.filter(row=>words.every(word=>(row.title+' '+row.group+' '+row.text).toLocaleLowerCase('ja').includes(word)));
      if(!list)return;list.replaceChildren();
      const count=document.createElement('p');count.className='site-result-count';count.setAttribute('role','status');count.textContent=rows.length+'件の案内';list.append(count);
      rows.forEach(row=>{
        const article=document.createElement('article');article.className='search-result';const h3=document.createElement('h3');
        const anchor=document.createElement('a');anchor.href=routes[row.page]||row.page;anchor.textContent=row.title;h3.append(anchor);
        const label=document.createElement('p');label.textContent=row.group;article.append(h3,label);list.append(article);
      });
      if(!rows.length){const p=document.createElement('p');p.textContent='該当する案内はありません。別のことばで検索してください。';list.append(p);}
    };
    input?.addEventListener('input',render);render();
  }
  document.querySelector('[data-font-plus]')?.addEventListener('click',event=>{
    const enabled=document.body.classList.toggle('large-text');event.currentTarget.setAttribute('aria-pressed',String(enabled));
  });
  document.querySelector('[data-contrast]')?.addEventListener('click',event=>{
    const enabled=document.body.classList.toggle('high-contrast');event.currentTarget.setAttribute('aria-pressed',String(enabled));
  });
})();
