/* Review/demo convenience gate only. Public static files remain accessible.
 * Change REVIEW_ACCESS_CODE to update the code. Do not use a real password here.
 */
(() => {
  'use strict';
  const REVIEW_ACCESS_CODE = 'VCH-REVIEW';
  const dialog = document.querySelector('#review-notice');
  if (!dialog) return;
  const form = document.querySelector('#review-access-form');
  const input = document.querySelector('#review-access-code');
  const error = document.querySelector('#review-access-error');

  // Show on every homepage visit; no approval or code is stored in the browser.
  dialog.addEventListener('cancel', (event) => event.preventDefault());
  dialog.showModal();
  input.addEventListener('input', () => {
    input.removeAttribute('aria-invalid');
    error.textContent = '';
  });
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (input.value.trim() !== REVIEW_ACCESS_CODE) {
      input.setAttribute('aria-invalid', 'true');
      error.textContent = 'Incorrect access code. Please try again.';
      input.focus();
      input.select();
      return;
    }
    input.value = '';
    dialog.close();
    document.querySelector('#hero-title')?.setAttribute('tabindex', '-1');
    document.querySelector('#hero-title')?.focus({ preventScroll: true });
  });
})();
