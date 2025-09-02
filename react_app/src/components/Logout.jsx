import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
  const navigate = useNavigate();


  useEffect(() => {
    // Удаляем токен
    localStorage.removeItem('access_token');
    // Можно удалить и другие данные, если есть
    // localStorage.removeItem('other_data');

    // Перенаправляем на страницу входа или главную
    navigate('/login'); // или любой другой маршрут
  }, [navigate]);

  return null; // ничего не отображаем
}

export default Logout;