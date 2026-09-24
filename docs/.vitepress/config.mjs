// Author:  Daniel Iwugo
// Comment: Christ is King
// Pentimento documentation site.
//
// Separate from Stegobench's site on purpose. Stegobench is a tool you run; Pentimento is a
// corpus you download. The two have different readers, and one site serving both meant a person
// looking for the licence terms had to read past an explanation of pairing discipline to reach
// them.
//
// Everything under this directory is self-contained, so the whole `pentimento/` folder moves to
// a repository of its own without touching anything else.
//
// `ignoreDeadLinks` is deliberately NOT set, so the build fails on a broken internal link.

const BASE = process.env.DOCS_BASE || '/pentimento/'
const SITE = process.env.DOCS_SITE || 'https://elementmerc.github.io'

export default {
  title: 'Pentimento',
  description:
    'A steganalysis corpus of 10,000 permissively licensed cover photographs and '
    + '344,357 matched stego pairs, where every image carries its own licence.',
  lang: 'en-GB',
  base: BASE,
  cleanUrls: true,
  lastUpdated: true,

  srcExclude: ['private/**', 'node_modules/**'],

  head: [
    ['link', { rel: 'icon', href: `${BASE}favicon.svg`, type: 'image/svg+xml' }],
    ['meta', { name: 'theme-color', content: '#F5F5F7' }],

    // The three faces `brand/README.md` specifies: Fraunces for display, Hanken Grotesk for
    // body, IBM Plex Mono for anything a reader compares character by character, which on this
    // site means checksums, licence codes and arm names like `juniward-0400`.
    //
    // Link tags rather than a CSS `@import`, because an import blocks the stylesheet holding it
    // and has to be that file's first statement. `preconnect` opens the two connections while
    // the HTML is still parsing, and `display=swap` means the page renders in the system stack
    // immediately rather than waiting on a font it may never get.
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', {
      rel: 'stylesheet',
      href: 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600'
        + '&family=Hanken+Grotesk:wght@400;500;600;700'
        + '&family=IBM+Plex+Mono:wght@400;500&display=swap',
    }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Pentimento' }],
    ['meta', {
      property: 'og:description',
      content: 'A steganalysis corpus with its licences attached.',
    }],
    // No `og:image` until `public/social-card.png` exists. Pointing the tag at a file nobody
    // drew gives every share a blank preview, which is worse than having no tag. Add the tag
    // and the file in one commit, and note that og:image has to be ABSOLUTE: a card served
    // from a relative path is fetched by a crawler with no page context and does not resolve.
    ['meta', { name: 'twitter:card', content: 'summary' }],
  ],

  themeConfig: {
    // The mark is two overlapping squares: Blue underneath, Ink over it at 92%, an earlier
    // layer showing through a later one. On a dark ground the Ink square disappears into the
    // background, so dark mode gets the reversed mark rather than the same file dimmed.
    logo: { light: '/mark.svg', dark: '/mark-reversed.svg', alt: 'Pentimento' },
    siteTitle: 'Pentimento',

    nav: [
      { text: 'Guide', link: '/guide/what-it-is', activeMatch: '/guide/' },
      { text: 'Get it', link: '/guide/get-it' },
      {
        text: 'Project',
        items: [
          { text: 'Licence (CC BY 4.0)', link: '/guide/licence' },
          { text: 'Stegobench, the harness that built it', link: 'https://github.com/elementmerc/stegobench' },
        ],
      },
    ],

    sidebar: {
      '/': [
        {
          text: 'Start here',
          items: [
            { text: 'What it is', link: '/guide/what-it-is' },
            { text: 'Get it', link: '/guide/get-it' },
            { text: 'What is in it', link: '/guide/whats-in-it' },
          ],
        },
        {
          text: 'Using it',
          items: [
            { text: 'Loading and splitting', link: '/guide/using-it' },
            { text: 'Licence and attribution', link: '/guide/licence' },
            { text: 'Limitations', link: '/guide/limitations' },
          ],
        },
        {
          text: 'Going further',
          items: [
            { text: 'Rebuilding it yourself', link: '/guide/rebuilding' },
          ],
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/elementmerc/pentimento' },
    ],

    outline: { level: [2, 3], label: 'On this page' },

    footer: {
      message: 'The corpus is published under CC BY 4.0. Each file also carries its own licence.',
      copyright: '© 2026 Daniel Iwugo',
    },

    search: { provider: 'local' },

    docFooter: { prev: 'Previous', next: 'Next' },
  },
}
