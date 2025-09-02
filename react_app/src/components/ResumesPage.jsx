import { useState, useEffect } from 'react';
import './ResumesPage.css';

function ResumesPage() {
    const [resumes, setResumes] = useState([]);
    const [user, setUser] = useState(null); // Для хранения данных пользователя
    const [newTitle, setNewTitle] = useState('');
    const [newContext, setNewContext] = useState('');
    const [loading, setLoading] = useState(false);
    const token = localStorage.getItem('access_token');

    // Получение данных пользователя по токену
    const fetchUserData = async () => {
        try {
            const response = await fetch('/api/auth/me', { // Предположим, есть такой эндпоинт
                headers: { 'Authorization': `Bearer ${token}` },
            });
            if (response.ok) {
                const data = await response.json();
                setUser(data);
            } else {
                console.error('Ошибка при получении данных пользователя');
            }
        } catch (error) {
            console.error('Ошибка сети:', error);
        }
    };

    const fetchResumes = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/resume/get_all_by_user', {
                headers: { 'Authorization': `Bearer ${token}` },
            });
            if (response.ok) {
                const data = await response.json();
                setResumes(data);
            } else {
                alert('Ошибка при получении резюме');
            }
        } catch (error) {
            alert('Ошибка сети или сервера');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUserData(); // Получаем данные пользователя
        fetchResumes();  // Получаем резюме
    }, []);

    const handleAddResume = async () => {
        try {
            const response = await fetch('/apiZ/resume/add_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ title: newTitle, context: newContext }),
            });
            if (response.ok) {
                await fetchResumes();
                setNewTitle('');
                setNewContext('');
            } else {
                alert('Ошибка при добавлении резюме');
            }
        } catch (error) {
            alert('Ошибка сети или сервера');
        }
    };

    return (
        <div className="page-container">
            {/* Заголовок и кнопка выхода */}
            <div className="header">
                {user && (
                    <div className="user-info">
                        <p>Резюме пользователя, {user.email}</p>
                    </div>
                )}
                <button
                    className="logout-button"
                    onClick={() => (window.location.href = '/auth/logout')}
                >
                    Выйти
                </button>
            </div>

            {/* Форма добавления нового резюме */}
            <div className="new-resume">
                <h3>Добавить новое резюме</h3>
                <input
                    placeholder="Заголовок"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                />
                <textarea
                    placeholder="Текст резюме"
                    value={newContext}
                    onChange={(e) => setNewContext(e.target.value)}
                />
                <button onClick={handleAddResume}>Добавить</button>
            </div>

            <hr />

            {/* Список резюме */}
            <h2>Список резюме</h2>
            {loading ? (
                <p>Загрузка...</p>
            ) : (
                resumes && resumes.length > 0 ? (
                    resumes.map((resume) => (
                        <div key={resume.id} className="resume-item">
                            {/* Название как ссылка на страницу деталей */}
                            <h4>
                                <a
                                    href={`/resume/get_resume_by_id/${resume.id}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {resume.title}
                                </a>
                            </h4>
                        </div>
                    ))
                ) : (
                    <p>Нет резюме для отображения</p>
                )
            )}
        </div>
    );
}

export default ResumesPage;