(function () {
  'use strict';

  function getFileName(url) {
    try {
      return decodeURIComponent(new URL(url, window.location.href).pathname.split('/').pop() || '');
    } catch (e) {
      return '';
    }
  }

  function getExtension(fileName) {
    var match = fileName.match(/\.([^.]+)$/);
    return match ? match[1].toLowerCase() : '';
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[data-download-track]');
    if (!link) return;

    var fileName = getFileName(link.href);
    var fileFormat = link.dataset.format || getExtension(fileName);

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'digital_edition_download', {
        work_id: link.dataset.work || '',
        part_id: link.dataset.part || '',
        language: link.dataset.language || '',
        file_format: fileFormat,
        edition_version: link.dataset.version || '',
        file_name: fileName,
        file_extension: fileFormat,
        link_url: link.href,
        link_text: (link.textContent || '').trim()
      });
    }
  });
})();
