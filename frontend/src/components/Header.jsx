import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="app-header">
      <div className="header-content">
        <h1>📝 Générateur de QCM</h1>
        <p className="subtitle">Créez des questionnaires mathématiques personnalisés</p>
      </div>
    </header>
  );
}

export default Header;
