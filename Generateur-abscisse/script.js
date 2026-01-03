document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate');
    const exportSvgBtn = document.getElementById('export-svg');
    const exportPngBtn = document.getElementById('export-png');
    const exportPdfBtn = document.getElementById('export-pdf');
    const axisSvg = document.getElementById('axis-svg');
    const lengthInput = document.getElementById('length');
    const scaleInput = document.getElementById('scale');
    const ticksInput = document.getElementById('ticks');

    // Fonction pour dessiner l'axe
    function drawAxis(lengthCm, scale, numTicks) {
        // Vider le SVG
        axisSvg.innerHTML = '';

        // Dimensions : 1 cm = 100 unités dans le viewBox (pour précision)
        const cmToUnits = 100;
        const totalWidth = lengthCm * cmToUnits;
        const height = 200;

        // Ajuster le viewBox
        axisSvg.setAttribute('viewBox', `0 0 ${totalWidth} ${height}`);

        // Dessiner la ligne principale (axe horizontal)
        const axisLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        axisLine.setAttribute('x1', '0');
        axisLine.setAttribute('y1', height / 2);
        axisLine.setAttribute('x2', totalWidth);
        axisLine.setAttribute('y2', height / 2);
        axisLine.setAttribute('stroke', 'black');
        axisLine.setAttribute('stroke-width', '2');
        axisSvg.appendChild(axisLine);

        // Dessiner les graduations et étiquettes
        const tickSpacing = totalWidth / numTicks;
        for (let i = 0; i <= numTicks; i++) {
            const x = i * tickSpacing;
            const y = height / 2;

            // Ligne de graduation
            const tick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            tick.setAttribute('x1', x);
            tick.setAttribute('y1', y - 10);
            tick.setAttribute('x2', x);
            tick.setAttribute('y2', y + 10);
            tick.setAttribute('stroke', 'black');
            tick.setAttribute('stroke-width', '1');
            axisSvg.appendChild(tick);

            // Étiquette
            const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            label.setAttribute('x', x);
            label.setAttribute('y', y + 30);
            label.setAttribute('text-anchor', 'middle');
            label.setAttribute('font-size', '12');
            const value = i * scale;
            label.textContent = value % 1 === 0 ? value.toString() : value.toFixed(1);
            axisSvg.appendChild(label);
        }
    }

    // Événement pour générer
    generateBtn.addEventListener('click', () => {
        const length = parseFloat(lengthInput.value);
        const scale = parseFloat(scaleInput.value);
        const ticks = parseInt(ticksInput.value);
        drawAxis(length, scale, ticks);
    });

    // Générer par défaut
    drawAxis(10, 1, 10);

    // Export en SVG
    exportSvgBtn.addEventListener('click', () => {
        const svgData = new XMLSerializer().serializeToString(axisSvg);
        const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'axe-abscisses.svg';
        a.click();
        URL.revokeObjectURL(url);
    });

    // Export en PNG
    exportPngBtn.addEventListener('click', () => {
        html2canvas(axisSvg).then(canvas => {
            const link = document.createElement('a');
            link.download = 'axe-abscisses.png';
            link.href = canvas.toDataURL();
            link.click();
        });
    });

    // Export en PDF
    exportPdfBtn.addEventListener('click', () => {
        const length = parseFloat(lengthInput.value);
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF({
            orientation: 'landscape',
            unit: 'cm',
            format: [length + 2, 5]  // Largeur basée sur la longueur + marges
        });

        html2canvas(axisSvg).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            pdf.addImage(imgData, 'PNG', 1, 1, length, 3);  // Position et taille en cm
            pdf.save('axe-abscisses.pdf');
        });
    });
});
