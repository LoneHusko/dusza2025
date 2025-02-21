// @ts-check

const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Dusza2025 - ${csapatnev}',
  tagline: 'Folyamatkezelő Rendszer',

  url: 'https://dusza2025.pages.dev',
  baseUrl: '/',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'hu',
    locales: ['hu'],
  },

  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '../docs',
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/LoneHusko/dusza2025/tree/master/',
        },
        blog: false,
        theme: {
          customCss: [require.resolve('./src/css/docs.css')],
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Dusza2025 - ${csapatnev}',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'mainSidebar',
            position: 'left',
            label: 'Dokumentáció',
          },
          {
            href: 'https://github.com/LoneHusko/dusza2025',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      prism: {
        theme: themes.gruvboxMaterialLight,
        darkTheme: themes.gruvboxMaterialDark,
        additionalLanguages: ['python', 'bash'],
      },
    }),
};

module.exports = config; 