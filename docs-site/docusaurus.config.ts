import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'HealthAICare',
  tagline: 'An Agentic AI Framework for Proactive Mental Health Support',
  favicon: 'img/favicon.ico',

  url: 'https://lombeytjhtt96-glitch.github.io',
  baseUrl: '/HealthAICare/',

  organizationName: 'lombeytjhtt96-glitch',
  projectName: 'HealthAICare',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
            editUrl:
              'https://github.com/lombeytjhtt96-glitch/HealthAICare/tree/main/docs-site/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/health_aicare-social-card.png',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'HealthAICare',
      logo: {
        alt: 'HealthAICare Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://aicare.sumbu.xyz',
          label: 'Live Demo',
          position: 'right',
        },
        {
          href: 'https://github.com/lombeytjhtt96-glitch/HealthAICare',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'Documentation',
          items: [
            {label: 'Introduction', to: '/docs/intro'},
            {label: 'Architecture', to: '/docs/architecture/system-overview'},
            {label: 'HealthAI Autopilot', to: '/docs/health_ai-autopilot/policy-governed-autonomy'},
          ],
        },
        {
          title: 'Project',
          items: [
            {
              label: 'Live App',
              href: 'https://aicare.sumbu.xyz',
            },
            {
              label: 'API Docs',
              href: 'https://api.aicare.sumbu.xyz/docs',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/lombeytjhtt96-glitch/HealthAICare',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'WHO Guidelines',
              href: 'https://www.who.int/publications/i/item/9789240031081',
            },
            {
              label: 'Kemenkes RI',
              href: 'https://kemkes.go.id',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} HealthAICare. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'json', 'typescript'],
    },
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
