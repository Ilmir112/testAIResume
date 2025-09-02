import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './ResumeDetailPage.css';

function ResumeDetailPage() {
  const { id } = useParams();
  const [histories, setHistories] = useState([]); // Массив историй
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('access_token');

  const fetchHistories = async () => {
    setLoading(true);
    const response = await fetch(`/api/resume/get_resume_by_id/${id}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (response.ok) {
      const data = await response.json();
      setHistories(data); // data — массив ResumesHistory
    } else {
      alert('Ошибка при загрузке данных');
    }
    setLoading(false);
  };

  const handleImprove = async (historyId, title, context) => {
    const response = await fetch(`/api/resume/${historyId}/improve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ title, context }),
    });
    if (response.ok) {
      const data = await response.json();
      alert(`Улучшенное резюме:\n${data.detail.improved_content}`);
    } else {
      alert('Ошибка при улучшении резюме');
    }
  };

  useEffect(() => {
    fetchHistories();
  }, [id]);

  if (loading) return <p>Загрузка...</p>;
  if (!histories || histories.length === 0) return <p>Истории не найдены</p>;

  return (
    <div className="resume-detail-container">
      <h2 className="resume-title">Истории резюме</h2>
      {histories.map((history) => (
        <div key={history.id} className="history-item">
          <h3>Версия резюме № {history.id}</h3>
          {/*<p><strong>Контекст:</strong> {history.context}</p>*/}
          {history.resume && (
            <>
              <h4>Резюме:</h4>
              <p><strong>Заголовок:</strong> {history.resume.title}</p>
              <p><strong>Контекст:</strong> {history.resume.context}</p>
              <button
                className="improve-button"
                onClick={() =>
                  handleImprove(history.id, history.resume.title, history.resume.context)
                }
              >
                Улучшить
              </button>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default ResumeDetailPage;