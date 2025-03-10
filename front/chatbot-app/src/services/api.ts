import axios, { AxiosError } from 'axios';
import { ApiInfo, ChatRequest, ChatResponse, ChatSession } from '../types';

const API_BASE_URL = 'http://localhost:7575';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  },
  timeout: 1000000,
  withCredentials: false,
});

api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      url: response.config.url,
      status: response.status,
      data: response.data,
      headers: response.headers,
    });
    return response;
  },
  (error: AxiosError) => {
    if (error.response) {
      // La requête a été faite et le serveur a répondu avec un code d'état
      // qui ne fait pas partie de la plage 2xx
      console.error('API Error Response:', {
        url: error.config?.url,
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers,
      });
    } else if (error.request) {
      // La requête a été faite mais aucune réponse n'a été reçue
      console.error('API No Response:', {
        url: error.config?.url,
        request: error.request,
        message: 'No response received from server',
      });
    } else {
      // Une erreur s'est produite lors de la configuration de la requête
      console.error('API Request Setup Error:', {
        message: error.message,
        config: error.config,
      });
    }
    return Promise.reject(error);
  }
);

api.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      url: config.url,
      method: config.method,
      data: config.data,
    });
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

export const checkApiConnection = async (): Promise<boolean> => {
  try {
    console.log('Checking API connection...');
    const response = await api.get('/');
    console.log('API connection successful:', response.data);
    return true;
  } catch (error) {
    const axiosError = error as AxiosError;
    console.error('API connection error:', axiosError);
    if (axiosError.message.includes('Network Error')) {
      console.error('Possible CORS issue - Make sure the API allows requests from:', window.location.origin);
    }
    return false;
  }
};

export const getApiInfo = async (): Promise<ApiInfo> => {
  try {
    console.log('Fetching API info...');
    const response = await api.get('/chat/infos');
    console.log('API info received:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching API info:', error);
    throw error;
  }
};

export const initChatSession = async (): Promise<ChatSession> => {
  try {
    console.log('Initializing chat session...');
    const response = await api.post('/chat/init/');
    const session_id = response.data.session_id;
    console.log('Chat session initialized:', session_id);
    
    return {
      session_id,
      name: `Chat ${new Date().toLocaleString()}`,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error('Error initializing chat session:', error);
    throw error;
  }
};

export const sendChatQuery = async (chatRequest: ChatRequest): Promise<ChatResponse> => {
  try {
    console.log('Sending chat query:', chatRequest);
    const response = await api.post('/chat/query', chatRequest);
    console.log('Chat query response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error sending chat query:', error);
    throw error;
  }
};

export const downloadFile = async (sessionId: string, filePath: string): Promise<Blob> => {
  try {
    console.log('Downloading file:', { sessionId, filePath });
    const response = await api.post(
      '/chat/download',
      { session_id: sessionId, file_path: filePath },
      { responseType: 'blob' }
    );
    console.log('File downloaded successfully');
    return response.data;
  } catch (error) {
    console.error('Error downloading file:', error);
    throw error;
  }
};

export default api; 