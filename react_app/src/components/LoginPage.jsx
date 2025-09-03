import React, { useState } from 'react';


function RegisterPage({ onBack }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleRegister = async () => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (response.ok) {
        const data = await response.json();
        setSuccess('Регистрация прошла успешно! Войдите в систему.');
        setError('');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка регистрации');
        setSuccess('');
      }
    } catch (err) {
      setError('Ошибка сети');
      setSuccess('');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f9f9f9' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Регистрация</h2>
      <input
        style={{ width: '100%', padding: '10px 15px', marginBottom: '15px', border: '1px solid #ccc', borderRadius: '4px', fontSize: '16px', boxSizing: 'border-box' }}
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        style={{ width: '100%', padding: '10px 15px', marginBottom: '15px', border: '1px solid #ccc', borderRadius: '4px', fontSize: '16px', boxSizing: 'border-box' }}
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        style={{ width: '100%', padding: '12px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', fontSize: '16px', cursor: 'pointer' }}
        onClick={handleRegister}
      >
        Зарегистрироваться
      </button>
      {error && <p style={{ color: 'red', marginTop: '10px', textAlign: 'center' }}>{error}</p>}
      {success && <p style={{ color: 'green', marginTop: '10px', textAlign: 'center' }}>{success}</p>}
      <p style={{ textAlign: 'center', marginTop: '15px' }}>
        Уже есть аккаунт?{' '}
        <button onClick={onBack} style={{ color: '#4CAF50', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline', padding: 0 }}>
          Войти
        </button>
      </p>
    </div>
  );
}

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [hover, setHover] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = async () => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        window.location.href = '/resumes';
      } else {
        setError('Неверный логин или пароль');
      }
    } catch (err) {
      setError('Ошибка сети');
    }
  };

  const styles = {
    container: {
      maxWidth: '400px',
      margin: '50px auto',
      padding: '20px',
      border: '1px solid #ccc',
      borderRadius: '8px',
      boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f9f9f9',
    },
    title: {
      textAlign: 'center',
      marginBottom: '20px',
      fontSize: '24px',
      color: '#333',
    },
    input: {
      width: '100%',
      padding: '10px 15px',
      marginBottom: '15px',
      border: '1px solid #ccc',
      borderRadius: '4px',
      fontSize: '16px',
      boxSizing: 'border-box',
    },
    button: {
      width: '100%',
      padding: '12px',
      backgroundColor: '#4CAF50',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      fontSize: '16px',
      cursor: 'pointer',
      transition: 'background-color 0.3s',
    },
    buttonHover: {
      backgroundColor: '#45a049',
    },
    errorText: {
      color: 'red',
      marginTop: '10px',
      textAlign: 'center',
    },
    registerLink: {
      marginTop: '15px',
      textAlign: 'center',
      cursor: 'pointer',
      color: '#4CAF50',
      textDecoration: 'underline',
      background: 'none',
      border: 'none',
      fontSize: '14px',
    },
  };

  if (showRegister) {
    return <RegisterPage onBack={() => setShowRegister(false)} />;
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Авторизация</h2>
      <input
        style={styles.input}
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        style={styles.input}
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        style={{
          ...styles.button,
          backgroundColor: hover ? styles.buttonHover.backgroundColor : styles.button.backgroundColor,
        }}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        onClick={handleLogin}
      >
        Войти
      </button>
      {error && <p style={styles.errorText}>{error}</p>}

      <button
        style={styles.registerLink}
        onClick={() => setShowRegister(true)}
      >
        Зарегистрироваться
      </button>
    </div>
  );
}

export default LoginPage;