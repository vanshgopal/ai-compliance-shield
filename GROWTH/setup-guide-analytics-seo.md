# Setup Guide: Analytics, Search Console, Robots, Sitemap (Step-by-Step)

This guide is for non-technical setup. Do it in order — each step unlocks the next.
You'll need a Google account (Gmail).

---

## STEP 1 — Make sure your site is live first
- Open https://vgsr.pythonanywhere.com in your browser.
- If the homepage loads, good. Continue.
- (If the newer pages like /resources are missing, the deploy still needs to run — tell the assistant.)

---

## STEP 2 — Google Search Console (get indexed by Google)
1. Go to https://search.google.com/search-console
2. Sign in with your Google account.
3. Click **"Add property"** → choose **"URL prefix"**.
4. Type exactly: `https://vgsr.pythonanywhere.com` → click **Continue**.
5. Verification method: choose **"HTML tag"** — it shows a small code snippet like `<meta name="google-site-verification" content="XXXX...">`.
6. Copy that whole tag. **Give it to the assistant** to add to your homepage code (deployed next time).
   - OR: PythonAnywhere may allow verification via DNS — but HTML tag is easiest for free tier.
7. Once added and deployed, back in Search Console click **"Verify"**.

### After verification:
- Left menu → **Sitemaps** → enter `sitemap.xml` → **Submit**.
- Left menu → **URL Inspection** → type `https://vgsr.pythonanywhere.com` → click **Request Indexing**.
- Repeat "Request Indexing" for your main pages: /pricing, /features, /how-it-works, /resources, and each blog page.

---

## STEP 3 — Google Analytics 4 (GA4) — see your visitors
1. Go to https://analytics.google.com
2. Sign in → click **"Start measuring"** (or the Admin gear → **Create property**).
3. Property name: `AI Compliance Shield`. Select your country/currency → **Create**.
4. It asks about business — fill quickly, click through.
5. Then it gives you a **"Measurement ID"** like `G-XXXXXXXXXX` and a **web stream**.
6. In that web stream page, copy the **global site tag** snippet — it starts with `<script async src="https://www.googletagmanager.com/gtag/js?id=G-..."></script>`.
7. **Give that snippet to the assistant** to add to every page (deployed next time).
8. After deploy, wait ~24h — GA4 will start showing real visitors.

### How to later see traffic:
- Admin → Reports → **Realtime** (see live visitors now)
- Reports → **Acquisition → Traffic acquisition** (see where visitors come from — Google, direct, etc.)

---

## STEP 4 — Bing Webmaster Tools (bonus, free extra indexing)
1. Go to https://www.bing.com/webmasters
2. Sign in → **Import from Google Search Console** (easiest — one click, brings your site over).
3. If import not available, add site manually with **URL verification** → then submit the sitemap `sitemap.xml`.

---

## STEP 5 — Robots.txt (tells Google what to crawl)
- You want a file at: `https://vgsr.pythonanywhere.com/robots.txt`
- It should look like:
  ```
  User-agent: *
  Allow: /
  Sitemap: https://vgsr.pythonanywhere.com/sitemap.xml
  ```
- If this file does not exist yet, ask the assistant to create it and deploy it.

---

## STEP 6 — Sitemap (already mostly done)
- Your sitemap should list ALL pages: homepage, /pricing, /features, /how-it-works, /get-started, /resources, all blog pages, /privacy-policy, /terms, /refund-policy, /contact, /about.
- This was prepared locally. When the newer pages (/resources, new blog) are deployed, the sitemap must be updated and re-submitted in Search Console.

---

## STEP 7 — Track the important actions (optional but recommended)
Later you may want to count how many people:
- started a scan, finished a scan
- downloaded a free resource (PDF)
- started/finished a payment
This needs the assistant to add "tracking events" to the code. Tell the assistant to add GA4 events for these.

---

## STEP 8 — Lead email setup (so you get notified)
- There is already a `/api/leads` endpoint that captures emails from the resources page.
- Confirm it sends you a notification to `vgsingh09@gmail.com`. If it only stores but doesn't email, tell the assistant to add an email alert.

---

## QUICK RECAP — What to hand to the assistant (deployed next round)
1. The **Search Console HTML verification tag** (from Step 2)
2. The **GA4 tag snippet** (from Step 3)
3. Ask to create/update **robots.txt** and confirm **sitemap** has all pages.
4. Keep a note of your GA4 **Measurement ID** (`G-...`) and your **Search Console property**.

---

> Note: because your site is on PythonAnywhere free plan, every deploy/reload is done via the assistant or the deploy script. You do not need to touch the server directly for any of the above.
