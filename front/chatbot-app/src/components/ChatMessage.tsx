import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FiUser, FiCopy, FiDownload, FiCode, FiInfo } from 'react-icons/fi';
import { IconType, IconBaseProps } from 'react-icons';
import { Message } from '../types';
import { downloadFile } from '../services/api';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useChatContext } from '../context/ChatContext';
import ReactMarkdown from 'react-markdown';
import { format, FormatOptionsWithLanguage } from 'sql-formatter';

const MessageContainer = styled.div<{ type: 'user' | 'assistant' }>`
  display: flex;
  padding: 20px;
  background-color: ${props => props.type === 'user' ? '#e1e8ed' : '#f0f4f8'};
  border-bottom: 1px solid ${props => props.type === 'user' ? '#c0d6df' : '#d1e2eb'};
  animation: fadeIn 0.3s ease-in-out;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;

const Avatar = styled.div<{ type: 'user' | 'assistant' }>`
  width: 30px;
  height: 30px;
  border-radius: 4px;
  background-color: ${props => props.type === 'user' ? '#4a90e2' : '#5b9bd5'};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  flex-shrink: 0;
  color: white;
`;

const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const MessageContent = styled.div`
  flex: 1;
  padding: 10px 15px;
  line-height: 1.5;
  position: relative;
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
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background-color: #f0f4f8;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
`;

const ModalHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  background-color: #e1e8ed;
  border-bottom: 1px solid #c0d6df;
`;

const ModalTitle = styled.h3`
  margin: 0;
  color: #2c3e50;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #4a90e2;
  
  &:hover {
    color: #357ABD;
  }
`;

const MarkdownContent = styled.div`
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
  color: #2c3e50; /* Bleu foncé pour le texte principal */
  
  /* Styles for markdown elements */
  h1, h2, h3, h4, h5, h6 {
    margin-top: 1em;
    margin-bottom: 0.3em;
    font-weight: 600;
    color: #2c3e50; /* Bleu foncé pour les titres */
  }
  
  h1 {
    font-size: 1.6em;
  }
  
  h2 {
    font-size: 1.4em;
  }
  
  h3 {
    font-size: 1.2em;
  }
  
  p {
    margin: 0.4em 0;
  }
  
  ul, ol {
    margin: 0.4em 0;
    padding-left: 1.5em;
  }
  
  li {
    margin: 0.2em 0;
  }
  
  /* Réduire l'espacement entre les paragraphes */
  p + p {
    margin-top: 0.3em;
  }
  
  /* Réduire l'espacement après les listes */
  ul + p, ol + p {
    margin-top: 0.3em;
  }
  
  /* Réduire l'espacement avant les listes */
  p + ul, p + ol {
    margin-top: 0.3em;
  }
  
  code {
    background-color: #e1e8ed; /* Bleu clair pour le fond du code */
    padding: 0.1em 0.3em;
    border-radius: 3px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.9em;
    color: #2c3e50; /* Bleu foncé pour le texte du code */
  }
  
  pre {
    background-color: #e1e8ed; /* Bleu clair pour le fond des blocs de code */
    padding: 0.7em;
    border-radius: 5px;
    overflow-x: auto;
    margin: 0.5em 0;
  }
  
  blockquote {
    border-left: 3px solid #4a90e2; /* Bleu vif pour la bordure des citations */
    padding-left: 0.8em;
    margin: 0.5em 0;
    margin-left: 0;
    color: #7b8a9a; /* Gris bleuté pour le texte des citations */
    background-color: #f8fafc; /* Bleu très clair pour le fond des citations */
    padding: 0.5em 0.8em;
    border-radius: 0 3px 3px 0;
  }
  
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.7em 0;
  }
  
  th, td {
    border: 1px solid #c0d6df; /* Bordure bleu clair */
    padding: 0.4em;
    text-align: left;
  }
  
  th {
    background-color: #e1e8ed; /* Bleu clair pour l'en-tête */
  }
  
  a {
    color: #4a90e2; /* Bleu vif pour les liens */
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
  
  /* Supprimer les marges excessives des éléments imbriqués */
  li > p {
    margin: 0;
  }
  
  /* Ajuster l'espacement des sauts de ligne */
  br {
    display: block;
    content: "";
    margin-top: 0.2em;
  }
`;

const CodeContainer = styled.div`
  max-height: 70vh;
  overflow-y: auto;
  border-radius: 5px;
  background-color: #f0f4f8; /* Bleu très clair pour le fond */
  margin-top: 10px;
  border: 1px solid #c0d6df; /* Bordure bleu clair */
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
  const [formattedSql, setFormattedSql] = useState('');
  const { activeSessionId } = useChatContext();
  
  // Format SQL when the message changes or when the SQL query modal is opened
  useEffect(() => {
    if (message.metadata?.sql_query && showSqlQuery) {
      try {
        // Format the SQL with sql-formatter
        const formatted = format(message.metadata.sql_query, {
          language: 'sql',
          tabWidth: 2,
          keywordCase: 'upper',
          linesBetweenQueries: 2,
        });
        setFormattedSql(formatted);
      } catch (error) {
        console.error('Error formatting SQL:', error);
        setFormattedSql(message.metadata.sql_query);
      }
    }
  }, [message.metadata?.sql_query, showSqlQuery]);
  
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };
  
  const handleCopy = () => {
    if (message.content) {
      navigator.clipboard.writeText(message.content);
    }
  };
  
  const handleCopySql = () => {
    if (formattedSql) {
      navigator.clipboard.writeText(formattedSql);
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
        {message.type === 'user' ? (
          message.content
        ) : (
          <MarkdownContent>
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </MarkdownContent>
        )}
        
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
            <MarkdownContent>
              <ReactMarkdown>{message.metadata.sql_explanation}</ReactMarkdown>
            </MarkdownContent>
          </ModalContent>
        </Modal>
      )}
      
      {/* SQL Query Modal */}
      {showSqlQuery && message.metadata?.sql_query && (
        <Modal onClick={() => setShowSqlQuery(false)}>
          <ModalContent onClick={e => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>SQL Query</ModalTitle>
              <div>
                <ActionButton onClick={handleCopySql} title="Copy SQL">
                  <IconWrapper>
                    <Icon icon={FiCopy} />
                  </IconWrapper>
                </ActionButton>
                <CloseButton onClick={() => setShowSqlQuery(false)}>×</CloseButton>
              </div>
            </ModalHeader>
            <CodeContainer>
              <SyntaxHighlighter 
                language="sql" 
                style={vscDarkPlus}
                showLineNumbers={true}
                wrapLines={true}
                customStyle={{
                  margin: 0,
                  padding: '15px',
                  fontSize: '14px',
                  borderRadius: '5px',
                }}
              >
                {formattedSql || message.metadata.sql_query}
              </SyntaxHighlighter>
            </CodeContainer>
          </ModalContent>
        </Modal>
      )}
    </MessageContainer>
  );
};

export default ChatMessage; 