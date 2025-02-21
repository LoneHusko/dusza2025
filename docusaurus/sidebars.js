const sidebars = {
  mainSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Bevezetés',
    },
    {
      type: 'category',
      label: 'Felhasználói útmutató',
      items: [
        'user-guide/getting-started',
        'user-guide/computer-management',
        'user-guide/program-management',
        'user-guide/process-management',
      ],
    },
    {
      type: 'category',
      label: 'Fejlesztői dokumentáció',
      items: [
        'developer-guide/architecture',
        'developer-guide/installation',
      ],
    },
  ],
};

module.exports = sidebars; 