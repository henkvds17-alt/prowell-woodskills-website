# Prowell WoodSkills — landing page

Static one-page site (no build step), same setup as `The Woodworking Guy/twg.site`.

- Edit `index.html` — all content (workshops, holiday dates, FAQ, contact) lives in the
  EASILY-EDITABLE CONTENT block at the top of the `<script>`.
- Images live in `images/` (relative paths, never base64).
- Deploy: `git add . && git commit -m "..." && git push` → GitHub → Vercel auto-deploys.
- Bookings stay on Wix (prowellwoodskills.co.za). Holiday dates: update `SESSIONS` to match
  the Wix calendar. Remove `SAMPLE_SESSIONS` + the mockup toggle before launch.

## Meta Pixel
- Pixel 975273788505595 (Wix Website Pixel, PWS portfolio) is in every page head + a click-event script at the end of each page (InitiateCheckout = Wix booking click, Lead = email date request, Contact = WhatsApp/phone). If you re-run _gen_workshop_pages.py, check the click-event script is still at the end of the three Read more pages.
