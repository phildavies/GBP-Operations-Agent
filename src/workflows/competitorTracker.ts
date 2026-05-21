import type { BusinessConfig, WorkflowResult } from "../core/types";

export interface CompetitorTrackerDraft {
  competitors: string[];
  contentGaps: string[];
  mediaRecommendations: string[];
  postingOpportunities: string[];
}

export async function runCompetitorTrackerWorkflow(
  businessConfig: BusinessConfig
): Promise<WorkflowResult<CompetitorTrackerDraft>> {
  return {
    mode: "draft",
    businessId: businessConfig.business.id,
    locationId: businessConfig.business.gbpLocationId,
    summary: "Competitor tracker placeholder. Connect competitor discovery or manual inputs.",
    draft: {
      competitors: [],
      contentGaps: [],
      mediaRecommendations: [],
      postingOpportunities: []
    }
  };
}
