/** Proxy to the separately hosted Python/Swiss Ephemeris API.
 * Configure JATAKA_ENGINE_URL and the matching secret JATAKA_ENGINE_TOKEN in Pages.
 */
export async function onRequestPost(context) {
  const env = context.env || {};
  const base = env.JATAKA_ENGINE_URL;
  const token = env.JATAKA_ENGINE_TOKEN;
  if (!base || !token) {
    return Response.json(
      { detail: "Calculation engine is not fully configured. Set JATAKA_ENGINE_URL and JATAKA_ENGINE_TOKEN. No calculation was performed." },
      { status: 503, headers: { "Cache-Control": "no-store" } }
    );
  }

  let incoming;
  try {
    incoming = await context.request.json();
  } catch {
    return Response.json({ detail: "Request body must be valid JSON." }, { status: 400 });
  }

  try {
    const upstream = await fetch(new URL("/api/calculate", base), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Jataka-Engine-Token": token,
      },
      body: JSON.stringify(incoming),
      signal: AbortSignal.timeout(25000),
    });
    return new Response(await upstream.text(), {
      status: upstream.status,
      headers: {
        "Content-Type": upstream.headers.get("Content-Type") || "application/json",
        "Cache-Control": "no-store",
      },
    });
  } catch {
    return Response.json(
      { detail: "Calculation service could not be reached. No calculation was performed." },
      { status: 502, headers: { "Cache-Control": "no-store" } }
    );
  }
}
