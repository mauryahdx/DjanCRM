import logo from './logo.svg';
import './App.scss';
import Navbar from './components/Navbar';
import Home from './pages/Home';

function App() {
  return (
    <div className="max-w-7xl mx-auto">
      <Navbar></Navbar>
      <Home></Home>
    </div>
  );
}

export default App;
