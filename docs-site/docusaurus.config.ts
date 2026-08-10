import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Health-AICare',
  tagline: 'An Agentic AI Framework for Proactive Mental Health Support',
  favicon: 'img/favicon.ico',

  url: 'https://lombeytjhtt96-glitch.github.io',
  baseUrl: '/Health-AICare/',

  organizationName: 'lombeytjhtt96-glitch',
  projectName: 'Health-AICare',

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
              'https://github.com/lombeytjhtt96-glitch/Health-AICare/tree/main/docs-site/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/health-aicare-social-card.png',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Health-AICare',
      logo: {
        alt: 'Health-AICare Logo',
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
          href: 'https://github.com/lombeytjhtt96-glitch/Health-AICare',
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
            {label: 'Health-AI Autopilot', to: '/docs/health-ai-autopilot/policy-governed-autonomy'},
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
              href: 'https://github.com/lombeytjhtt96-glitch/Health-AICare',
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
      copyright: `Copyright © ${new Date().getFullYear()} Health-AICare. Built with Docusaurus.`,
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
