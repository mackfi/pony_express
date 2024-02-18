import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import "./components/ChatsPage"
import ChatsPage from './components/ChatsPage';

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<h1>placeholder</h1>} />
          <Route path="/chats" element={<ChatsPage/>} />
          <Route path="/chats/:chatId" element={<ChatsPage/>} />
          <Route path="/error/404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/error/404" />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
