// frontend/src/services/reports/types.ts
// src/services/reports/types.ts

export interface Report {
  id: number;
  type: string;
  generated_at: string; // ISO date string
  start_date: string; // ISO date string
  end_date: string; // ISO date string
  data: any; // The structure of this can vary based on report type
}

/* You can expand this file with more specific types or enums as needed */