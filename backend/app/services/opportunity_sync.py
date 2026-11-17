import asyncio
from collections.abc import Awaitable, Callable

from supabase import Client

from ..agents.opportunity_agent import extract_opportunity_requirements
from ..schemas.opportunity import OpportunitySourceConfig, RawOpportunity
from ..services.opportunity_normalizer import normalize_opportunity
from ..services.opportunity_persistence import (
    mark_missing_opportunities_inactive,
    opportunity_changed,
    save_opportunity,
)
from ..config import settings
from ..sources.jsearch import fetch_jsearch_jobs

Fetcher = Callable[[OpportunitySourceConfig], Awaitable[list[RawOpportunity]]]

FETCHERS: dict[str, Fetcher] = {
    "jsearch": fetch_jsearch_jobs,
}


async def sync_opportunities(
    client: Client,
    sources: list[OpportunitySourceConfig],
) -> dict:
    """Fetch all configured sources and persist only new or changed jobs."""
    grouped = await asyncio.gather(
        *[_fetch_source(config) for config in sources]
    )
    fetched = sum(len(items) for _, items in grouped)
    saved = 0
    unchanged = 0
    results = []

    for config, opportunities in grouped:
        seen_external_ids = []
        for raw_opportunity in opportunities:
            opportunity = normalize_opportunity(raw_opportunity)
            seen_external_ids.append(opportunity.external_id)
            if not opportunity_changed(client, opportunity):
                save_opportunity(
                    client,
                    opportunity,
                    extracted=None,
                )
                unchanged += 1
                continue
            extracted = extract_opportunity_requirements(opportunity)
            result = save_opportunity(client, opportunity, extracted)
            if result["changed"]:
                saved += 1
                results.append(result)

        mark_missing_opportunities_inactive(
            client,
            source=config.source_key,
            seen_external_ids=seen_external_ids,
        )

    return {
        "fetched": fetched,
        "saved": saved,
        "unchanged": unchanged,
        "opportunities": results,
    }


async def _fetch_source(
    config: OpportunitySourceConfig,
) -> tuple[OpportunitySourceConfig, list[RawOpportunity]]:
    fetcher = FETCHERS.get(config.source.lower())
    if fetcher is None:
        supported = ", ".join(sorted(FETCHERS))
        raise ValueError(f"Unsupported source '{config.source}'. Use: {supported}.")
    return config, await fetcher(config)


def sources_from_environment() -> list[OpportunitySourceConfig]:
    """Build the configured India-focused JSearch source."""
    if not settings.openwebninja_api_key:
        return []
    return [
        OpportunitySourceConfig(
            query=settings.jsearch_query,
            country=settings.jsearch_country,
            num_pages=settings.jsearch_num_pages,
        )
    ]
