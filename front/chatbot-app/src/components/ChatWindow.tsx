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
  background-color: #f0f4f8;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  scroll-behavior: smooth;
  padding: 0 10px;
`;

const WelcomeMessage = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #7b8a9a;
  text-align: center;
  padding: 0 20px;
`;

const WelcomeTitle = styled.h2`
  font-size: 24px;
  margin-bottom: 10px;
  color: #2c3e50;
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
  color: #4a90e2;
  
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
  background-color: #fce4e4;
  color: #e74c3c;
  padding: 15px;
  margin: 15px;
  border-radius: 5px;
  text-align: center;
  border: 1px solid #f7d6d6;
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
            <WelcomeTitle>Welcome to the Analysis Assistant</WelcomeTitle>
            <WelcomeText>
            Ask your questions and get detailed answers with SQL explanations and code — no SQL expertise needed.
            </WelcomeText>
          </WelcomeMessage>
        )}
        
        {error && <ErrorMessage>{error}</ErrorMessage>}
        
        {activeSessionId && activeMessages.map(message => (
          <ChatMessage key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <LoadingIndicator>Loading...</LoadingIndicator>
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