export type WorkflowMode = "draft" | "approved" | "published";

export type PublishAction =
  | "publish_post"
  | "update_listing"
  | "reply_to_review"
  | "upload_media";

export interface BusinessConfig {
  business: {
    id: string;
    displayName: string;
    gbpLocationId: string;
    timezone: string;
    locale: string;
  };
  brand: {
    toneOfVoice: string[];
    preferredCtas: string[];
    prohibitedWording: string[];
    targetKeywords: string[];
    terminology: {
      preferred: string[];
      avoided: string[];
    };
    hashtags: string[];
  };
  media: {
    preferredImageStyle: string;
    preferredImageDimensions: {
      width: number;
      height: number;
    };
  };
  posting: {
    preferredFrequency: string;
    autoPostingEnabled: boolean;
    duplicateWindowDays: number;
  };
  reviews: {
    responseStyle: string;
    includeServiceKeywordsWhenNatural: boolean;
  };
}

export interface ApprovalRequest<TDraft> {
  id: string;
  businessId: string;
  locationId: string;
  workflow: string;
  action: PublishAction;
  draft: TDraft;
  status: "needs_review" | "approved" | "rejected";
  createdAt: string;
  reviewedAt?: string;
  reviewer?: string;
  notes?: string;
}

export interface WorkflowResult<TDraft> {
  mode: WorkflowMode;
  businessId: string;
  locationId: string;
  summary: string;
  draft: TDraft;
  approval?: ApprovalRequest<TDraft>;
}
