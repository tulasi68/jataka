# Hosting the Jataka calculation API

The browser interface stays on Cloudflare Pages. The calculation engine is a separate
Python service because the native `pyswisseph` package cannot be assumed to run in a
Cloudflare Pages JavaScript function.

## Deploy the API on Render (free web service)

1. Sign in to Render and choose **New → Blueprint** (or create a Web Service from the
   `tulasi68/jataka` GitHub repository).
2. Select this repository and branch `main` after these changes are merged.
3. Render should detect `render.yaml`; review the service named `jataka-engine`.
4. Set the service's `JATAKA_ENGINE_TOKEN` environment variable to a long random secret.
   Use a password manager to generate it. Do not commit it to GitHub or send it in chat.
5. Deploy. The first build can take several minutes. Free services may sleep when idle and
   take a little time to wake up.
6. Copy the service's public HTTPS base URL (for example, `https://your-service.onrender.com`).
   Do not add `/api/calculate` to the base URL.

## Connect the service to Cloudflare Pages

In Cloudflare Dashboard:

1. Open **Workers & Pages → jataka → Settings → Variables and Secrets** (wording may vary).
2. Add `JATAKA_ENGINE_URL` as a production environment variable with the Render HTTPS base URL.
3. Add `JATAKA_ENGINE_TOKEN` as a **secret**, using exactly the same random secret configured on Render.
4. Save and trigger a new production deployment so the Pages function receives the new values.

## Verify

- Open `https://your-service.onrender.com/health`. It should return JSON with `"status":"ok"`.
- Open `https://jataka.pages.dev/api/status` to inspect the site status.
- Submit test birth details on the site. The API should return raw positions marked
  **UNVALIDATED**, not a chart or interpretation.
- Try once after the service has been idle; the free service may need to wake up.

The token prevents arbitrary callers from using the Python calculation endpoint without the
Pages secret. Keep the token private. This is not a promise that the hosting provider keeps
request metadata or logs no matter what; review the provider's logging and privacy terms.
Birth details are not written to application storage by this code, but are sent over HTTPS
to the calculation service for processing.

## Important limitations

- Free hosting can sleep, impose usage limits, or change its free-tier terms.
- This only connects the first Swiss Ephemeris numerical pass. It does **not** complete
  reference-chart validation or the remaining Jaimini/Ashtakavarga/consensus modules.
- All results must remain labelled unvalidated until checked against independent, trusted
  reference charts and documented conventions.
