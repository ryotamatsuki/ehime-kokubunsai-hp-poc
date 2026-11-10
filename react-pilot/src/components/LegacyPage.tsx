import SiteTheme from './SiteTheme';

interface Props { html: string; title: string; source: string }
export default function LegacyPage({html,title,source}: Props) {
  return <SiteTheme>
    <div className="react-migrated-page" data-migrated-from={source}
      aria-label={title} dangerouslySetInnerHTML={{__html:html}} />
  </SiteTheme>;
}
