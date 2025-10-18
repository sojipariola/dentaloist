// src/types/clinical-trials.ts
export interface ClinicalTrial {
  id: number;
  title: string;
  description: string;
  phase: TrialPhase;
  status: TrialStatus;
  conditions: string[];
  interventions: Intervention[];
  criteria: EligibilityCriteria;
  timeline: TrialTimeline;
  sponsors: Sponsor[];
  investigators: Investigator[];
  sites: TrialSite[];
  participants: Participant[];
  results: TrialResults;
  documents: TrialDocument[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Intervention {
  type: InterventionType;
  name: string;
  description: string;
  dosage?: string;
  duration?: string;
}

export interface EligibilityCriteria {
  inclusion: string[];
  exclusion: string[];
  ageRange: AgeRange;
  gender: Gender[];
  healthStatus: string[];
}

export interface TrialTimeline {
  startDate: Date;
  endDate: Date;
  milestones: Milestone[];
  visits: VisitSchedule[];
}

export interface Sponsor {
  name: string;
  type: SponsorType;
  contact: ContactInfo;
}

export interface Investigator {
  id: number;
  role: InvestigatorRole;
  siteId: number;
  user?: User;
}

export interface TrialSite {
  id: number;
  name: string;
  address: Address;
  contact: ContactInfo;
  status: SiteStatus;
}

export interface Participant {
  id: number;
  patientId: number;
  siteId: number;
  status: ParticipantStatus;
  group?: string;
  randomizationDate?: Date;
  completionDate?: Date;
  dropoutReason?: string;
  adverseEvents: AdverseEvent[];
  patient?: Patient;
}

export interface TrialResults {
  primaryOutcomes: OutcomeResult[];
  secondaryOutcomes: OutcomeResult[];
  safetyOutcomes: SafetyResult[];
  statisticalAnalysis: StatisticalAnalysis;
  publications: Publication[];
}

export enum TrialPhase {
  PHASE_1 = 'phase_1',
  PHASE_2 = 'phase_2',
  PHASE_3 = 'phase_3',
  PHASE_4 = 'phase_4'
}

export enum TrialStatus {
  RECRUITING = 'recruiting',
  ACTIVE = 'active',
  COMPLETED = 'completed',
  SUSPENDED = 'suspended',
  TERMINATED = 'terminated'
}

export enum InterventionType {
  DRUG = 'drug',
  DEVICE = 'device',
  PROCEDURE = 'procedure',
  BEHAVIORAL = 'behavioral'
}

export enum SponsorType {
  INDUSTRY = 'industry',
  NIH = 'nih',
  OTHER_GOV = 'other_gov',
  OTHER = 'other'
}

export enum InvestigatorRole {
  PRINCIPAL = 'principal',
  SUB_INVESTIGATOR = 'sub_investigator',
  COORDINATOR = 'coordinator'
}

export enum SiteStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended'
}

export enum ParticipantStatus {
  SCREENING = 'screening',
  RANDOMIZED = 'randomized',
  ACTIVE = 'active',
  COMPLETED = 'completed',
  DROPPED_OUT = 'dropped_out'
}