/* Public cultural records -> personal observations -> a local word workshop. */
(() => {
  'use strict';
  const fields=window.EHIME_V2_DATA?.fieldnotes||[], byId=new Map(fields.map(r=>[r.id,r]));
  const routes=window.EHIME_V2_ROUTES||{}, assetBase=document.documentElement.dataset.assetBase||'';
  const storageKey='ehime-v2-field-observations',haikuKey='ehime-v2-kana-poem';
  const cleanNotes=value=>Object.fromEntries(fields.filter(r=>value&&typeof value[r.id]==='string'&&value[r.id].trim()).map(r=>[r.id,[...value[r.id].replace(/[\u0000-\u001f]/g,' ').trim()].slice(0,80).join('')]));
  let notes={};let canStore=true;
  try{notes=cleanNotes(JSON.parse(localStorage.getItem(storageKey)||'{}'));}catch(_){canStore=false;}
  if(window.__POC_FIELD_NOTES__)notes=cleanNotes(window.__POC_FIELD_NOTES__);
  const persist=()=>{
    try{localStorage.setItem(storageKey,JSON.stringify(notes));}catch(_){canStore=false;}
    if(window.__POC_OFFLINE__)window.parent.postMessage({type:'ehime-field-notes',notes},'*');
  };
  const download=(content,mime,name)=>{
    const url=URL.createObjectURL(new Blob([content],{type:mime}));const a=document.createElement('a');
    a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  const atlas=document.querySelector('[data-field-atlas]');
  if(atlas&&fields.length){
    const nav=atlas.querySelector('[data-field-choices]'),panels=[...atlas.querySelectorAll('[data-field-panel]')];
    const form=atlas.querySelector('[data-field-note-form]'),input=atlas.querySelector('[data-field-note]'),status=atlas.querySelector('[data-field-note-status]');
    const tabs=[...nav.querySelectorAll('[data-field-choice]')].map(anchor=>{
      const b=document.createElement('button');b.type='button';b.dataset.fieldChoice=anchor.dataset.fieldChoice;b.innerHTML=anchor.innerHTML;
      b.id='field-choice-'+b.dataset.fieldChoice;b.setAttribute('role','tab');b.setAttribute('aria-controls','field-'+b.dataset.fieldChoice);anchor.replaceWith(b);return b;
    });
    nav.setAttribute('role','tablist');nav.setAttribute('aria-label','土地の文化の記録');
    let active=fields[0].id;
    const select=(id,focus=false)=>{
      if(!byId.has(id))return;active=id;
      tabs.forEach(tab=>{const selected=tab.dataset.fieldChoice===id;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;if(selected&&focus)tab.focus();});
      panels.forEach(panel=>{panel.hidden=panel.dataset.fieldPanel!==id;panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby','field-choice-'+panel.dataset.fieldPanel);panel.tabIndex=0;});
      input.value=notes[id]||'';status.textContent='';
      const params=new URLSearchParams(window.__POC_QUERY__??location.search);params.set('place',id);
      if(window.__POC_OFFLINE__)window.__POC_QUERY__='?'+params.toString();
      else if(location.protocol==='http:'||location.protocol==='https:')history.replaceState(null,'',location.pathname+'?'+params.toString()+location.hash);
    };
    tabs.forEach((tab,index)=>{
      tab.addEventListener('click',()=>select(tab.dataset.fieldChoice));
      tab.addEventListener('keydown',event=>{
        const moves={ArrowRight:1,ArrowLeft:-1};let next;
        if(event.key in moves)next=(index+moves[event.key]+tabs.length)%tabs.length;
        else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else return;
        event.preventDefault();select(tabs[next].dataset.fieldChoice,true);
      });
    });
    const selected=new URLSearchParams(window.__POC_QUERY__??location.search).get('place');select(byId.has(selected)?selected:fields[0].id);
    form.hidden=false;form.addEventListener('submit',event=>{
      event.preventDefault();const value=[...input.value.trim()].slice(0,80).join('');
      if(!value){status.textContent='気づいたことを、ひと言入力してください。';input.focus();return;}
      notes[active]=value;persist();status.textContent=byId.get(active).place+'で気づいたことを文化帖に残しました。'+(canStore?'':'この環境では保存を利用できません。確認ファイル内の移動では引き継ぎます。');
    });
  }
  const journal=document.querySelector('[data-field-journal-list]');
  if(journal){
    const status=document.querySelector('[data-field-journal-status]'),exportButton=document.querySelector('[data-field-journal-export]');
    const render=focusIndex=>{
      journal.replaceChildren();const entries=fields.filter(r=>notes[r.id]);
      for(const r of entries){
        const a=document.createElement('article');a.className='field-journal-item';
        const img=document.createElement('img'),key='assets/culture/'+r.id+'-480.webp';
        img.src=window.__POC_ASSET_URLS__?.[key]||(assetBase?assetBase.replace(/\/$/,'')+'/':'')+key;img.alt=r.photo.title;img.width=r.photo.width;img.height=r.photo.height;img.loading='lazy';
        const copy=document.createElement('div'),h3=document.createElement('h3'),link=document.createElement('a');
        const params=new URLSearchParams(window.__POC_QUERY__??location.search);params.set('place',r.id);
        link.href=(routes['culture-atlas.html']||'culture-atlas.html')+'?'+params;link.textContent=r.place+' / '+r.subject;h3.append(link);
        const quote=document.createElement('p');quote.className='field-journal-words';quote.textContent=notes[r.id];
        const credit=document.createElement('p');credit.className='small';credit.textContent='写真：'+r.photo.author+' · '+r.photo.license+' / '+r.photo.date;
        const source=document.createElement('a');source.className='text-link';source.href=r.source;source.textContent='文化背景の出典 ↗';
        const photoSource=document.createElement('a');photoSource.className='text-link';photoSource.href=r.photo.source;photoSource.textContent='写真の出典・利用条件 ↗';
        copy.append(h3,quote,credit,source,photoSource);
        const remove=document.createElement('button');remove.type='button';remove.className='remove-note';remove.dataset.removeField=r.id;remove.textContent='削除';remove.setAttribute('aria-label',r.place+'のことばを文化帖から削除');
        remove.addEventListener('click',()=>{const index=entries.findIndex(e=>e.id===r.id);delete notes[r.id];persist();render(index);status.textContent=r.place+'のことばを削除しました。';});
        a.append(img,copy,remove);journal.append(a);
      }
      document.querySelector('[data-field-journal-empty]').hidden=!!entries.length;exportButton.hidden=!entries.length;
      if(focusIndex!==undefined){const buttons=journal.querySelectorAll('[data-remove-field]');if(buttons.length)buttons[Math.min(focusIndex,buttons.length-1)].focus();else document.querySelector('[data-field-journal-empty]').setAttribute('tabindex','-1'),document.querySelector('[data-field-journal-empty]').focus();}
    };
    exportButton.addEventListener('click',()=>{
      const lines=['わたしの愛媛 / 土地から見つけたことば','文化紹介の記録と、自分の観察。開催予定・移動の旅程ではありません。',''];
      fields.filter(r=>notes[r.id]).forEach(r=>lines.push(r.place+' / '+r.subject,notes[r.id],'文化背景：'+r.source,'写真：'+r.photo.author+' / '+r.photo.date+' / '+r.photo.license,r.photo.source,r.photo.licenseUrl,''));
      download(lines.join('\n'),'text/plain;charset=utf-8','my-ehime-cultural-notes.txt');status.textContent='ことばの記録をテキストファイルにしました。';
    });render();
  }
  const studio=document.querySelector('[data-haiku-studio]');
  if(studio){
    const inputs=[...studio.querySelectorAll('[data-haiku-line]')],preview=studio.querySelector('[data-haiku-preview]'),status=studio.querySelector('[data-haiku-status]'),exportButton=studio.querySelector('[data-haiku-export]'),reset=studio.querySelector('[data-haiku-reset]');
    const sample=['あきのそら','ことばひろって','まちをゆく'];let initial;
    try{initial=JSON.parse(localStorage.getItem(haikuKey)||'null');}catch(_){}
    if(window.__POC_HAIKU__)initial=window.__POC_HAIKU__;
    if(Array.isArray(initial)&&initial.length===3&&initial.every(v=>typeof v==='string'))inputs.forEach((input,i)=>input.value=[...initial[i]].slice(0,24).join(''));
    const sounds=text=>{
      let count=0,last='';for(const letter of text.normalize('NFKC').replace(/[\s、。・！？!?]/g,'')){
        if(!/^[\u3041-\u3096\u30a1-\u30faー]$/.test(letter))return null;
        if(!'ぁぃぅぇぉゃゅょゎァィゥェォャュョヮ'.includes(letter)||!last||'っんッンーぁぃぅぇぉゃゅょゎァィゥェォャュョヮ'.includes(last))count++;
        last=letter;
      }return count;
    };
    const update=()=>{
      const words=inputs.map(i=>[...i.value].slice(0,24).join('')),counts=words.map(sounds);preview.replaceChildren();
      words.forEach((word,i)=>{const p=document.createElement('p');p.textContent=word||'　';preview.append(p);studio.querySelector('[data-haiku-count="'+i+'"]').textContent=counts[i]===null?'かなで読みを入力':counts[i]+'音';});
      preview.style.setProperty('--poem-size',Math.min(44,390/Math.max(1,...words.map(w=>[...w].length)))+'px');
      const valid=words.every(w=>w.trim())&&counts.every(n=>n!==null&&n>0);exportButton.disabled=!valid;
      status.textContent=valid?(counts.join('・')+'音。'+(counts.join(',')==='5,7,5'?'五・七・五になりました。':'自由な音数でも持ちかえられます。')):'各句を、ひらがな・カタカナで入力してください。漢字は読みを入力すると音数を確かめられます。';
      try{localStorage.setItem(haikuKey,JSON.stringify(words));}catch(_){}
      if(window.__POC_OFFLINE__)window.parent.postMessage({type:'ehime-kana-poem',words},'*');
    };
    inputs.forEach(i=>{i.maxLength=24;i.addEventListener('input',update);});
    studio.querySelector('form').addEventListener('submit',e=>e.preventDefault());reset.disabled=false;
    reset.addEventListener('click',()=>{inputs.forEach((input,i)=>input.value=sample[i]);update();inputs[0].focus();});
    const xml=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
    exportButton.addEventListener('click',()=>{
      const words=inputs.map(i=>[...i.value].slice(0,24).join(''));if(words.some(w=>sounds(w)===null||!w.trim()))return;
      const size=Math.min(38,600/Math.max(1,...words.map(w=>[...w].length)));
      const poem=words.map((w,i)=>'<text x="70" y="'+(220+i*110)+'" font-size="'+size+'">'+xml(w)+'</text>').join('');
      const svg='<svg xmlns="http://www.w3.org/2000/svg" width="760" height="660" viewBox="0 0 760 660"><title>'+xml(words.join(' / '))+'</title><rect width="760" height="660" fill="#f5f2ea"/><g fill="#151d36" font-family="sans-serif"><text x="70" y="80" font-size="20">MY EHIME / ことばの記録</text>'+poem+'<text x="70" y="560" font-size="18">自分の景色を、ことばに。 / 愛媛の文化から</text><text x="70" y="600" font-size="16">個人の作例。公式の投句・開催告知ではありません。</text></g></svg>';
      download(svg,'image/svg+xml;charset=utf-8','my-ehime-words.svg');status.textContent='あなたのことばをSVGファイルにしました。';
    });update();
  }
})();
