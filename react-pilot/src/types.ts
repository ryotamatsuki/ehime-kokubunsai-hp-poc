export type FestivalEvent = {
  id: string;
  title: string;
  shortTitle: string;
  city: string;
  genre: string;
  kind: 'sample' | 'verified';
  date: string;
  venue: string;
  fee: string;
  booking: string;
  status: string;
  description: string;
  page: string;
  image: string;
  imageAlt: string;
  supports: string[];
  supportStatus: string;
  source: string;
  dateNote: string;
};
export const legacyRoot = 'https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc';
export const pilotRoot = import.meta.env.BASE_URL.replace(/\/$/, '');
export const eventImage = (image: string) =>
  legacyRoot + '/design-lab/assets/art/' + image + '-960.webp';
