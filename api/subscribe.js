// Holiday list sign-up: adds the visitor to the Wix contact list with the
// "PWS Holiday list" label (the master list Henk's emails go to).
// Needs Vercel env vars: WIX_API_KEY (Wix API key with Contacts permissions), WIX_SITE_ID.
const LABEL = 'custom.pws-holiday-list-oGDsm';
const WIX = 'https://www.wixapis.com/contacts/v4/contacts';

async function wix(path, body) {
  const r = await fetch(WIX + path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: process.env.WIX_API_KEY,
      'wix-site-id': process.env.WIX_SITE_ID,
    },
    body: JSON.stringify(body),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`Wix ${path || '/'} ${r.status}: ${JSON.stringify(data).slice(0, 300)}`);
  return data;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.website) return res.status(200).json({ ok: true }); // honeypot: bots fill this hidden field
  const email = String(b.email || '').trim().toLowerCase();
  const first = String(b.first || '').trim().slice(0, 60);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.includes('..'))
    return res.status(400).json({ ok: false, error: 'email' });
  if (!process.env.WIX_API_KEY || !process.env.WIX_SITE_ID)
    return res.status(500).json({ ok: false, error: 'not configured' });
  try {
    const q = await wix('/query', { query: { filter: { 'info.emails.email': email } } });
    const found = (q.contacts || [])[0];
    if (found) {
      // existing contact: just add the label, never overwrite the name Henk already has
      await wix(`/${found.id}/labels`, { labelKeys: [LABEL] });
    } else {
      const info = { emails: { items: [{ email, tag: 'MAIN' }] }, labelKeys: { items: [LABEL] } };
      if (first) info.name = { first };
      await wix('', { info });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error(e.message);
    return res.status(502).json({ ok: false, error: 'wix' });
  }
};
