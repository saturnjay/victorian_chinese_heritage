(() => {
  const i18n = window.vchI18n;
  const t = (key) => (i18n ? i18n.t(key) : key);
  const fmt = (message, replacements = {}) => (i18n
    ? i18n.format(message, replacements)
    : Object.entries(replacements).reduce((text, [key, value]) => text.replaceAll(`{${key}}`, String(value)), message));

  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.portal-menu');
  const languageButton = document.querySelector('.language-button');
  const languagePopover = document.querySelector('.language-popover');
  const header = document.querySelector('.portal-header');

  const updateHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 24);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  menuButton?.addEventListener('click', () => {
    const open = menu.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(open));
  });

  languageButton?.addEventListener('click', () => {
    const open = languagePopover.hasAttribute('hidden');
    languagePopover.toggleAttribute('hidden', !open);
    languageButton.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', (event) => {
    if (event.target.closest('.portal-menu a')) {
      menu?.classList.remove('is-open');
      menuButton?.setAttribute('aria-expanded', 'false');
    }
    if (event.target.closest('.language-popover a, .language-popover [data-set-lang]')) {
      languagePopover.hidden = true;
      languageButton?.setAttribute('aria-expanded', 'false');
    } else if (languagePopover && !event.target.closest('.language-wrap')) {
      languagePopover.hidden = true;
      languageButton?.setAttribute('aria-expanded', 'false');
    }
  });

  const cemeteryNameList = document.querySelector('#cemetery-name-list');
  const cemeteryNameSummary = document.querySelector('#cemetery-name-summary');
  const cemeteryRecordList = document.querySelector('#cemetery-record-list');
  const cemeteryRecordSummary = document.querySelector('#cemetery-record-summary');

  const renderCemeteryRecords = ({ scrollToHash = false } = {}) => {
    if ((!cemeteryNameList || !cemeteryNameSummary) && (!cemeteryRecordList || !cemeteryRecordSummary)) return;
    try {
      const records = (window.CEMETERY_RECORDS || []).filter((record) => record.recorded_name.trim());
      if (!records.length) throw new Error('Packaged cemetery data is unavailable');

      if (cemeteryNameList && cemeteryNameSummary) {
        const yearIn = (value) => (value || '').match(/(?:18|19|20)\d{2}/)?.[0];
        const deathYear = (record) => {
          const recordedYears = [...new Set((record.death_date || '').match(/(?:18|19|20)\d{2}/g) || [])];
          if (recordedYears.length === 1) return Number(recordedYears[0]);
          if (recordedYears.length > 1) return null;
          // A few CAFHOV death dates use a two-digit year; their adjacent
          // four-digit record year provides the unambiguous century.
          if (/\d{1,2}\/\d{1,2}\/\d{2}\s*$/.test(record.death_date || '')) {
            return Number(yearIn(record.year_or_date)) || null;
          }
          return null;
        };
        const chronologicalRecords = records
          .map((record, index) => ({
            record,
            recordNumber: index + 1,
            deathYear: deathYear(record),
            sortYear: deathYear(record) ?? (Number(yearIn(record.year_or_date)) || null)
          }))
          .sort((a, b) => {
            if (a.sortYear === null && b.sortYear !== null) return 1;
            if (a.sortYear !== null && b.sortYear === null) return -1;
            return (a.sortYear ?? 0) - (b.sortYear ?? 0)
              || a.record.recorded_name.localeCompare(b.record.recorded_name, 'en');
          });
        const nameFragment = document.createDocumentFragment();
        chronologicalRecords.forEach(({ record, recordNumber, deathYear }) => {
          const item = document.createElement('li');
          const link = document.createElement('a');
          const name = document.createElement('strong');
          link.href = `./cemetery-records.html#record-${recordNumber}`;
          name.textContent = record.recorded_name;
          link.append(name);
          if (record.chinese_characters) {
            const characters = document.createElement('span');
            characters.lang = 'zh';
            characters.textContent = record.chinese_characters;
            link.append(characters);
          }
          if (deathYear !== null) {
            const yearLabel = document.createElement('span');
            yearLabel.className = 'death-year';
            yearLabel.textContent = fmt('d. {year}', { year: deathYear });
            yearLabel.setAttribute('aria-label', fmt('Death year {year}', { year: deathYear }));
            link.append(yearLabel);
          }
          item.append(link);
          nameFragment.append(item);
        });
        cemeteryNameList.replaceChildren(nameFragment);
        const datedCount = chronologicalRecords.filter((entry) => entry.deathYear !== null).length;
        cemeteryNameSummary.textContent = fmt('{count} sourced name records · {dated} with a recorded death year · oldest to latest', {
          count: records.length.toLocaleString(),
          dated: datedCount.toLocaleString()
        });
      }

      if (cemeteryRecordList && cemeteryRecordSummary) {
        const fieldLabels = {
          finding_ids: 'Finding IDs',
          cemetery: 'Cemetery or source',
          recorded_name: 'Recorded name',
          chinese_characters: 'Chinese characters',
          year_or_date: 'Year or date',
          age: 'Age',
          plot_or_location: 'Plot or location',
          origin_or_birthplace: 'Origin or birthplace',
          evidence_basis: 'Evidence basis',
          confidence: 'Confidence',
          source_url: 'Source',
          source_record_url: 'Source record',
          source_file: 'Source file',
          notes: 'Transcription and research notes',
          gender: 'Gender recorded or derived',
          pronunciation: 'Name pronunciation',
          other_names: 'Other names',
          maiden_name: 'Maiden name',
          birth_date: 'Birth date',
          death_date: 'Death date',
          province: 'Province (Chinese)',
          county: 'County (Chinese)',
          district: 'District (Chinese)',
          township: 'Township (Chinese)',
          village: 'Village (Chinese)',
          plot_number: 'Plot number',
          latitude: 'Latitude',
          longitude: 'Longitude',
          photo_1: 'Grave photograph 1',
          photo_2: 'Grave photograph 2',
          photo_3: 'Grave photograph 3',
          community_notes: 'Community-contributed biography',
          related_story_url: 'Related story'
        };
        const detailFragment = document.createDocumentFragment();
        records.forEach((record, index) => {
          const article = document.createElement('article');
          const heading = document.createElement('h2');
          const fields = document.createElement('dl');
          article.className = 'cemetery-record';
          article.id = `record-${index + 1}`;
          heading.textContent = record.chinese_characters
            ? `${record.recorded_name} · ${record.chinese_characters}`
            : record.recorded_name;
          article.append(heading);

          Object.entries(fieldLabels).forEach(([field, label]) => {
            if (!record[field]) return;
            const term = document.createElement('dt');
            const description = document.createElement('dd');
            term.textContent = t(label);
            const isLinkField = field === 'source_url' || field === 'source_record_url' || field === 'related_story_url' || field.startsWith('photo_');
            const url = isLinkField ? (String(record[field]).match(/^https?:\/\//i) ? record[field] : '') : '';
            if (url) {
              const link = document.createElement('a');
              link.href = url;
              link.target = '_blank';
              link.rel = 'noopener noreferrer';
              link.textContent = field.startsWith('photo_')
                ? t('View high-resolution photograph ↗')
                : field === 'related_story_url' ? t('Read the related story ↗') : record[field];
              description.append(link);
            } else if (isLinkField) {
              description.textContent = record[field];
            } else {
              description.textContent = record[field];
            }
            fields.append(term, description);
          });
          article.append(fields);
          detailFragment.append(article);
        });
        cemeteryRecordList.replaceChildren(detailFragment);
        cemeteryRecordSummary.textContent = fmt('{count} complete sourced records', { count: records.length.toLocaleString() });
        if (scrollToHash && window.location.hash) {
          const selectedRecord = document.querySelector(window.location.hash);
          requestAnimationFrame(() => selectedRecord?.scrollIntoView({ block: 'start' }));
        }
      }
    } catch (error) {
      [cemeteryNameSummary, cemeteryRecordSummary].filter(Boolean).forEach((summary) => {
        summary.classList.add('record-error');
        summary.textContent = t('The packaged cemetery records could not be loaded.');
      });
      console.error(error);
    }
  };

  renderCemeteryRecords({ scrollToHash: true });
  window.addEventListener('vch-languagechange', () => renderCemeteryRecords());

  const form = document.querySelector('#contribution-form');
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const subject = `[Victorian Chinese Heritage] ${data.get('submission-type')}: ${data.get('title')}`;
    const body = [
      `${t('Submission type:')} ${data.get('submission-type')}`,
      `${t('Related page or finding:')} ${data.get('related-record') || t('Not supplied')}`,
      `${t('Name:')} ${data.get('name')}`,
      `${t('Email:')} ${data.get('email')}`,
      '',
      data.get('details'),
      '',
      `${t('Evidence or source links:')} ${data.get('sources') || t('Not supplied')}`
    ].join('\n');
    const url = `mailto:cccav.committee@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    const status = document.querySelector('.form-status');
    if (status) status.textContent = t('Your email application is opening with the submission prepared.');
    window.location.href = url;
  });
})();
