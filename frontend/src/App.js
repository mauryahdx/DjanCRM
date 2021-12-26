import logo from './logo.svg';
import './App.scss';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/registration/Login'
import SignUp from './pages/registration/SignUp'
import {BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    
    <div className="max-w-7xl mx-auto">
      
     <BrowserRouter>
      <Navbar></Navbar>
      <Routes>
       <Route path="/" exact element={<Home/>}/>
       <Route path="/login" exact element={<Login/>}/>
       <Route path="/signup" exact element={<SignUp/>}/>
    
      </Routes>
      </BrowserRouter>
    </div>
    
  );
}

export default App;
