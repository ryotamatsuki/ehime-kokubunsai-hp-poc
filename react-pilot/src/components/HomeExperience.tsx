import SiteTheme from './SiteTheme';
import { legacyRoot, pilotRoot } from '../types';

export default function HomeExperience() {
  return <SiteTheme>
    <section className="hero section-shell" aria-labelledby="hero-title">
      <div className="hero-content">
        <p className="eyebrow">EHIME / CULTURE / 2028</p>
        <h1 id="hero-title">愛媛を、<br/><span>ひらく。</span></h1>
        <p className="hero-lead">観る。つくる。出会う。<br/>文化の担い手は、あなた。</p>
        <p className="body-muted">土地の歴史に触れ、表現に出会い、誰もが文化をつくる側になる。愛媛県全体を舞台にした文化祭へ。</p>
        <div className="hero-actions">
          <a className="link-button primary" href={pilotRoot + '/events/'}>催しを探す <span aria-hidden="true">↗</span></a>
          <a className="link-button outline" href={legacyRoot + '/recruitment/index.html'}>参加・募集 <span aria-hidden="true">↗</span></a>
        </div>
        <p className="festival-date"><strong>2028.10.22 — 12.03</strong><br/>第43回国民文化祭・第28回全国障害者芸術・文化祭</p>
      </div>
      <figure className="hero-visual">
        <img src={legacyRoot + '/design-lab/assets/art/festival-hero-960.webp'} alt="文化祭で多世代の人々が舞台や作品を楽しむAI生成イメージ。実際の開催写真ではありません。" width="960" height="640" fetchPriority="high"/>
        <figcaption>文化と人が、出会う場所。 <small>AI生成イメージ</small></figcaption>
      </figure>
    </section>
    <section className="section-shell intro-band" aria-labelledby="intro-title">
      <div className="heading-line"><p className="eyebrow">DISCOVER CULTURE</p><h2 id="intro-title">土地の文化から、<br/>新しい発見へ。</h2></div>
      <p>新居浜の太鼓祭り、松山の俳句、内子の芝居小屋、宇和島の牛鬼。地域に根ざした文化を、知ることから始めませんか。</p>
    </section>
    <section className="section-shell feature-grid" aria-label="文化祭を楽しむ入口">
      <a className="feature-card pale-blue" href={pilotRoot + '/events/'}>
        <span className="eyebrow">01 / FIND</span><strong>催しを探す。</strong><p>開催状態や地域、ジャンルから探せます。仮の掲載例は明確に区別します。</p><span className="feature-arrow" aria-hidden="true">↗</span>
      </a>
      <a className="feature-card pale-peach" href={legacyRoot + '/culture/field-notes.html'}>
        <span className="eyebrow">02 / EXPLORE</span><strong>文化に出会う。</strong><p>愛媛の地域に根づく祭り、文学、芸術の背景をたどります。</p><span className="feature-arrow" aria-hidden="true">↗</span>
      </a>
      <a className="feature-card pale-green" href={legacyRoot + '/accessibility/information-support.html'}>
        <span className="eyebrow">03 / JOIN</span><strong>誰もが参加する。</strong><p>情報保障や会場の支援を確認し、安心して参加する入口へ。</p><span className="feature-arrow" aria-hidden="true">↗</span>
      </a>
    </section>
    <section className="section-shell note-panel"><div><p className="eyebrow">INFORMATION</p><h2>本大会は2028年開催。</h2></div><p>催しの正式な開催内容は順次発表されます。実際の開催情報とデザイン確認用の仮イベントを区別して掲載しています。</p></section>
  </SiteTheme>;
}
