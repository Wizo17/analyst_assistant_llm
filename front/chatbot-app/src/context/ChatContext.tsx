import React, { createContext, useContext, useReducer, useEffect, useCallback, ReactNode, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { 
  ChatState, 
  Message, 
  ChatSession, 
  ChatRequest, 
  ChatResponse, 
  ApiInfo 
} from '../types';
import { 
  checkApiConnection, 
  getApiInfo, 
  initChatSession, 
  sendChatQuery 
} from '../services/api';

// Initial state
const initialState: ChatState = {
  sessions: [],
  activeSessionId: null,
  messages: {},
  isLoading: false,
  error: null,
  apiInfo: null,
};

// Action types
type ActionType =
  | { type: 'SET_API_CONNECTION_STATUS'; payload: boolean }
  | { type: 'SET_API_INFO'; payload: ApiInfo }
  | { type: 'ADD_SESSION'; payload: ChatSession }
  | { type: 'SET_ACTIVE_SESSION'; payload: string }
  | { type: 'ADD_MESSAGE'; payload: { sessionId: string; message: Message } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'RENAME_SESSION'; payload: { sessionId: string; newName: string } };

// Reducer function
const chatReducer = (state: ChatState, action: ActionType): ChatState => {
  switch (action.type) {
    case 'SET_API_INFO':
      return {
        ...state,
        apiInfo: action.payload,
      };
    case 'ADD_SESSION':
      return {
        ...state,
        sessions: [...state.sessions, action.payload],
        activeSessionId: action.payload.session_id,
        messages: {
          ...state.messages,
          [action.payload.session_id]: [],
        },
      };
    case 'SET_ACTIVE_SESSION':
      return {
        ...state,
        activeSessionId: action.payload,
      };
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: {
          ...state.messages,
          [action.payload.sessionId]: [
            ...(state.messages[action.payload.sessionId] || []),
            action.payload.message,
          ],
        },
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    case 'RENAME_SESSION':
      return {
        ...state,
        sessions: state.sessions.map(session => 
          session.session_id === action.payload.sessionId 
            ? { ...session, name: action.payload.newName } 
            : session
        ),
      };
    default:
      return state;
  }
};

// Create context
interface ChatContextType extends ChatState {
  initializeChat: () => Promise<void>;
  createNewSession: () => Promise<void>;
  setActiveSession: (sessionId: string) => void;
  renameSession: (sessionId: string, newName: string) => void;
  sendMessage: (
    message: string, 
    detailedAnswer: boolean, 
    fileFormat: 'json' | 'csv', 
    sampleData: boolean
  ) => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
interface ChatProviderProps {
  children: ReactNode;
}

// Ajouter une variable globale pour suivre les sessions créées
const createdSessions = new Set<string>();

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  const initializationRef = useRef(false);

  // Initialize the chat application
  const initializeChat = useCallback(async () => {
    if (initializationRef.current) {
      return;
    }

    try {
      // Check API connection
      const isConnected = await checkApiConnection();
      
      if (!isConnected) {
        dispatch({ 
          type: 'SET_ERROR', 
          payload: 'Erreur serveur. Veuillez démarrer l\'API.' 
        });
        return;
      }
      
      // Get API info
      const apiInfo = await getApiInfo();
      dispatch({ type: 'SET_API_INFO', payload: apiInfo });
      
      // Create initial session
      await createNewSession();
      
      // Marquer l'initialisation comme terminée
      initializationRef.current = true;
      
    } catch (error) {
      console.error('Error initializing chat:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: 'Erreur lors de l\'initialisation du chat.' 
      });
    }
  }, []);

  // Déplacer l'initialisation dans un useEffect du provider
  useEffect(() => {
    initializeChat();
  }, []);

  // Create a new chat session
  const createNewSession = async () => {
    try {
      // Ajouter des logs pour déboguer
      console.log('Creating new session...');
      console.log('Current sessions:', state.sessions);
      console.log('Initialization status:', initializationRef.current);
      
      dispatch({ type: 'SET_LOADING', payload: true });
      const session = await initChatSession();
      
      // Vérifier si cette session a déjà été créée
      if (createdSessions.has(session.session_id)) {
        console.log('Session already exists, skipping:', session.session_id);
        dispatch({ type: 'SET_LOADING', payload: false });
        return;
      }
      
      // Ajouter l'ID de session à l'ensemble des sessions créées
      createdSessions.add(session.session_id);
      console.log('New session created:', session.session_id);
      console.log('Created sessions set:', createdSessions);
      
      dispatch({ type: 'ADD_SESSION', payload: session });
      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      console.error('Error creating new session:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: 'Erreur lors de la création d\'une nouvelle session.' 
      });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Set active session
  const setActiveSession = (sessionId: string) => {
    dispatch({ type: 'SET_ACTIVE_SESSION', payload: sessionId });
  };

  // Rename a session
  const renameSession = (sessionId: string, newName: string) => {
    dispatch({
      type: 'RENAME_SESSION',
      payload: { sessionId, newName }
    });
  };

  // Send a message
  const sendMessage = async (
    message: string, 
    detailedAnswer: boolean, 
    fileFormat: 'json' | 'csv', 
    sampleData: boolean
  ) => {
    if (!state.activeSessionId) {
      dispatch({ 
        type: 'SET_ERROR', 
        payload: 'Aucune session active. Veuillez créer une nouvelle session.' 
      });
      return;
    }

    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      // Add user message to the state
      const userMessage: Message = {
        id: uuidv4(),
        type: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };
      
      dispatch({
        type: 'ADD_MESSAGE',
        payload: { sessionId: state.activeSessionId, message: userMessage },
      });

      // Prepare the request
      const request: ChatRequest = {
        session_id: state.activeSessionId,
        query: message,
        explanation_full: detailedAnswer,
        output_format: fileFormat,
        full_data: !sampleData, // Inverse of sampleData toggle
      };

      // Send the request to the API
      const response = await sendChatQuery(request);

      // Add assistant message to the state
      const assistantMessage: Message = {
        id: uuidv4(),
        type: 'assistant',
        content: response.business_explanation,
        timestamp: new Date().toISOString(),
        metadata: response,
      };

      dispatch({
        type: 'ADD_MESSAGE',
        payload: { sessionId: state.activeSessionId, message: assistantMessage },
      });

      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      console.error('Error sending message:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: 'Erreur lors de l\'envoi du message.' 
      });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Context value
  const value = {
    ...state,
    initializeChat,
    createNewSession,
    setActiveSession,
    renameSession,
    sendMessage,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Custom hook to use the chat context
export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
}; 