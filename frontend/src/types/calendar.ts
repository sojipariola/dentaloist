// src/types/calendar.ts
export interface CalendarEvent {
  id: number;
  title: string;
  description?: string;
  type: EventType;
  start: Date;
  end: Date;
  allDay: boolean;
  location?: string;
  organizerId: number;
  attendees: Attendee[];
  recurrence?: RecurrenceRule;
  reminders: Reminder[];
  status: EventStatus;
  color?: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  organizer?: User;
}

export interface Attendee {
  userId: number;
  status: AttendeeStatus;
  role: AttendeeRole;
  responseDate?: Date;
  user?: User;
}

export interface RecurrenceRule {
  frequency: RecurrenceFrequency;
  interval: number;
  count?: number;
  until?: Date;
  byDay?: number[];
  byMonth?: number[];
  bySetPos?: number[];
}

export interface Reminder {
  type: ReminderType;
  minutes: number;
  sent: boolean;
}

export interface CalendarView {
  date: Date;
  viewType: ViewType;
  events: CalendarEvent[];
  availability: AvailabilitySlot[];
}

export interface AvailabilitySlot {
  start: Date;
  end: Date;
  available: boolean;
  reason?: string;
}

export enum EventType {
  APPOINTMENT = 'appointment',
  MEETING = 'meeting',
  TASK = 'task',
  REMINDER = 'reminder',
  HOLIDAY = 'holiday',
  OUT_OF_OFFICE = 'out_of_office'
}

export enum EventStatus {
  CONFIRMED = 'confirmed',
  TENTATIVE = 'tentative',
  CANCELLED = 'cancelled'
}

export enum AttendeeStatus {
  ACCEPTED = 'accepted',
  DECLINED = 'declined',
  TENTATIVE = 'tentative',
  NEEDS_ACTION = 'needs_action'
}

export enum AttendeeRole {
  REQUIRED = 'required',
  OPTIONAL = 'optional',
  RESOURCE = 'resource'
}

export enum RecurrenceFrequency {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  YEARLY = 'yearly'
}

export enum ReminderType {
  EMAIL = 'email',
  SMS = 'sms',
  PUSH = 'push',
  POPUP = 'popup'
}

export enum ViewType {
  DAY = 'day',
  WEEK = 'week',
  MONTH = 'month',
  AGENDA = 'agenda'
}