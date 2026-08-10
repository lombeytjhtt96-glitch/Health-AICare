const getApiBaseUrl = () => {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== "undefined") return "/api/v1";
  return "http://localhost:8000/api/v1";
};

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${getApiBaseUrl()}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "API Request Failed" }));
    throw new Error(errorData.detail || `HTTP Error ${response.status}`);
  }

  return response.json();
}

export const api = {
  // Chat
  sendChatMessage: (data: { message: string; session_id: string; user_id?: number; user_role?: string }) =>
    fetchApi<any>("/chat/message", { method: "POST", body: JSON.stringify(data) }),

  getChatHistory: (sessionId: string) =>
    fetchApi<any>(`/chat/history/${sessionId}`),

  // Journaling
  createJournal: (data: { user_id: number; content: string; mood?: number }) =>
    fetchApi<any>("/journal", { method: "POST", body: JSON.stringify(data) }),

  getUserJournals: (userId: number) =>
    fetchApi<any[]>(`/journal/${userId}`),

  // Quests
  getUserQuests: (userId: number) =>
    fetchApi<any[]>(`/quests/${userId}`),

  completeQuest: (userId: number, questInstanceId: number) =>
    fetchApi<any>("/quests/complete", { method: "POST", body: JSON.stringify({ user_id: userId, quest_instance_id: questInstanceId }) }),

  // Proof Timeline
  getProofAttestations: () =>
    fetchApi<any[]>("/proof/attestations"),

  // Counselor Cases
  getCounselorCases: () =>
    fetchApi<any[]>("/counselor/cases"),

  claimCase: (caseId: string, counselorId: string) =>
    fetchApi<any>(`/counselor/cases/${caseId}/claim`, { method: "POST", body: JSON.stringify({ counselor_id: counselorId }) }),

  // Admin Autopilot Queue
  getAutopilotQueue: () =>
    fetchApi<any[]>("/admin/autopilot/queue"),

  approveAutopilotAction: (actionId: number, adminId: number = 1) =>
    fetchApi<any>(`/admin/autopilot/${actionId}/approve`, { method: "POST", body: JSON.stringify({ admin_id: adminId }) }),

  rejectAutopilotAction: (actionId: number, adminId: number = 1) =>
    fetchApi<any>(`/admin/autopilot/${actionId}/reject`, { method: "POST", body: JSON.stringify({ admin_id: adminId }) }),
};
