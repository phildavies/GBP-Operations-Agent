import { createApprovalRequest } from "../core/approval";
import type { BusinessConfig, WorkflowResult } from "../core/types";
import type { SheetPostInput } from "../integrations/google-sheets/client";

export interface PostDraft {
  postType: "event" | "offer" | "update";
  headline: string;
  body: string;
  cta: string;
  imageSuggestion?: string;
  duplicateCheck: "pending" | "clear" | "possible_duplicate";
}

export async function runEventCreatorWorkflow(
  businessConfig: BusinessConfig,
  input: SheetPostInput
): Promise<WorkflowResult<PostDraft>> {
  const draft: PostDraft = {
    postType: input.postType,
    headline: input.title,
    body: input.description ?? "",
    cta: input.cta ?? businessConfig.brand.preferredCtas[0] ?? "Learn more",
    imageSuggestion: input.imageUrl,
    duplicateCheck: "pending"
  };

  return {
    mode: "draft",
    businessId: businessConfig.business.id,
    locationId: businessConfig.business.gbpLocationId,
    summary: "Post draft created and queued for approval.",
    draft,
    approval: createApprovalRequest({
      businessId: businessConfig.business.id,
      locationId: businessConfig.business.gbpLocationId,
      workflow: "gbp-event-creator",
      action: "publish_post",
      draft
    })
  };
}
