import React, { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

/**
 * Composant pour rendre du contenu LaTeX/mathématique
 * Supporte le LaTeX inline ($...$) et display ($$...$$)
 */
function LatexRenderer({ content, className = '' }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || !content) return;

    try {
      // Remplacer le contenu LaTeX par du HTML rendu
      let html = content;

      // Traiter les formules display ($$...$$) en premier
      html = html.replace(/\$\$([^$]+)\$\$/g, (match, tex) => {
        try {
          return katex.renderToString(tex, {
            displayMode: true,
            throwOnError: false
          });
        } catch (e) {
          console.error('Erreur rendu LaTeX display:', e);
          return match;
        }
      });

      // Traiter les formules inline ($...$)
      html = html.replace(/\$([^$]+)\$/g, (match, tex) => {
        try {
          return katex.renderToString(tex, {
            displayMode: false,
            throwOnError: false
          });
        } catch (e) {
          console.error('Erreur rendu LaTeX inline:', e);
          return match;
        }
      });

      containerRef.current.innerHTML = html;
    } catch (error) {
      console.error('Erreur lors du rendu LaTeX:', error);
      containerRef.current.textContent = content;
    }
  }, [content]);

  return <div ref={containerRef} className={className} />;
}

export default LatexRenderer;
