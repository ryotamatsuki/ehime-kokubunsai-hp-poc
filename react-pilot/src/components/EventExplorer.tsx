import { useEffect, useMemo, useState } from 'react';
import { Button } from '@astryxdesign/core/Button';
import catalog from '../data/events.json';
import SiteTheme from './SiteTheme';
import { eventImage, pilotRoot, type FestivalEvent } from '../types';

const events = catalog as FestivalEvent[];
export function filterEvents(items: FestivalEvent[], term: string, city: string, genre: string, kind: string) {
  const query = term.trim().toLocaleLowerCase('ja-JP');
  return items.filter((event) => {
    const matchesTerm = !query || [event.title, event.shortTitle, event.city, event.genre,
      event.description].join(' ').toLocaleLowerCase('ja-JP').includes(query);
    return matchesTerm && (!city || event.city === city) &&
      (!genre || event.genre === genre) && (!kind || event.kind === kind);
  });
}
export default function EventExplorer() {
  const [term, setTerm] = useState('');
  const [city, setCity] = useState('');
  const [genre, setGenre] = useState('');
  const [kind, setKind] = useState('');
  const cities = Array.from(new Set(events.map(e => e.city)));
  const genres = Array.from(new Set(events.map(e => e.genre)));
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setTerm(params.get('q') ?? '');
    setCity(params.get('city') ?? '');
    setGenre(params.get('genre') ?? '');
    setKind(params.get('kind') ?? '');
  }, []);
  useEffect(() => {
    const params = new URLSearchParams();
    if (term) params.set('q', term);
    if (city) params.set('city', city);
    if (genre) params.set('genre', genre);
    if (kind) params.set('kind', kind);
    const target = window.location.pathname + (params.size ? '?' + params.toString() : '');
    window.history.replaceState(null, '', target);
  }, [term,city,genre,kind]);
  const visible = useMemo(() => filterEvents(events,term,city,genre,kind), [term,city,genre,kind]);
  const reset = () => {setTerm('');setCity('');setGenre('');setKind('');};
  return <SiteTheme>
    <section className="section-shell list-heading">
      <p className="eyebrow">EXPLORE EVENTS</p><h1>催しを探す。</h1>
      <p className="body-muted">地域、ジャンル、掲載区分で絞り込めます。現在の内容にはデザイン確認用の掲載例が含まれています。</p>
    </section>
    <section className="section-shell" aria-label="催しの絞り込み">
      <div className="filter-panel">
        <div className="filter-field wide"><label htmlFor="filter-keyword">キーワード</label><input id="filter-keyword" type="search" value={term} onChange={e=>setTerm(e.target.value)} placeholder="催し名・文化・地域から探す" /></div>
        <div className="filter-field"><label htmlFor="filter-city">地域</label><select id="filter-city" value={city} onChange={e=>setCity(e.target.value)}><option value="">すべての地域</option>{cities.map(c=><option key={c} value={c}>{c}</option>)}</select></div>
        <div className="filter-field"><label htmlFor="filter-genre">ジャンル</label><select id="filter-genre" value={genre} onChange={e=>setGenre(e.target.value)}><option value="">すべてのジャンル</option>{genres.map(g=><option key={g} value={g}>{g}</option>)}</select></div>
        <div className="filter-field"><label htmlFor="filter-kind">掲載区分</label><select id="filter-kind" value={kind} onChange={e=>setKind(e.target.value)}><option value="">すべて</option><option value="verified">確認済み</option><option value="sample">掲載例</option></select></div>
        <div className="filter-reset"><Button label="条件をクリア" variant="secondary" onClick={reset}/></div>
      </div>
      <div className="results-heading"><h2>催しの一覧</h2><p role="status" aria-live="polite">{visible.length}件 / 全{events.length}件</p></div>
      {visible.length===0 && <div className="empty-state"><h3>該当する催しはありません。</h3><p>条件を変えてもう一度お試しください。</p></div>}
      <div className="event-grid">
        {visible.map(event=><article className="event-card" key={event.id}>
          <a href={pilotRoot + '/events/' + event.id + '/'} className="event-image-link"><img src={eventImage(event.image)} alt={event.imageAlt} loading="lazy" width="960" height="640"/></a>
          <div className="event-card-inner">
            <div className="event-tags"><span className={event.kind === 'verified' ? 'status verified' : 'status sample'}>{event.kind==='verified' ? '確認済み' : '掲載例・架空の催し'}</span><span>{event.city} · {event.genre}</span></div>
            <h3><a href={pilotRoot + '/events/' + event.id + '/'}>{event.title}<span aria-hidden="true"> ↗</span></a></h3>
            <p>{event.date}</p><p className="event-desc">{event.description}</p>
            <div className="event-card-footer">{event.kind==='sample' ? '申込み不可・表示用の情報です' : event.status}</div>
          </div>
        </article>)}
      </div>
    </section>
  </SiteTheme>;
}
