import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import ResumesPage from './components/ResumesPage';
import ResumeDetailPage from './components/ResumeDetailPage';
import Logout from './components/Logout'; // импорт компонента выхода

function App() {
  const token = localStorage.getItem('access_token');

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/resumes"
          element={token ? <ResumesPage /> : <Navigate to="/login" />}
        />
        {/* Маршрут выхода */}
        <Route path="/auth/logout" element={<Logout />} />
        <Route path="/resume/get_resume_by_id/:id" element={<ResumeDetailPage />} />
        {/* Перенаправление по умолчанию */}
        <Route path="*" element={<Navigate to={token ? "/resumes" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;