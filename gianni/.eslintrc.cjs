module.exports = {
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  plugins: ['only-warn'],
  extends: 'airbnb',
  parser: '@babel/eslint-parser',
  parserOptions: {
    requireConfigFile: false,
  },
  rules: {
    'no-param-reassign': 'off',
    'import/prefer-default-export': 'off',
    'padded-blocks': 'off',
    'no-multiple-empty-lines': 'off',
    'no-floating-decimal': 'off',
    eqeqeq: 'off',
    camelcase: 'off',
    'comma-dangle': ['error', 'always-multiline'],
    'one-var': 'off',
    'arrow-parens': ['error', 'as-needed', { requireForBlockBody: true }],
    'no-console': 'off',
    'import/no-dynamic-require': 'off',
    'global-require': 'off',
    'no-plusplus': 'off',
    'no-restricted-syntax': 'off',
    'no-continue': 'off',
    'import/extensions': 'off',
    'no-labels': 'off',
    'max-len': 'off',
    'no-loop-func': 'off',
  },

  globals: {

    // Bannerboy
    BBTimeline: true,
    bannerboy: true,
    bb: true,
    scrubber: true,

    // Greensock
    gsap: true,
    TweenLite: true,
    TweenMax: true,
    TimelineLite: true,
    TimelineMax: true,
    CSSPlugin: true,
    Linear: true,
    Power0: true,
    Power1: true,
    Power2: true,
    Power3: true,
    Power4: true,
    Back: true,
    Sine: true,
    Elastic: true,
    Draggable: true,
    Expo: true,

    // DC
    Enabler: true,
    studioinnovation: true,
    studio: true,

    // Adform
    dhtml: true,
    Adform: true,

    // Sizmek
    EB: true,
    EBG: true,

    // Other
    PIXI: true,
    GSDevTools: true,
    Stats: true,
    THREE: true,
    $: true,
    screenad: true,
    YT: true,
    createjs: true,
    PerspectiveTransform: true,
    FontFaceObserver: true,

    // Webpack build
    __EXECUTION__: true,
    __BLUEPRINT__: true,
    __WIDTH__: true,
    __HEIGHT__: true,
    __NAME__: true,
    __FONTS__: true,
    __COPY__: true,
    __DEV__: true,
    __COPY_PATCH_KEYS__: true,
    __STYLE_PATCH_FILEPATH__: true,
    __COPY_PATCH_FILEPATH__: true,
  },
};
