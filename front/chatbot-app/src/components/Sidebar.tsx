import React, { useState } from 'react';
import styled from 'styled-components';
import { FiPlus, FiMessageSquare, FiInfo, FiEdit, FiCheck } from 'react-icons/fi';
import { IconType, IconBaseProps } from 'react-icons';
import { useChatContext } from '../context/ChatContext';

const SidebarContainer = styled.div`
  width: 260px;
  height: 100%;
  background-color: #e1e8ed;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #c0d6df;
`;

const NewChatButton = styled.button`
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 16px;
  margin: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
  
  &:hover {
    background-color: #357ABD;
  }
  
  &:disabled {
    background-color: #a3c2e6;
    cursor: not-allowed;
  }
`;

const IconWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const SessionsList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 10px;
`;

const SessionActions = styled.div`
  display: flex;
  align-items: center;
  margin-left: auto;
  opacity: 0;
  transition: opacity 0.2s;
`;

const SessionItem = styled.div<{ active: boolean }>`
  display: flex;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  background-color: ${props => props.active ? '#c0d6df' : 'transparent'};
  border-radius: 5px;
  margin: 5px 0;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: ${props => props.active ? '#c0d6df' : '#d1e2eb'};
    
    ${SessionActions} {
      opacity: 1;
    }
  }
`;

const SessionIcon = styled.div`
  display: flex;
  align-items: center;
  margin-right: 10px;
  color: #4a90e2;
`;

const SessionName = styled.div`
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const SessionNameInput = styled.input`
  flex: 1;
  background-color: #f0f4f8;
  border: 1px solid #c0d6df;
  color: #2c3e50;
  padding: 5px;
  border-radius: 3px;
  outline: none;
  font-size: 14px;
  
  &:focus {
    border-color: #4a90e2;
  }
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: #4a90e2;
  cursor: pointer;
  padding: 5px;
  margin-left: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    color: #357ABD;
  }
`;

const ApiInfoContainer = styled.div`
  padding: 15px;
  border-top: 1px solid #c0d6df;
  font-size: 12px;
  background-color: #e1e8ed;
  margin-top: auto;
  height: 80px;
`;

const ApiInfoItem = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
`;

const ApiInfoLabel = styled.span`
  color: #7b8a9a;
`;

const ApiInfoValue = styled.span`
  color: #4a90e2;
  font-weight: 500;
`;

// Create a component to wrap icons
const Icon = ({ icon: IconComponent }: { icon: IconType }) => {
  const Component = IconComponent as React.ComponentType<IconBaseProps>;
  return <Component />;
};

const Sidebar: React.FC = () => {
  const { 
    sessions, 
    activeSessionId, 
    createNewSession, 
    setActiveSession,
    renameSession,
    apiInfo,
    isLoading
  } = useChatContext();
  
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [newSessionName, setNewSessionName] = useState('');

  const handleNewChat = () => {
    createNewSession();
  };

  const handleSessionClick = (sessionId: string) => {
    if (editingSessionId !== sessionId) {
      setActiveSession(sessionId);
    }
  };
  
  const handleEditClick = (e: React.MouseEvent, sessionId: string, currentName: string) => {
    e.stopPropagation();
    setEditingSessionId(sessionId);
    setNewSessionName(currentName);
  };
  
  const handleSaveClick = (e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation();
    if (newSessionName.trim()) {
      renameSession(sessionId, newSessionName.trim());
    }
    setEditingSessionId(null);
  };
  
  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewSessionName(e.target.value);
  };
  
  const handleNameKeyDown = (e: React.KeyboardEvent, sessionId: string) => {
    if (e.key === 'Enter') {
      if (newSessionName.trim()) {
        renameSession(sessionId, newSessionName.trim());
      }
      setEditingSessionId(null);
    } else if (e.key === 'Escape') {
      setEditingSessionId(null);
    }
  };

  return (
    <SidebarContainer>
      <NewChatButton onClick={handleNewChat} disabled={isLoading}>
        <IconWrapper>
          <Icon icon={FiPlus} />
        </IconWrapper>
        New Chat
      </NewChatButton>
      
      <SessionsList>
        {sessions.map(session => (
          <SessionItem 
            key={session.session_id} 
            active={session.session_id === activeSessionId}
            onClick={() => handleSessionClick(session.session_id)}
          >
            <SessionIcon>
              <Icon icon={FiMessageSquare} />
            </SessionIcon>
            
            {editingSessionId === session.session_id ? (
              <SessionNameInput 
                value={newSessionName}
                onChange={handleNameChange}
                onKeyDown={(e) => handleNameKeyDown(e, session.session_id)}
                autoFocus
                onClick={(e) => e.stopPropagation()}
              />
            ) : (
              <SessionName>{session.name}</SessionName>
            )}
            
            <SessionActions>
              {editingSessionId === session.session_id ? (
                <ActionButton onClick={(e) => handleSaveClick(e, session.session_id)}>
                  <Icon icon={FiCheck} />
                </ActionButton>
              ) : (
                <ActionButton onClick={(e) => handleEditClick(e, session.session_id, session.name)}>
                  <Icon icon={FiEdit} />
                </ActionButton>
              )}
            </SessionActions>
          </SessionItem>
        ))}
      </SessionsList>
      
      <ApiInfoContainer>
        <ApiInfoItem>
          <ApiInfoLabel>LLM Model:</ApiInfoLabel>
          <ApiInfoValue>{apiInfo?.llm_model || 'N/A'}</ApiInfoValue>
        </ApiInfoItem>
        <ApiInfoItem>
          <ApiInfoLabel>LLM Provider:</ApiInfoLabel>
          <ApiInfoValue>{apiInfo?.llm_provider || 'N/A'}</ApiInfoValue>
        </ApiInfoItem>
      </ApiInfoContainer>
    </SidebarContainer>
  );
};

export default Sidebar; 