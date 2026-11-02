// Visual helpers: mark affiliate CTA paragraphs and the opening verdict box.
(function () {
  var root = document.querySelector('.post-single .post-content');
  if (!root) return;
  root.querySelectorAll('a[data-affiliate="true"]').forEach(function (a) {
    var p = a.closest('p');
    if (p && p.parentElement === root && p.textContent.trim() === a.textContent.trim()) p.classList.add('cta');
  });
  var first = root.querySelector(':scope > p');
  if (first && first.children.length === 1 && first.firstElementChild.tagName === 'STRONG' &&
      first.textContent.trim() === first.firstElementChild.textContent.trim() &&
      !first.querySelector('a') && first.textContent.length > 60) {
    first.classList.add('verdict');
  }
})();
