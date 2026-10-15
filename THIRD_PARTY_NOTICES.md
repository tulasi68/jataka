# Third-party notices

## Swiss Ephemeris / pyswisseph

Jataka uses the Swiss Ephemeris Python binding (pyswisseph) for astronomical calculations.
Swiss Ephemeris is offered under the GNU Affero General Public License (AGPL) or a
commercial Swiss Ephemeris Professional License. This project selects the AGPL option.
The binding and upstream project are maintained separately from Jataka.

- Upstream source and licence: https://github.com/aloistr/swisseph
- Licensing information: https://www.astro.com/swisseph/sweph_e.htm?lang=s
- Python binding project: https://pypi.org/project/pyswisseph/

Consult the complete upstream licence and preserve all notices when redistributing.
This notice is informational and does not replace the licence texts supplied by upstream.

## Open-Meteo geocoding

The browser prototype uses the public Open-Meteo geocoding API, which uses GeoNames data.
Location search requires an internet connection. Review the provider's current terms and
attribution requirements before operating the service, especially for commercial use.

- API documentation: https://open-meteo.com/en/docs/geocoding-api
- GeoNames: https://www.geonames.org/
- GeoNames data licence: https://creativecommons.org/licenses/by/4.0/


## Ashtakavarga rule-table references

The seven-recipient Bhinna Ashtakavarga benefic-house table is encoded as rule data in Jataka and should be compared against the specific tradition/reference selected for a release. Publicly accessible comparison material includes:

- [B.V. Raman, “The Ashtakavarga System” chapter extract](https://vedastro.org/blog/Hindu-Predictive-Astrology-Chapter-26-The-Ashtakavarga-System.html)
- [Jyotishganit Ashtakavarga implementation and rule table](https://github.com/northtara/jyotishganit/blob/main/jyotishganit/components/ashtakavarga.py)
- [AstroSK Ashtakavarga reference tables](https://docs.astrosk.com/glossary/vedic/ashtakavarga/definition-of-suns-ashtakavarga)

These are comparison sources, not a declaration that all lineages agree. Review upstream licenses before copying implementation code; Jataka stores its own explicit rule data and documents the chosen convention. No third-party implementation code is imported at runtime.
