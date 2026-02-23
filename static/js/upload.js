/**
 * MARGAM AI – Upload form handler
 */
(function () {
  const form = document.getElementById('uploadForm');
  const result = document.getElementById('result');
  const submitBtn = document.getElementById('submitBtn');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.checkValidity()) return;

    const fd = new FormData(form);
    const fileInput = document.getElementById('file');
    if (fileInput.files.length) {
      fd.set('file', fileInput.files[0]);
    }

    submitBtn.disabled = true;
    result.hidden = true;

    try {
      const res = await fetch('/upload/', {
        method: 'POST',
        body: fd
      });
      const data = await res.json();

      if (!res.ok) {
        result.className = 'result-box error';
        result.textContent = data.error || 'Upload failed';
      } else {
        result.className = 'result-box success';
        result.innerHTML = [
          '<strong>Detection complete</strong>',
          `<p>CRRS: ${data.composite_risk_score} (${data.risk_level})</p>`,
          `<p>Potholes: ${data.pothole_count} | Cracks: ${data.crack_count}</p>`,
          `<p>District: ${data.district}</p>`
        ].join('');
      }
    } catch (err) {
      result.className = 'result-box error';
      result.textContent = 'Network error: ' + err.message;
    } finally {
      result.hidden = false;
      submitBtn.disabled = false;
    }
  });
})();
