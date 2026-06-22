import { getAuth, postAuth, putAuth } from './api'

export async function sendInvitation(classroomId: number, correo: string): Promise<{ ok: boolean; data?: any; error?: string }> {
  return postAuth(`/invitations`, { classroom_id: classroomId, correo })
}

export async function getReceivedInvitations(): Promise<{ ok: boolean; data?: any[]; error?: string }> {
  return getAuth(`/invitations/received`)
}

export async function respondInvitation(invitationId: number, status: 'aceptada' | 'rechazada') {
  return putAuth(`/invitations/${invitationId}`, { status })
}
