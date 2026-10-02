const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../static/js/affiliate-tracking.js'), 'utf8');
function click({dnt, marked = true, href = 'https://vendor.example/offer?ref=private', gtag = true} = {}) {
  let listener;
  const events = [];
  const window = {location: {href: 'https://aiprofreelancer.com/posts/example/',
                            hostname: 'aiprofreelancer.com', pathname: '/posts/example/'}};
  if (gtag) window.gtag = (...args) => events.push(args);
  vm.runInNewContext(source, {window, navigator: {doNotTrack: dnt}, URL,
    document: {addEventListener: (_, callback) => {listener = callback;}}});
  listener({target: {closest: () => marked ? {href} : null}});
  return events;
}
const event = click();
assert.equal(event.length, 1);
assert.equal(event[0][1], 'affiliate_click');
assert.equal(event[0][2].affiliate_domain, 'vendor.example');
assert.ok(!JSON.stringify(event).includes('private'));
assert.equal(click({dnt: '1'}).length, 0);
assert.equal(click({marked: false}).length, 0);
assert.equal(click({gtag: false}).length, 0);
assert.equal(click({href: 'https://aiprofreelancer.com/about/'}).length, 0);
assert.equal(click({href: 'javascript:alert(1)'}).length, 0);
console.log('6 tracking scenarios passed; referral query excluded');
