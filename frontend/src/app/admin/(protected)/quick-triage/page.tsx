import { Metadata } from 'next';
import QuickTriageClient from './QuickTriageClient';

export const metadata: Metadata = {
  title: 'Quick Triage | HealthAICare Admin',
  description: 'Create and triage clinical cases with automatic SLA calculation and counselor assignment',
};

export default function QuickTriagePage() {
  return <QuickTriageClient />;
}
