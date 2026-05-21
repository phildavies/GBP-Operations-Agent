import { createApprovalRequest } from "../core/approval";
import type { BusinessConfig, WorkflowResult } from "../core/types";

export interface ReviewReplyDraft {
  reviewId: string;
  reply: string;
  detectedThemes: string[];
  suggestedSeoPhrases: string[];
}

export async function runReviewReplyWorkflow(
  businessConfig: BusinessConfig,
  reviewId: string
): Promise<WorkflowResult<ReviewReplyDraft>> {
  const draft: ReviewReplyDraft = {
    reviewId,
    reply: "",
    detectedThemes: [],
    suggestedSeoPhrases: []
  };

  return {
    mode: "draft",
    businessId: businessConfig.business.id,
    locationId: businessConfig.business.gbpLocationId,
    summary: "Review reply draft placeholder created and queued for approval.",
    draft,
    approval: createApprovalRequest({
      businessId: businessConfig.business.id,
      locationId: businessConfig.business.gbpLocationId,
      workflow: "gbp-review-reply-generator",
      action: "reply_to_review",
      draft
    })
  };
}
