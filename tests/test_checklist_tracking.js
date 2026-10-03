const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../static/js/affiliate-tracking.js'), 'utf8');
function run(href, dnt, available = true) {
  const callbacks = [], events = [];
  const window = {location: {href: 'https://aiprofreelancer.com/posts/guide/', hostname: 'aiprofreelancer.com', pathname: '/posts/guide/'}};
  if (available) window.gtag = (...args) => events.push(args);
  vm.runInNewContext(source, {window, navigator: {doNotTrack: dnt}, URL,
    document: {addEventListener: (_, callback) => callbacks.push(callback)}});
  callbacks.forEach(callback => callback({target: {closest: selector => selector === 'a[href]' ? {href} : null}}));
  return events;
}
const events = run('/downloads/voiceover-evaluation-scorecard.txt?token=private');
assert.equal(events.length, 1);
assert.equal(events[0][1], 'checklist_download_click');
assert.equal(events[0][2].asset_path, '/downloads/voiceover-evaluation-scorecard.txt');
assert.ok(!JSON.stringify(events).includes('private'));
assert.equal(run('/downloads/voiceover-evaluation-scorecard.txt', '1').length, 0);
assert.equal(run('/downloads/voiceover-evaluation-scorecard.txt', undefined, false).length, 0);
assert.equal(run('https://other.example/downloads/template.txt').length, 0);
assert.equal(run('/about/').length, 0);
assert.equal(run('javascript:alert(1)').length, 0);
console.log('Checklist tracking: event, query privacy, DNT and exclusions passed');
