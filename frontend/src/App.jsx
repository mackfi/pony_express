import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route, Link } from 'react-router-dom';
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
import { LoginLink } from './components/Registration';
import Button from './components/Button';

const queryClient = new QueryClient();

function NotFound() {
  return <h1 className=' text-9xl text-center py-10'>404: not found</h1>;
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function Home() {

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8 text-xl">
      welcome to pony express!
      <p className='p-4'>pony express is a simple (but very cool) chat application built for CS 4550 at the University of Utah. </p>
      <p className='p-4'>on the backend, this application uses FastAPI, pydantic, and SQLite. on the frontend, this application uses React, Vite, and TailwindCSS.</p>
      <p className='p-4'>to log in, click the link below.</p>
      <Link to="/login">
        <Button className="mt-1 w-full">
          get started
        </Button>
      </Link>
    </div>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="max-h-main w-full">
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
      <Route path="/" element={<Navigate to="/chats" />} />
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
      <Route path="/" element={<Home/>} />
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
