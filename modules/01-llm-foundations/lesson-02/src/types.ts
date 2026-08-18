export type ResponseData = {
  summary?: string | null;
  patientName?: string | null;
  contactInfo?: string | null;
  appointmentType: "checkup" | "follow-up" | "consultation";
  preferredDate?: string | null;
  preferredTime?: string | null;
  missingInformation?: string[] | null;
  readyForAvailabilityCheck: boolean;
};
