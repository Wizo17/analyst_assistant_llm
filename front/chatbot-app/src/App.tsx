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
  background-color: #343541;
  color: #fff;
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
