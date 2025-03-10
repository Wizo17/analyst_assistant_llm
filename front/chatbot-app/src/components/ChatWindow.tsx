import React, { useRef, useEffect } from 'react';
import styled from 'styled-components';
import { useChatContext } from '../context/ChatContext';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { FormState } from '../types';

const ChatWindowContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
  background-color: #343541;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  scroll-behavior: smooth;
`;

const WelcomeMessage = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #8e8ea0;
  text-align: center;
  padding: 0 20px;
`;

const WelcomeTitle = styled.h2`
  font-size: 24px;
  margin-bottom: 10px;
  color: #fff;
`;

const WelcomeText = styled.p`
  font-size: 16px;
  max-width: 600px;
  line-height: 1.6;
`;

const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #8e8ea0;
  
  &::after {
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid #8e8ea0;
    border-radius: 50%;
    border-top-color: transparent;
    margin-left: 10px;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const ErrorMessage = styled.div`
  background-color: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  color: #ff6b6b;
  padding: 15px;
  margin: 20px;
  border-radius: 5px;
  text-align: center;
`;

const ChatWindow: React.FC = () => {
  const { 
    activeSessionId, 
    messages, 
    isLoading, 
    error,
    sendMessage 
  } = useChatContext();
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, activeSessionId]);
  
  const handleSendMessage = (message: string, formState: FormState) => {
    sendMessage(
      message, 
      formState.detailedAnswer, 
      formState.fileFormat, 
      formState.sampleData
    );
  };
  
  const activeMessages = activeSessionId ? messages[activeSessionId] || [] : [];
  
  return (
    <ChatWindowContainer>
      <MessagesContainer>
        {activeSessionId && activeMessages.length === 0 && !isLoading && !error && (
          <WelcomeMessage>
            <WelcomeTitle>Bienvenue dans l'assistant d'analyse</WelcomeTitle>
            <WelcomeText>
              Posez vos questions sur les données et obtenez des réponses détaillées avec des explications SQL.
            </WelcomeText>
          </WelcomeMessage>
        )}
        
        {error && <ErrorMessage>{error}</ErrorMessage>}
        
        {activeSessionId && activeMessages.map(message => (
          <ChatMessage key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <LoadingIndicator>Génération de la réponse...</LoadingIndicator>
        )}
        
        <div ref={messagesEndRef} />
      </MessagesContainer>
      
      <ChatInput 
        onSendMessage={handleSendMessage} 
        isLoading={isLoading} 
      />
    </ChatWindowContainer>
  );
};

export default ChatWindow; 