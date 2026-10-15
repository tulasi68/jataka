export function onRequest(context) {
 const configured=Boolean(context.env&&context.env.JATAKA_ENGINE_URL);
 return Response.json({app:"Jataka — Guided Setup",prototype:true,chart_display:false,
 calculations_enabled:configured,calculation_status:configured?"unvalidated":"engine_not_configured",
 input_storage:false,message:configured?"Pages can proxy requests to the configured Jataka engine. Results remain unvalidated.":"Python Swiss Ephemeris service is not configured for this Pages deployment. No calculation has been performed."});
}
