import React, { useState } from 'react';
import styled from 'styled-components';
import { FiUser, FiCopy, FiDownload, FiCode, FiInfo } from 'react-icons/fi';
import { IconType, IconBaseProps } from 'react-icons';
import { Message } from '../types';
import { downloadFile } from '../services/api';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useChatContext } from '../context/ChatContext';

const MessageContainer = styled.div<{ type: 'user' | 'assistant' }>`
  display: flex;
  padding: 20px;
  background-color: ${props => props.type === 'user' ? '#343541' : '#444654'};
  border-bottom: 1px solid ${props => props.type === 'user' ? '#444654' : '#565869'};
  animation: fadeIn 0.3s ease-in-out;
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;

const Avatar = styled.div<{ type: 'user' | 'assistant' }>`
  width: 30px;
  height: 30px;
  border-radius: 4px;
  background-color: ${props => props.type === 'user' ? '#10a37f' : '#7c3aed'};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  flex-shrink: 0;
`;

const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const MessageContent = styled.div`
  flex: 1;
  color: #fff;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
`;

const Timestamp = styled.div`
  font-size: 12px;
  color: #8e8ea0;
  margin-top: 8px;
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 15px;
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #40414f;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: #565869;
  }
`;

const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background-color: #343541;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 20px;
  position: relative;
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444654;
`;

const ModalTitle = styled.h3`
  color: #fff;
  margin: 0;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: #8e8ea0;
  font-size: 20px;
  cursor: pointer;
  
  &:hover {
    color: #fff;
  }
`;

interface ChatMessageProps {
  message: Message;
}

// Create a component to wrap icons
const Icon = ({ icon: IconComponent, color }: { icon: IconType; color?: string }) => {
  const Component = IconComponent as React.ComponentType<IconBaseProps>;
  return <Component color={color} />;
};

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [showSqlExplanation, setShowSqlExplanation] = useState(false);
  const [showSqlQuery, setShowSqlQuery] = useState(false);
  const { activeSessionId } = useChatContext();
  
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };
  
  const handleCopy = () => {
    if (message.content) {
      navigator.clipboard.writeText(message.content);
    }
  };
  
  const handleDownload = async () => {
    if (message.metadata?.download_link && activeSessionId) {
      try {
        const blob = await downloadFile(activeSessionId, message.metadata.download_link);
        
        // Create a download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `result.${message.metadata.download_link.split('.').pop() || 'csv'}`;
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } catch (error) {
        console.error('Error downloading file:', error);
      }
    }
  };
  
  return (
    <MessageContainer type={message.type}>
      <Avatar type={message.type}>
        {message.type === 'user' ? (
          <IconWrapper>
            <Icon icon={FiUser} color="#fff" />
          </IconWrapper>
        ) : 'AI'}
      </Avatar>
      
      <MessageContent>
        {message.content}
        
        <Timestamp>{formatTimestamp(message.timestamp)}</Timestamp>
        
        {message.type === 'assistant' && message.metadata && (
          <ActionButtons>
            <ActionButton onClick={handleCopy}>
              <IconWrapper>
                <Icon icon={FiCopy} />
              </IconWrapper>
              Copy
            </ActionButton>
            
            {message.metadata.download_link && (
              <ActionButton onClick={handleDownload}>
                <IconWrapper>
                  <Icon icon={FiDownload} />
                </IconWrapper>
                Download
              </ActionButton>
            )}
            
            {message.metadata.sql_explanation && (
              <ActionButton onClick={() => setShowSqlExplanation(true)}>
                <IconWrapper>
                  <Icon icon={FiInfo} />
                </IconWrapper>
                Explanation
              </ActionButton>
            )}
            
            {message.metadata.sql_query && (
              <ActionButton onClick={() => setShowSqlQuery(true)}>
                <IconWrapper>
                  <Icon icon={FiCode} />
                </IconWrapper>
                Code
              </ActionButton>
            )}
          </ActionButtons>
        )}
      </MessageContent>
      
      {/* SQL Explanation Modal */}
      {showSqlExplanation && message.metadata?.sql_explanation && (
        <Modal onClick={() => setShowSqlExplanation(false)}>
          <ModalContent onClick={e => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>SQL Explanation</ModalTitle>
              <CloseButton onClick={() => setShowSqlExplanation(false)}>×</CloseButton>
            </ModalHeader>
            <div>{message.metadata.sql_explanation}</div>
          </ModalContent>
        </Modal>
      )}
      
      {/* SQL Query Modal */}
      {showSqlQuery && message.metadata?.sql_query && (
        <Modal onClick={() => setShowSqlQuery(false)}>
          <ModalContent onClick={e => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>SQL Query</ModalTitle>
              <CloseButton onClick={() => setShowSqlQuery(false)}>×</CloseButton>
            </ModalHeader>
            <SyntaxHighlighter language="sql" style={vscDarkPlus}>
              {message.metadata.sql_query}
            </SyntaxHighlighter>
          </ModalContent>
        </Modal>
      )}
    </MessageContainer>
  );
};

export default ChatMessage; 