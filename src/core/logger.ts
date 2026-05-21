export interface ActionLogEvent {
  eventId: string;
  timestamp: string;
  businessId: string;
  locationId: string;
  workflow: string;
  mode: string;
  status: string;
  summary: string;
}

export function createActionLogEvent(
  event: Omit<ActionLogEvent, "eventId" | "timestamp">
): ActionLogEvent {
  return {
    eventId: crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    ...event
  };
}
