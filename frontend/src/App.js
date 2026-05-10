import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Llamar al backend en el montaje del componente
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/hello');
        setMessage(response.data.message);
        setError(null);
      } catch (err) {
        setError('Error al conectar con el servidor: ' + err.message);
        setMessage('');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Acadelytics</h1>
        <p>Plataforma Educativa Inteligente</p>
        
        <div className="content">
          {loading && <p className="loading">Cargando...</p>}
          {error && <p className="error">{error}</p>}
          {message && <p className="success">{message}</p>}
        </div>

        <div className="info">
          <h2>Bienvenido</h2>
          <p>Backend con Flask y Frontend con React</p>
        </div>
      </header>
    </div>
  );
}

export default App;
