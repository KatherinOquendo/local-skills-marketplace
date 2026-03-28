---
name: google-maps-integration
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Integrates Google Maps Platform APIs: Maps JavaScript API, markers and
  clustering, geocoding, Places API, and Directions API for location-based
  web applications.
  Trigger: "Google Maps", "maps API", "geocoding", "Places API", "Directions API", "markers"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Google Maps Integration

> "The world is a book, and those who do not travel read only one page." — Saint Augustine

## TL;DR

Integrates Google Maps Platform APIs including Maps JavaScript API, advanced markers, geocoding, Places API, and Directions API for building location-aware web applications with interactive maps. Use this skill when adding maps, location search, address autocomplete, routing, or geospatial features to web applications. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify map requirements: display, interaction, search, routing, geofencing
- Determine which Google Maps APIs are needed and their pricing implications
- Review API key restrictions and billing alerts configuration
- Check existing map implementations and library wrappers in the codebase

### Step 2: Analyze
- Select required APIs:
  - **Maps JavaScript API**: interactive map display and interaction
  - **Places API**: address autocomplete, place search, place details
  - **Geocoding API**: address → coordinates and reverse geocoding
  - **Directions API**: route calculation, turn-by-turn, travel times
  - **Distance Matrix API**: travel time/distance between multiple origins/destinations
- Plan marker strategy: individual markers, clustering for density, custom styling
- Design map interaction: info windows, custom overlays, drawing tools
- Estimate API call volume for billing projection

### Step 3: Execute
- Load Maps JavaScript API with async script loading and callback
- Implement map initialization with appropriate center, zoom, and map type
- Create Advanced Markers with custom HTML content and PinElement
- Implement marker clustering using @googlemaps/markerclusterer
- Set up Places Autocomplete with session tokens (billing optimization)
- Implement Geocoding for address resolution with caching
- Build Directions rendering with DirectionsService and DirectionsRenderer
- Configure API key restrictions: HTTP referrers, API restrictions

### Step 4: Validate
- Verify API key is restricted to specific domains and APIs
- Confirm billing alerts are configured to prevent unexpected charges
- Test map performance with expected marker density (cluster if >100 markers)
- Check map is accessible: keyboard navigation, screen reader description

## Quality Criteria

- [ ] API key is restricted by HTTP referrer and specific APIs
- [ ] Billing alerts are configured with monthly budget caps
- [ ] Places Autocomplete uses session tokens to minimize costs
- [ ] Maps are responsive and usable on mobile devices
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Unrestricted API key exposed in client-side code
- Geocoding on every page load instead of caching results
- Loading all Places API fields when only name and geometry are needed

## Related Skills

- `vanilla-javascript` — Maps API integration without framework wrappers
- `responsive-design` — responsive map containers and mobile interaction
- `performance-architecture` — lazy loading maps for page performance

## Usage

Example invocations: [EXPLICIT]

- "/google-maps-integration" — Run the full google maps integration workflow
- "google maps integration on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
