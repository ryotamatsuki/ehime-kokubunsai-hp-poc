/* Optional SVG painting: no animation loop, GPU scene, or network. */
(() => {
  'use strict';
  const studio=document.querySelector('[data-paint-studio]'); if(!studio)return;
  const board=studio.querySelector('[data-paint-board]'),layer=studio.querySelector('[data-paint-lines]');
  const mode=studio.querySelector('[data-paint-mode]'),instruction=studio.querySelector('[data-paint-instruction]');
  const status=studio.querySelector('[data-paint-status]');const key='ehime-v2-blue-painting';const ns='http://www.w3.org/2000/svg';
  let lines=[],drawing=false,points=[],pending=null,serial=0,storage=true;
  const clean=items=>Array.isArray(items)?items.slice(0,32).filter(item=>item&&typeof item.d==='string'&&item.d.length<=10000&&/^[MLCQZmlcqz\d.,\s-]+$/.test(item.d)&&Number.isFinite(item.width)&&item.width>=2&&item.width<=20).map(item=>({d:item.d,width:item.width})):[];
  try{lines=clean(JSON.parse(localStorage.getItem(key)||'[]'))}catch(_){storage=false}
  if(Array.isArray(window.__POC_PAINTING__))lines=clean(window.__POC_PAINTING__);
  const persist=()=>{try{localStorage.setItem(key,JSON.stringify(lines))}catch(_){storage=false}if(window.__POC_OFFLINE__)window.parent.postMessage({type:'ehime-v2-painting',lines},'*')};
  const path=line=>{const node=document.createElementNS(ns,'path');node.setAttribute('d',line.d);node.setAttribute('stroke','#183c9e');node.setAttribute('stroke-width',String(line.width));node.setAttribute('opacity','.86');return node};
  const refresh=message=>{
    layer.replaceChildren(...lines.map(path));
    studio.querySelector('[data-paint-undo]').disabled=!lines.length;studio.querySelector('[data-paint-clear]').disabled=!lines.length;studio.querySelector('[data-paint-export]').disabled=!lines.length;
    status.textContent=message||lines.length+'筆の絵付けです。';board.setAttribute('aria-label','デジタル絵付けのプレビュー。'+lines.length+'筆の円・波・線。');
    if(!storage)instruction.textContent='この環境では絵付けの保存を利用できません。つくった絵付けは「持ちかえる」から保存できます。';
  };
  const add=line=>{if(lines.length>=32){status.textContent='32筆まで重ねられます。一筆戻すか、消して続けてください。';return}lines.push(line);persist();refresh('一筆加えました。'+lines.length+'筆の絵付けです。')};
  const presets={
    circle:n=>({d:'M '+(139+n*3)+' '+(279-n*3)+' C 96 110 359 72 447 209 C 533 343 299 480 173 347',width:7+n%3}),
    wave:n=>({d:'M 97 '+(225+n*22)+' C 175 '+(148+n*22)+' 241 '+(326+n*22)+' 316 '+(235+n*22)+' C 390 '+(160+n*22)+' 445 '+(300+n*22)+' 511 '+(217+n*22),width:8+n%4}),
    line:n=>({d:'M '+(165+n*23)+' 141 Q '+(207+n*23)+' 243 '+(347+n*11)+' 381',width:12-n%5})
  };
  studio.querySelectorAll('[data-paint-preset]').forEach(button=>button.addEventListener('click',()=>{const preset=presets[button.dataset.paintPreset];if(preset){add(preset(serial%6));serial++}}));
  const toggle=on=>{drawing=on;if(!on&&pending){pending.remove();pending=null;points=[]}mode.setAttribute('aria-pressed',String(on));board.dataset.painting=String(on);instruction.textContent=on?'描くモードです。器の中で指やマウスを動かすと線を描けます。ページをスクロールするときは「描き終える」を選んでください。':'図形を加えるボタンはキーボードでも操作できます。「自分で描く」を選ぶと、器の中に線を描けます。';mode.textContent=on?'描き終える':'自分で描く'};
  mode.addEventListener('click',()=>toggle(!drawing));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&drawing){toggle(false);mode.focus();status.textContent='描くモードを終了しました。'}});
  studio.querySelector('[data-paint-undo]').addEventListener('click',()=>{lines.pop();persist();refresh('一筆戻しました。'+lines.length+'筆の絵付けです。')});
  studio.querySelector('[data-paint-clear]').addEventListener('click',()=>{lines=[];persist();refresh('絵付けを消しました。')});
  const coordinate=event=>{const rect=board.getBoundingClientRect();return{x:Math.max(0,Math.min(600,(event.clientX-rect.left)*600/rect.width)),y:Math.max(0,Math.min(540,(event.clientY-rect.top)*540/rect.height))}};
  const inside=point=>(point.x-300)**2+(point.y-263)**2<=206**2;
  const makePath=values=>values.map((point,index)=>(index?'L ':'M ')+point.x.toFixed(1)+' '+point.y.toFixed(1)).join(' ');
  board.addEventListener('pointerdown',event=>{
    if(!drawing||event.isPrimary===false||(event.button!==undefined&&event.button!==0)||lines.length>=32)return;const point=coordinate(event);if(!inside(point))return;
    event.preventDefault();points=[point];pending=path({d:makePath(points),width:9});layer.append(pending);board.setPointerCapture?.(event.pointerId);
  });
  board.addEventListener('pointermove',event=>{
    if(!pending||!drawing||points.length>=256)return;const point=coordinate(event);if(!inside(point))return;
    const previous=points[points.length-1];if((point.x-previous.x)**2+(point.y-previous.y)**2<9)return;
    points.push(point);pending.setAttribute('d',makePath(points));
  });
  const finish=()=>{if(!pending)return;pending.remove();pending=null;if(points.length>1)add({d:makePath(points),width:9});points=[]};
  board.addEventListener('pointerup',finish);board.addEventListener('pointercancel',()=>{pending?.remove();pending=null;points=[];refresh('描画を中断しました。')});
  studio.querySelector('[data-paint-export]').addEventListener('click',()=>{
    if(!lines.length)return;const copy=board.cloneNode(true);copy.setAttribute('xmlns',ns);copy.removeAttribute('data-paint-board');copy.removeAttribute('data-painting');copy.removeAttribute('role');
    const blob=new Blob([new XMLSerializer().serializeToString(copy)],{type:'image/svg+xml;charset=utf-8'});const url=URL.createObjectURL(blob);const anchor=document.createElement('a');anchor.href=url;anchor.download='ehime-my-blue.svg';document.body.append(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='絵付けをSVGファイルで持ちかえられます。';
  });
  studio.hidden=false;refresh();
})();
