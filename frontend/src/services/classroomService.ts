import type { Classroom, ClassroomMember } from '../types'
import { deleteAuth, getAuth, postAuth, putAuth } from './api'

export async function getUserClassrooms(): Promise<{ ok: boolean; data?: Classroom[]; error?: string }> {
  return getAuth<Classroom[]>('/classrooms')
}

export async function getClassroomMembers(classroomId: number): Promise<{ ok: boolean; data?: ClassroomMember[]; error?: string }> {
  return getAuth<ClassroomMember[]>(`/classrooms/${classroomId}/members`)
}

export async function addClassroomMember(
  classroomId: number,
  correos: string | string[],
): Promise<{ ok: boolean; data?: { id: number; classroom_id: number; student_id: number }; error?: string }> {
  const payload = Array.isArray(correos)
    ? { correos }
    : { correo: correos }

  return postAuth(`/classrooms/${classroomId}/members`, payload)
}

export async function createClassroom(payload: { nombre: string; type: string }): Promise<{ ok: boolean; data?: Classroom; error?: string }> {
  return postAuth('/classrooms', payload)
}

export async function updateClassroom(classroomId: number, payload: { nombre?: string; type?: string }): Promise<{ ok: boolean; data?: Classroom; error?: string }> {
  return putAuth(`/classrooms/${classroomId}`, payload)
}

export async function deleteClassroom(classroomId: number): Promise<{ ok: boolean; data?: unknown; error?: string }> {
  return deleteAuth<unknown>(`/classrooms/${classroomId}`)
}
