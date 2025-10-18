// src/types/api.ts
export interface APIKey {
  id: number;
  name: string;
  key: string;
  secret: string;
  type: APIKeyType;
  permissions: APIPermission[];
  rateLimit: RateLimit;
  ips: string[];
  domains: string[];
  expiresAt?: Date;
  lastUsed?: Date;
  usage: APIUsage;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface APIPermission {
  resource: string;
  actions: string[];
  conditions?: Condition[];
}

export interface RateLimit {
  requests: number;
  period: number; // seconds
  burst: number;
}

export interface APIUsage {
  total: number;
  today: number;
  thisMonth: number;
  byEndpoint: Record<string, number>;
  byStatus: Record<number, number>;
  byHour: Record<string, number>;
}

export interface APIRequest {
  id: number;
  keyId?: number;
  endpoint: string;
  method: HTTPMethod;
  status: number;
  duration: number;
  ip: string;
  userAgent: string;
  parameters: Record<string, any>;
  headers: Record<string, string>;
  body?: any;
  response?: any;
  error?: string;
  timestamp: Date;
  
  // Relations
  apiKey?: APIKey;
}

export interface APIDocumentation {
  version: string;
  baseUrl: string;
  endpoints: APIEndpoint[];
  schemas: APISchema[];
  examples: APIExample[];
  changelog: ChangeLog[];
}

export interface APIEndpoint {
  path: string;
  method: HTTPMethod;
  description: string;
  parameters: Parameter[];
  responses: Response[];
  authentication: AuthRequirement;
  rateLimit: RateLimit;
}

export interface APISchema {
  name: string;
  type: SchemaType;
  properties: Property[];
  required: string[];
  example: any;
}

export interface APIExample {
  language: string;
  code: string;
  description: string;
}

export interface ChangeLog {
  version: string;
  date: Date;
  changes: Change[];
}

export enum APIKeyType {
  PUBLIC = 'public',
  SECRET = 'secret',
  SESSION = 'session'
}

export enum HTTPMethod {
  GET = 'GET',
  POST = 'POST',
  PUT = 'PUT',
  DELETE = 'DELETE',
  PATCH = 'PATCH',
  HEAD = 'HEAD',
  OPTIONS = 'OPTIONS'
}

export enum SchemaType {
  OBJECT = 'object',
  ARRAY = 'array',
  STRING = 'string',
  NUMBER = 'number',
  BOOLEAN = 'boolean',
  NULL = 'null'
}

export enum AuthRequirement {
  NONE = 'none',
  API_KEY = 'api_key',
  BEARER = 'bearer',
  OAUTH = 'oauth'
}