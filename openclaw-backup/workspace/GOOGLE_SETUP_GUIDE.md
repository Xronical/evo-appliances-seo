# Evo Appliances - Google Cloud Setup Guide

## Step 1: Find Your GA4 Property ID

1. Go to https://analytics.google.com
2. Select your Evo Appliances property
3. Click **Admin** (bottom left)
4. In the Property column, click **Property Settings**
5. Copy the **Property ID** (looks like `123456789`)
6. Send it to me

---

## Step 2: Create Google Cloud Service Account

### 2.1 Go to Google Cloud Console
1. Visit https://console.cloud.google.com
2. Sign in with the same Google account as GA4/Search Console
3. Select or create a project (top left dropdown)

### 2.2 Enable Required APIs
1. Go to **APIs & Services** → **Library**
2. Search and enable these APIs:
   - ✅ **Google Analytics Data API** (for GA4)
   - ✅ **Google Search Console API** (for Search Console)
   - ✅ **PageSpeed Insights API** (optional, already have API key)

### 2.3 Create Service Account
1. Go to **IAM & Admin** → **Service Accounts**
2. Click **+ CREATE SERVICE ACCOUNT**
3. **Service account name**: `evo-appliances-seo`
4. **Description**: `SEO automation for Evo Appliances`
5. Click **CREATE AND CONTINUE**
6. **Grant roles**: Select **Viewer** (or **Analytics Viewer** + **Search Console Viewer**)
7. Click **CONTINUE** → **DONE**

### 2.4 Create JSON Key
1. Find your service account in the list
2. Click the three dots → **Manage keys**
3. Click **ADD KEY** → **Create new key**
4. Select **JSON**
5. Click **CREATE**
6. A `.json` file downloads automatically - **SAVE IT SECURELY**

### 2.5 Share the Key with Me
Send the contents of the downloaded JSON file (it starts with `{"type": "service_account",...}`)

---

## Step 3: Add Service Account to GA4

1. Go to https://analytics.google.com
2. Click **Admin** (bottom left)
3. In the Property column, click **Property Access Management**
4. Click **+** → **Add users**
5. **Email address**: Paste the service account email (from the JSON, looks like `evo-appliances-seo@project-id.iam.gserviceaccount.com`)
6. **Roles**: Select **Viewer** or **Analyst**
7. Click **Add**

---

## Step 4: Add Service Account to Search Console

### 4.1 Add Site to Search Console (if not done)
1. Go to https://search.google.com/search-console
2. Click **Add property**
3. Select **Domain** (recommended) or **URL prefix**
4. Enter `evoappliances.ca`
5. Verify ownership (via DNS or HTML tag)

### 4.2 Grant Service Account Access
1. In Search Console, select your property
2. Click **Settings** (gear icon) → **Users and permissions**
3. Click **ADD USER**
4. **Email address**: Paste the service account email
5. **Permission**: Select **Full** or **Restricted**
6. Click **ADD**

---

## Summary Checklist

- [ ] GA4 Property ID copied
- [ ] Google Cloud project created/selected
- [ ] APIs enabled (Analytics Data API + Search Console API)
- [ ] Service account created
- [ ] JSON key downloaded
- [ ] Service account added to GA4
- [ ] Service account added to Search Console
- [ ] evoappliances.ca verified in Search Console
- [ ] JSON file contents sent to me

---

## What I'll Do With This

Once you send me:
1. GA4 Property ID
2. Service account JSON

I'll configure:
- ✅ Automated GA4 data pulls (traffic, conversions, landing pages)
- ✅ Search Console query analysis (rankings, CTR, impressions)
- ✅ Weekly SEO reports
- ✅ Page performance tracking
- ✅ Content opportunity identification

---

## Questions?

Stuck on any step? Send me a screenshot or describe where you are. I'll guide you through.
