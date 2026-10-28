const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../static/js/affiliate-tracking.js'), 'utf8');
function click({dnt, marked = true, href = 'https://get.murf.ai/issued?sid=private', gtag = true, ratio = 0, article = 'example', inContent = true} = {}) {
  const listeners = [], events = [];
  const window = {location: {href: 'https://aiprofreelancer.com/posts/example/', hostname: 'aiprofreelancer.com'}};
  if (gtag) window.gtag = (...args) => events.push(args);
  const content = {getBoundingClientRect: () => ({top: -300, height: 900})};
  const link = {href, getAttribute: () => article, closest: () => inContent ? content : null,
                getBoundingClientRect: () => ({top: -300 + ratio * 900})};
  vm.runInNewContext(source, {window, navigator: {doNotTrack: dnt}, URL,
    document: {addEventListener: (_, callback) => listeners.push(callback)}});
  listeners.forEach(listener => listener({target: {closest: selector => marked && selector.includes('data-affiliate') ? link : null}}));
  return events;
}
for (const [ratio, position] of [[0,'top'],[0.3334,'middle'],[0.5,'middle'],[0.6667,'bottom'],[1,'bottom']]) {
  const events = click({ratio});
  assert.equal(events.length, 1);
  assert.deepEqual(JSON.parse(JSON.stringify(events[0])), ['event', 'affiliate_click', {
    program: 'murf', article: 'example', position, transport_type: 'beacon'
  }]);
  assert.ok(!JSON.stringify(events).includes('private'));
}
for (const options of [{dnt:'1'},{dnt:'yes'},{marked:false},{gtag:false},{inContent:false},
  {article:'person@example.com'},{href:'https://unknown.example/'},{href:'https://aiprofreelancer.com/'},
  {href:'javascript:alert(1)'}]) assert.equal(click(options).length, 0);
for (const [host, program] of Object.entries({'mangools.com':'mangools','try.elevenlabs.io':'elevenlabs',
  'beautifulai.partnerlinks.io':'beautifulai','ultahost.com':'ultahost','www.hostinger.com':'hostinger'})) {
  assert.equal(click({href:`https://${host}/issued`})[0][2].program,program);
}
console.log('Affiliate tracking: positions, host mapping, privacy, DNT, nested targets and exclusions passed');
