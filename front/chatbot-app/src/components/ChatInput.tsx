import React, { useState, FormEvent } from 'react';
import styled from 'styled-components';
import { FiSend, FiToggleLeft, FiToggleRight } from 'react-icons/fi';
import { IconType, IconBaseProps } from 'react-icons';
import { FormState } from '../types';

const ChatInputContainer = styled.div`
  padding: 15px;
  background-color: #f0f4f8;
  border-top: 1px solid #c0d6df;
  height: 80px; /* Hauteur fixe pour correspondre à l'ApiInfoContainer */
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const InputForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const InputWrapper = styled.div`
  display: flex;
  position: relative;
`;

const TextInput = styled.textarea`
  width: 100%;
  padding: 8px 45px 8px 15px;
  border-radius: 8px;
  border: 1px solid #c0d6df;
  background-color: white;
  color: #2c3e50;
  font-size: 14px;
  resize: none;
  min-height: 36px;
  max-height: 36px;
  outline: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  
  &:focus {
    border-color: #4a90e2;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
  }
  
  &::placeholder {
    color: #7b8a9a;
  }
`;

const SendButton = styled.button`
  position: absolute;
  right: 10px;
  top: 50%; /* Centrer verticalement */
  transform: translateY(-50%); /* Centrer verticalement */
  background: none;
  border: none;
  color: #4a90e2;
  cursor: pointer;
  
  &:hover {
    color: #357ABD;
  }
  
  &:disabled {
    color: #a3c2e6;
    cursor: not-allowed;
  }
`;

const ToggleContainer = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 0 5px;
  margin-bottom: 5px;
`;

const ToggleGroup = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const ToggleItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
`;

const ToggleLabel = styled.span`
  font-size: 12px;
  color: #7b8a9a;
`;

// Create styled components for the toggle icons
const ToggleOn = styled.div`
  color: #4a90e2; /* Bleu vif pour les toggles actifs */
  display: flex;
  align-items: center;
`;

const ToggleOff = styled.div`
  color: #7b8a9a; /* Gris bleuté pour les toggles inactifs */
  display: flex;
  align-items: center;
`;

const SendButtonIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

// Create a component to wrap icons
const Icon = ({ icon: IconComponent }: { icon: IconType }) => {
  const Component = IconComponent as React.ComponentType<IconBaseProps>;
  return <Component />;
};

interface ChatInputProps {
  onSendMessage: (message: string, formState: FormState) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [formState, setFormState] = useState<FormState>({
    detailedAnswer: true,
    fileFormat: 'json',
    sampleData: true,
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message, formState);
      setMessage('');
    }
  };

  const handleToggle = (key: keyof FormState) => {
    if (key === 'fileFormat') {
      setFormState({
        ...formState,
        fileFormat: formState.fileFormat === 'json' ? 'csv' : 'json',
      });
    } else {
      setFormState({
        ...formState,
        [key]: !formState[key],
      });
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <ChatInputContainer>
      <InputForm onSubmit={handleSubmit}>
        <ToggleContainer>
          <ToggleGroup>
            <ToggleItem onClick={() => handleToggle('detailedAnswer')}>
              {formState.detailedAnswer ? (
                <ToggleOn>
                  <Icon icon={FiToggleRight} />
                </ToggleOn>
              ) : (
                <ToggleOff>
                  <Icon icon={FiToggleLeft} />
                </ToggleOff>
              )}
              <ToggleLabel>Detailed Answer</ToggleLabel>
            </ToggleItem>
            
            <ToggleItem onClick={() => handleToggle('fileFormat')}>
              {formState.fileFormat === 'json' ? (
                <ToggleOn>
                  <Icon icon={FiToggleRight} />
                </ToggleOn>
              ) : (
                <ToggleOff>
                  <Icon icon={FiToggleLeft} />
                </ToggleOff>
              )}
              <ToggleLabel>File Format: {formState.fileFormat.toUpperCase()}</ToggleLabel>
            </ToggleItem>
          </ToggleGroup>
          
          <ToggleItem onClick={() => handleToggle('sampleData')}>
            {formState.sampleData ? (
              <ToggleOn>
                <Icon icon={FiToggleRight} />
              </ToggleOn>
            ) : (
              <ToggleOff>
                <Icon icon={FiToggleLeft} />
              </ToggleOff>
            )}
            <ToggleLabel>Sample Data</ToggleLabel>
          </ToggleItem>
        </ToggleContainer>
        
        <InputWrapper>
          <TextInput
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            disabled={isLoading}
            rows={1}
          />
          <SendButton type="submit" disabled={!message.trim() || isLoading}>
            <SendButtonIcon>
              <Icon icon={FiSend} />
            </SendButtonIcon>
          </SendButton>
        </InputWrapper>
      </InputForm>
    </ChatInputContainer>
  );
};

export default ChatInput; 