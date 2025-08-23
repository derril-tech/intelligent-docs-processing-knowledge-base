import { BaseEntity } from './common';

export interface User extends BaseEntity {
  email: string;
  username: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  last_login?: string;
  preferences: UserPreferences;
}

export type UserRole = 'admin' | 'user' | 'validator' | 'viewer';

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  notifications: NotificationSettings;
  dashboard_layout?: Record<string, any>;
}

export interface NotificationSettings {
  email: boolean;
  push: boolean;
  processing_updates: boolean;
  validation_requests: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}

export interface RegisterRequest {
  email: string;
  username: string;
  full_name: string;
  password: string;
  confirm_password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

export interface ResetPasswordRequest {
  email: string;
}

export interface ResetPasswordConfirmRequest {
  token: string;
  new_password: string;
  confirm_password: string;
}
