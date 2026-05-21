import type { ApprovalRequest, PublishAction } from "./types";

export function createApprovalRequest<TDraft>(input: {
  businessId: string;
  locationId: string;
  workflow: string;
  action: PublishAction;
  draft: TDraft;
}): ApprovalRequest<TDraft> {
  return {
    id: crypto.randomUUID(),
    businessId: input.businessId,
    locationId: input.locationId,
    workflow: input.workflow,
    action: input.action,
    draft: input.draft,
    status: "needs_review",
    createdAt: new Date().toISOString()
  };
}

export function assertApproved<TDraft>(request: ApprovalRequest<TDraft>): void {
  if (request.status !== "approved") {
    throw new Error(`Approval required before ${request.action}`);
  }
}
