import {useState} from 'react';
import SiteTheme from './SiteTheme';
import cultureData from '../data/culture.json';
import events from '../data/events.json';
import {eventImage,legacyRoot,pilotRoot} from '../types';

const fieldnotes=cultureData.fieldnotes;
const cultures=cultureData.cultures;
const latestEvents=events;
const fieldImage=(id:string)=>legacyRoot+'/design-lab/assets/culture/'+id+'-960.webp';
const href=(path:string)=>pilotRoot+'/'+path.replace(/^\/|\/$/g,'')+(path?'/':'');
export default function HomeExperience(){
  const [selected,setSelected]=useState(fieldnotes[0].id);
  const note=fieldnotes.find(n=>n.id===selected)??fieldnotes[0];
  return <SiteTheme>
    <section className="hero section-shell" aria-labelledby="hero-title">
      <div className="hero-content">
        <p className="eyebrow">EHIME / CULTURE / 2028</p>
        <h1 id="hero-title">愛媛を、<br/><span>ひらく。</span></h1>
        <p className="hero-lead">観る。つくる。出会う。<br/>文化の担い手は、あなた。</p>
        <p className="body-muted">土地の歴史に触れ、表現に出会い、誰もが文化をつくる側になる。愛媛県全体を舞台にした文化祭へ。</p>
        <div className="hero-actions">
          <a className="link-button primary" href={href('events')}>催しを探す <span aria-hidden="true">↗</span></a>
          <a className="link-button outline" href={href('recruitment')}>参加・募集 <span aria-hidden="true">↗</span></a>
        </div>
        <p className="festival-date"><strong>2028.10.22 — 12.03</strong><br/>第43回国民文化祭・第28回全国障害者芸術・文化祭</p>
        <a className="hero-discover" href="#discover">土地の文化をたどる <span aria-hidden="true">↓</span></a>
      </div>
      <figure className="hero-visual">
        <img src={legacyRoot+'/design-lab/assets/art/festival-hero-960.webp'} alt="文化祭で多世代の人々が舞台や作品を楽しむAI生成イメージ。実際の開催写真ではありません。" width="960" height="640" fetchPriority="high"/>
        <figcaption>文化と人が、出会う場所。 <small>AI生成イメージ</small></figcaption>
      </figure>
    </section>
    <section className="atlas-section" id="discover" aria-labelledby="atlas-title">
      <div className="section-shell">
        <div className="atlas-intro">
          <div><p className="eyebrow">FIELDNOTES / EHIME</p><h2 id="atlas-title">土地の時間に、<br/>出会う。</h2></div>
          <p>東予・中予・南予。それぞれの土地に、語り継がれてきた音やことば、技と舞台がある。記録写真と地域の資料を手がかりに巡ります。</p>
        </div>
        <div className="atlas-controls" aria-label="文化の記録を選ぶ">
          {fieldnotes.map((item,index)=><button type="button" key={item.id} onClick={()=>setSelected(item.id)}
            aria-pressed={item.id===selected} className="atlas-choice">
            <small>{String(index+1).padStart(2,'0')} / {item.place}</small><strong>{item.subject}</strong>
          </button>)}
        </div>
        <div className="atlas-layout">
          <figure className="atlas-photo">
            <img key={note.id} src={fieldImage(note.id)} width={note.photo.width} height={note.photo.height}
              alt={note.photo.title} loading="lazy"/>
            <figcaption>写真：<a href={note.photo.source} target="_blank" rel="noopener noreferrer">{note.photo.author}</a> ／ {note.photo.date} ／ <a href={note.photo.licenseUrl} target="_blank" rel="noopener noreferrer">{note.photo.license}</a></figcaption>
          </figure>
          <div className="atlas-caption">
            <p className="eyebrow">CULTURE / {note.place}</p>
            <h3>{note.subject}</h3>
            <p>一つの文化を、場所から知る。写真の背景や出典をたどり、愛媛の文化を少しずつ見つめてみませんか。</p>
            <a className="text-action" href={note.source} target="_blank" rel="noopener noreferrer">地域の一次資料を見る <span aria-hidden="true">↗</span></a>
            <a className="text-action" href={href('culture/field-notes')}>文化の記録を読む <span aria-hidden="true">↗</span></a>
          </div>
        </div>
      </div>
    </section>
    <section className="section-shell culture-index" aria-labelledby="culture-title">
      <div className="section-intro"><div><p className="eyebrow">FOUR WAYS TO EXPERIENCE CULTURE</p><h2 id="culture-title">文化の入り口は、<br/>ひとつじゃない。</h2></div>
        <p>手を動かすこと、ことばにすること、味わうこと、表現を見つめること。興味から選べる四つの入口。</p></div>
      <div className="culture-grid">{cultures.map((c,i)=><a className={'culture-card culture-card-'+i} key={c.id} href={href('culture/'+c.id)}>
        <div className="culture-meta"><span>{c.number} / {c.genre}</span><span>{c.place}</span></div>
        <h3>{c.title}</h3><p>{c.intro}</p><span className="culture-arrow" aria-hidden="true">↗</span>
      </a>)}</div>
    </section>
    <section className="event-section" aria-labelledby="events-title">
      <div className="section-shell">
        <div className="section-intro">
          <div><p className="eyebrow">EVENT GUIDE</p><h2 id="events-title">催しから、出会う。</h2></div>
          <p>確認できた開催案内と、サイトの表示を確かめるための架空の掲載例を分けて紹介します。掲載例は申し込みできません。</p>
        </div>
        <div className="home-events-grid">
          {latestEvents.map(event=><article className="home-event-card" key={event.id}>
            <a href={href('events/'+event.id)} className="home-event-image"><img src={eventImage(event.image)} alt={event.imageAlt} loading="lazy" width="960" height="640"/></a>
            <div className="home-event-content">
              <div className="event-tags"><span className={event.kind==='verified'?'status verified':'status sample'}>{event.kind==='verified'?'確認済み':'架空の掲載例'}</span><span>{event.city} / {event.genre}</span></div>
              <h3><a href={href('events/'+event.id)}>{event.title}</a></h3>
              <p>{event.date}</p><small>{event.kind==='sample'?'開催・募集を告知するものではありません。':event.status}</small>
            </div>
          </article>)}
        </div>
        <p className="all-events-link"><a className="link-button primary" href={href('events')}>すべての催しを探す <span aria-hidden="true">↗</span></a></p>
      </div>
    </section>
    <section className="section-shell participate-section" aria-labelledby="participate-title">
      <div className="participate-intro"><p className="eyebrow">CULTURE BEGINS WITH YOU</p><h2 id="participate-title">観るだけでは、<br/>終わらない。</h2><p>気になる催しを残したり、ことばをつくったり。小さな参加から文化との距離を縮めてみる。</p></div>
      <div className="participate-links">
        <a href={href('culture/notebook')}><span>01 / CULTURE NOTEBOOK</span><strong>わたしの文化帖。</strong><small>気になる催しや発見を残す</small><b aria-hidden="true">↗</b></a>
        <a href={href('culture/literature')}><span>02 / HAIKU</span><strong>十七音の、余白。</strong><small>松山の文化に出会い、自分のことばをつくる</small><b aria-hidden="true">↗</b></a>
        <a href={href('accessibility/information-support')}><span>03 / ACCESSIBILITY</span><strong>誰もが参加する。</strong><small>参加の支援や相談窓口を確認する</small><b aria-hidden="true">↗</b></a>
      </div>
    </section>
    <section className="section-shell note-panel"><div><p className="eyebrow">INFORMATION</p><h2>本大会は2028年開催。</h2></div><div><p>個別の催しは順次発表されます。現時点の公式情報と仮の掲載例は区別してご覧ください。</p><a className="text-action" href={href('festival-guide')}>大会の概要を見る <span aria-hidden="true">↗</span></a></div></section>
  </SiteTheme>;
}
