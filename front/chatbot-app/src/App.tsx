import React from 'react';
import styled from 'styled-components';
import { ChatProvider, useChatContext } from './context/ChatContext';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import './App.css';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #f0f4f8; /* Bleu très clair pour le fond principal */
  color: #2c3e50; /* Bleu foncé pour le texte */
`;

const AppContent = () => {
  const { error } = useChatContext();
  
  return (
    <AppContainer>
      <Sidebar />
      <ChatWindow />
    </AppContainer>
  );
};

const App: React.FC = () => {
  return (
    <ChatProvider>
      <AppContent />
    </ChatProvider>
  );
};

export default App;
