import { useState } from 'react';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (response.ok) {
        const data = await response.json();
        // Сохраняем токен в localStorage
        localStorage.setItem('access_token', data.access_token);
        // Перенаправляем на страницу с резюме
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
  };

  // Для эффекта hover на кнопку
  const [hover, setHover] = useState(false);

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
    </div>
  );
}

export default LoginPage;