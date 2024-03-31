import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import "./components/ChatsPage"
import ChatsPage from './components/ChatsPage';
import { AuthProvider } from './context/auth';
import { UserProvider } from './context/user';
import Login from './components/Login';
import Registration from './components/Registration';

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chats" element={<ChatsPage />} />
      <Route path="/chats/:chatId" element={<ChatsPage />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <UserProvider>
            <Routes>
              <Route path="/" element={<ChatsPage/>} />
              <Route path="/chats" element={<ChatsPage/>} />
              <Route path="/chats/:chatId" element={<ChatsPage/>} />
              <Route path="/error/404" element={<NotFound />} />
              <Route path='/login' element={<Login/>} />
              <Route path='/register' element={<Registration/>} />
              <Route path="*" element={<Navigate to="/error/404" />} />
            </Routes>
          </UserProvider>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
