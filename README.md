# Prowell WoodSkills — landing page

Static one-page site (no build step), same setup as `The Woodworking Guy/twg.site`.

- Edit `index.html` — all content (workshops, holiday dates, FAQ, contact) lives in the
  EASILY-EDITABLE CONTENT block at the top of the `<script>`.
- Images live in `images/` (relative paths, never base64).
- Deploy: `git add . && git commit -m "..." && git push` → GitHub → Vercel auto-deploys.
- Bookings stay on Wix (prowellwoodskills.co.za). Holiday dates: update `SESSIONS` to match
  the Wix calendar. Remove `SAMPLE_SESSIONS` + the mockup toggle before launch.
