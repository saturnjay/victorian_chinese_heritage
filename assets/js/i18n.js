/* Shared interface-language runtime for the Victorian Chinese Heritage portal.
 * English is the canonical source text in the HTML; the Simplified and
 * Traditional Chinese catalogues (i18n-zh-hans.js, i18n-zh-hant.js) are
 * applied on top. The language choice is remembered per browser and mirrored
 * in the ?lang= query parameter so it can be shared as a link.
 *
 * The header language popover (the existing EN / 中文 switch button) contains
 * buttons marked data-set-lang; clicking one switches the whole page in place.
 * Dynamic content built by portal.js calls window.vchI18n.t() / .format() and
 * listens for the vch-languagechange event to re-render.
 */
(() => {
  'use strict';
  const emptyCatalog = { text: {}, attributes: {}, values: {} };
  const languageCatalogs = {
    'zh-Hans': window.VCH_I18N || emptyCatalog,
    'zh-Hant': window.VCH_I18N_ZH_HANT || emptyCatalog
  };
  const reverseCatalogs = Object.fromEntries(Object.entries(languageCatalogs).map(([language, catalog]) => {
    const reverse = {};
    Object.entries({ ...catalog.text, ...catalog.attributes, ...catalog.values })
      .forEach(([english, translated]) => {
        if (!(translated in reverse)) reverse[translated] = english;
        else if (reverse[translated] !== english) reverse[translated] = null;
      });
    return [language, reverse];
  }));
  const supportedLanguages = new Set(['en', 'zh-Hans', 'zh-Hant']);
  const originalText = new WeakMap();
  const originalAttributes = new WeakMap();
  const originalDocumentTitle = document.title;
  const descriptionElement = document.querySelector('meta[name="description"]');
  const originalDescription = descriptionElement?.content || '';

  let currentLanguage = (() => {
    try {
      const requested = new URL(window.location.href).searchParams.get('lang');
      if (supportedLanguages.has(requested)) return requested;
      const saved = window.localStorage.getItem('vch-language');
      if (supportedLanguages.has(saved)) return saved;
    } catch (error) {
      // Local files can restrict URL or storage access; English remains the safe default.
    }
    return 'en';
  })();

  const canonicalEnglish = (value) => {
    const text = String(value ?? '');
    for (const reverseCatalog of Object.values(reverseCatalogs)) {
      if (reverseCatalog[text]) return reverseCatalog[text];
    }
    return text;
  };

  const translateExact = (value, language = currentLanguage) => {
    const english = canonicalEnglish(value);
    if (language === 'en') return english;
    const catalog = languageCatalogs[language] || emptyCatalog;
    return catalog.text?.[english] || catalog.attributes?.[english] || catalog.values?.[english] || english;
  };

  const formatMessage = (message, replacements = {}) => Object.entries(replacements)
    .reduce((translated, [key, value]) => translated.replaceAll(`{${key}}`, String(value)), translateExact(message));

  const localizeTree = (root = document) => {
    const nodeRoot = root.nodeType === Node.TEXT_NODE ? root.parentElement : root;
    if (nodeRoot instanceof Element && nodeRoot.closest('[data-no-i18n]')) return;

    const translateTextNode = (node) => {
      if (!node.parentElement || node.parentElement.closest('[data-no-i18n], script, style')) return;
      const match = node.nodeValue.match(/^(\s*)([\s\S]*?)(\s*)$/);
      if (!match || !match[2]) return;
      if (!originalText.has(node)) originalText.set(node, canonicalEnglish(match[2]));
      const translated = translateExact(originalText.get(node));
      node.nodeValue = match[1] + translated + match[3];
    };

    if (root.nodeType === Node.TEXT_NODE) translateTextNode(root);
    else {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) translateTextNode(node);
    }

    const attributeNames = ['aria-label', 'placeholder', 'alt', 'title'];
    const elementsToTranslate = root instanceof Element
      ? [root, ...root.querySelectorAll('*')]
      : [...document.querySelectorAll('*')];
    elementsToTranslate.forEach((element) => {
      if (element.closest('[data-no-i18n]')) return;
      attributeNames.forEach((attribute) => {
        if (!element.hasAttribute(attribute)) return;
        let originals = originalAttributes.get(element);
        if (!originals) {
          originals = new Map();
          originalAttributes.set(element, originals);
        }
        if (!originals.has(attribute)) {
          originals.set(attribute, canonicalEnglish(element.getAttribute(attribute)));
        }
        const original = originals.get(attribute);
        const translated = translateExact(original);
        element.setAttribute(attribute, translated);
      });
    });

    document.documentElement.lang = currentLanguage;
    document.title = translateExact(originalDocumentTitle);
    if (descriptionElement) descriptionElement.content = translateExact(originalDescription);
  };

  const updateLanguageControls = () => {
    document.querySelectorAll('[data-set-lang]').forEach((control) => {
      control.setAttribute('aria-pressed', String(control.dataset.setLang === currentLanguage));
    });
  };

  const persistLanguage = () => {
    try {
      window.localStorage.setItem('vch-language', currentLanguage);
      const url = new URL(window.location.href);
      if (currentLanguage === 'en') url.searchParams.delete('lang');
      else url.searchParams.set('lang', currentLanguage);
      window.history.replaceState(null, '', `${url.pathname}${url.search}${url.hash}`);
    } catch (error) {
      // Local files can restrict URL or storage access; the in-page switch still works.
    }
  };

  const setLanguage = (language) => {
    if (!supportedLanguages.has(language) || language === currentLanguage) return;
    currentLanguage = language;
    persistLanguage();
    localizeTree();
    updateLanguageControls();
    window.dispatchEvent(new CustomEvent('vch-languagechange', { detail: { language } }));
  };

  document.querySelectorAll('[data-set-lang]').forEach((control) => {
    control.addEventListener('click', (event) => {
      event.preventDefault();
      setLanguage(control.dataset.setLang);
      const popover = control.closest('.language-popover');
      popover?.setAttribute('hidden', '');
      popover?.parentElement?.querySelector('.language-button')?.setAttribute('aria-expanded', 'false');
    });
  });

  window.vchI18n = {
    get language() { return currentLanguage; },
    setLanguage,
    t: (key) => translateExact(key),
    format: formatMessage,
    localize: (root) => localizeTree(root)
  };

  localizeTree();
  updateLanguageControls();
})();
