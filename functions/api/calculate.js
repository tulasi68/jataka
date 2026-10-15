/** Proxy to separately hosted Python/Swiss Ephemeris API. Set JATAKA_ENGINE_URL to its base URL. */
export async function onRequestPost(context) {
 const base=context.env&&context.env.JATAKA_ENGINE_URL;
 if(!base)return Response.json({detail:"Calculation engine is not connected to this hosted site yet. Deploy the Python Swiss Ephemeris API and configure JATAKA_ENGINE_URL. No calculation was performed."},{status:503});
 let incoming;try{incoming=await context.request.json()}catch{return Response.json({detail:"Request body must be valid JSON."},{status:400})}
 try{const upstream=await fetch(new URL("/api/calculate",base),{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(incoming)});
 return new Response(await upstream.text(),{status:upstream.status,headers:{"Content-Type":upstream.headers.get("Content-Type")||"application/json","Cache-Control":"no-store"}})}
 catch{return Response.json({detail:"Calculation service could not be reached. No calculation was performed."},{status:502})}
}
