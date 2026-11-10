import type { ReactNode } from 'react';
import { Theme } from '@astryxdesign/core/theme';
import { stoneTheme } from '@astryxdesign/theme-stone/built';

export default function SiteTheme({children}: {children: ReactNode}) {
  return <Theme theme={stoneTheme} mode="light">{children}</Theme>;
}
