import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import "./components/ChatsPage"
import ChatsPage from './components/ChatsPage';
import { AuthProvider } from './context/auth';
import { UserProvider } from './context/user';
import { useAuth } from './context/auth';
import Login from './components/Login';
import Registration from './components/Registration';
import Profile from './components/Profile';
import LeftNav from './components/LeftNav';
import TopNav from './components/TopNav';

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="max-h-main">
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />
      }
    </main>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ChatsPage />} />
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
      <Route path="/" element={<ChatsPage/>} />
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
            <Header />
            <Main/>
            {/* <Routes>
              <Route path="/" element={<ChatsPage/>} />
              <Route path="/chats" element={<ChatsPage/>} />
              <Route path="/chats/:chatId" element={<ChatsPage/>} />
              <Route path="/error/404" element={<NotFound />} />
              <Route path='/login' element={<Login/>} />
              <Route path='/register' element={<Registration/>} />
              <Route path='/profile' element={<Profile/>} />
              <Route path='/leftnavtest' element = { <LeftNav/>}/>
              <Route path="*" element={<Navigate to="/error/404" />} />
            </Routes> */}
          </UserProvider>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
