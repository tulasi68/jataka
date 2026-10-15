export function onRequest() {
  return Response.json({
    app: "Jataka — Guided Setup",
    prototype: true,
    chart_display: false,
    calculations_enabled: false,
    input_storage: false,
    message: "Guided input prototype only; no horoscope calculation has been performed."
  });
}
