import styles from './Layout.module.scss';
import { ThemeProvider, Button, Icon } from '@gravity-ui/uikit';
import { Sun, Moon } from '@gravity-ui/icons';
import { ReactNode, useState } from 'react';
import logo from '../../static/icons/logo.svg';

export interface WrapperProps {
  children: ReactNode;
}

const DARK = 'dark';
const LIGHT = 'light';
const DEFAULT_THEME = DARK;

export const Layout = (props: WrapperProps) => {

  const [theme, setTheme] = useState<'light' | 'dark'>(DEFAULT_THEME);

  return (
    <ThemeProvider theme={theme}>
          <header className={styles.header}>
            <img src={logo} alt="" className={styles.logo} />
            <Button onClick={() => setTheme(theme => theme === DARK ? LIGHT : DARK)} size={"l"} view='outlined'>
              <Icon data={theme === DARK ? Sun : Moon} />
            </Button>
          </header>
          <main className={styles.main}>
            {
              props.children
            }
          </main>
    </ThemeProvider>
  )
}