import SiteTheme from './SiteTheme';
import { eventImage, pilotRoot, legacyRoot, type FestivalEvent } from '../types';

export default function EventDetail({event}: {event: FestivalEvent}) {
  const sample = event.kind === 'sample';
  return <SiteTheme>
    <article className="section-shell detail-layout">
      <div className="detail-header">
        <p className="eyebrow">EVENT DETAIL / {event.genre.toUpperCase()}</p>
        <p><span className={sample ? 'status sample' : 'status verified'}>{sample ? '掲載例・架空の催し' : '確認済み'}</span></p>
        <h1>{event.title}</h1>
        <p className="detail-lead">{event.description}</p>
        {sample && <div role="note" className="notice"><strong>この催しは掲載例です。</strong><p>開催・募集を告知するものではありません。日時・会場・支援内容も実際の実施を保証しません。</p></div>}
      </div>
      <figure className="detail-image"><img src={eventImage(event.image)} width="960" height="640" alt={event.imageAlt}/><figcaption>AI生成イメージ。実際の催しの写真ではありません。</figcaption></figure>
      <section className="detail-information" aria-labelledby="detail-information-title">
        <h2 id="detail-information-title">催しの概要</h2>
        <dl className="info-list">
          <div><dt>日時</dt><dd>{event.date}</dd></div><div><dt>場所</dt><dd>{event.venue}</dd></div>
          <div><dt>料金</dt><dd>{event.fee}</dd></div><div><dt>掲載状況</dt><dd>{event.status}</dd></div>
          <div><dt>申し込み</dt><dd>{event.booking}</dd></div>
          <div><dt>参加の支援</dt><dd>{event.supportStatus}</dd></div>
        </dl>
        {event.dateNote && <p className="note-text">{event.dateNote}</p>}
        {event.source && <p className="source-link"><a href={event.source} target="_blank" rel="noopener noreferrer">公式の出典を確認する <span aria-hidden="true">↗</span></a></p>}
        <div className="hero-actions detail-actions"><a className="link-button primary" href={pilotRoot + '/events/'}>催し一覧へ戻る</a><a className="link-button outline" href={legacyRoot + '/events/' + event.page}>現行v2の詳細を見る ↗</a></div>
      </section>
    </article>
  </SiteTheme>;
}
