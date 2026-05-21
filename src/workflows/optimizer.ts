import type { BusinessConfig, WorkflowResult } from "../core/types";

export interface OptimizerDraft {
  recommendations: string[];
  missingImages: string[];
  suggestedFaqs: string[];
  suggestedPosts: string[];
}

export async function runOptimizerWorkflow(
  businessConfig: BusinessConfig
): Promise<WorkflowResult<OptimizerDraft>> {
  return {
    mode: "draft",
    businessId: businessConfig.business.id,
    locationId: businessConfig.business.gbpLocationId,
    summary: "Optimizer workflow placeholder. Connect GBP read APIs to generate a full audit.",
    draft: {
      recommendations: [],
      missingImages: [],
      suggestedFaqs: [],
      suggestedPosts: []
    }
  };
}
