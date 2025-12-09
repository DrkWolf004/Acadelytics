// API Service para conectar con Backend Flask
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Funciones auxiliares
const getToken = () => localStorage.getItem('token');
const setToken = (token) => localStorage.setItem('token', token);
const removeToken = () => localStorage.removeItem('token');

// Configurar headers con token
const getHeaders = (includeAuth = true) => {
  const headers = {
    'Content-Type': 'application/json',
  };
  if (includeAuth) {
    const token = getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return headers;
};

// Función de petición genérica
const apiCall = async (endpoint, method = 'GET', body = null, includeAuth = true) => {
  try {
    const options = {
      method,
      headers: getHeaders(includeAuth),
    };
    if (body) {
      options.body = JSON.stringify(body);
    }
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `Error ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// ============ AUTH ENDPOINTS ============
export const authAPI = {
  login: (correo, password) =>
    apiCall('/auth/login', 'POST', { correo, password }, false),
  
  register: (nombre, apellidos, correo, password) =>
    apiCall('/auth/register', 'POST', { nombre, apellidos, correo, password }, false),
  
  logout: () => {
    removeToken();
    return Promise.resolve();
  },
};

// ============ USER ENDPOINTS ============
export const userAPI = {
  getUsers: () => apiCall('/users/', 'GET'),
  
  getUser: (id) => apiCall(`/users/detail/?id=${id}`, 'GET'),
  
  updateUser: (id, body) =>
    apiCall(`/users/detail/?id=${id}`, 'PATCH', body),
  
  deleteUser: (id) => apiCall(`/users/detail/?id=${id}`, 'DELETE'),
};

// ============ CLASSROOM ENDPOINTS ============
export const classroomAPI = {
  getClassrooms: () => apiCall('/classrooms/', 'GET'),
  
  getClassroom: (id) => apiCall(`/classrooms/detail/?id=${id}`, 'GET'),
  
  createClassroom: (nombre, member_id) =>
    apiCall('/classrooms/', 'POST', { nombre, member_id }),
  
  updateClassroom: (id, body) =>
    apiCall(`/classrooms/detail/?id=${id}`, 'PATCH', body),
  
  deleteClassroom: (id) => apiCall(`/classrooms/detail/?id=${id}`, 'DELETE'),
};

// ============ CLASSFOLDER ENDPOINTS ============
export const classFolderAPI = {
  getClassFolders: () => apiCall('/classfolders/', 'GET'),
  
  getClassFolder: (id) => apiCall(`/classfolders/detail/?id=${id}`, 'GET'),
  
  createClassFolder: (classroom_id) =>
    apiCall('/classfolders/', 'POST', { classroom_id }),
  
  updateClassFolder: (id, body) =>
    apiCall(`/classfolders/detail/?id=${id}`, 'PATCH', body),
  
  deleteClassFolder: (id) => apiCall(`/classfolders/detail/?id=${id}`, 'DELETE'),
};

// ============ FILE ENDPOINTS ============
export const fileAPI = {
  getFiles: () => apiCall('/files/', 'GET'),
  
  getFile: (id) => apiCall(`/files/detail/?id=${id}`, 'GET'),
  
  uploadFile: (classroom_id, nombreArchivo, file) => {
    const formData = new FormData();
    formData.append('classroom_id', classroom_id);
    formData.append('nombreArchivo', nombreArchivo);
    formData.append('file', file);
    
    const token = getToken();
    const headers = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return fetch(`${API_BASE_URL}/files/`, {
      method: 'POST',
      headers,
      body: formData,
    }).then(res => res.json());
  },
  
  deleteFile: (id) => apiCall(`/files/detail/?id=${id}`, 'DELETE'),
};

export { setToken, getToken, removeToken };
