import React, { useState, useRef } from 'react';
import { UploadCloud, FileSpreadsheet, Send, Loader2, Key } from 'lucide-react';
import { uploadSalesData } from './services/api';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [email, setEmail] = useState('');
  const [apiKey, setApiKey] = useState('dev_secret_key');
  const [status, setStatus] = useState({ type: '', message: '' });
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('active');
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('active');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('active');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile) => {
    if (selectedFile.name.endsWith('.csv') || selectedFile.name.endsWith('.xlsx')) {
      setFile(selectedFile);
      setStatus({ type: '', message: '' });
      setSummary('');
    } else {
      setFile(null);
      setStatus({ type: 'error', message: 'Please upload a valid .csv or .xlsx file' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !email || !apiKey) {
      setStatus({ type: 'error', message: 'Please fill in all fields' });
      return;
    }

    setLoading(true);
    setStatus({ type: '', message: '' });
    setSummary('');

    try {
      const result = await uploadSalesData(file, email, apiKey);
      
      if (result.status === 'success') {
        setStatus({ type: 'success', message: result.message });
      } else {
        setStatus({ type: 'warning', message: result.message });
      }
      
      if (result.summary) {
        setSummary(result.summary);
      }
      
      setFile(null);
      setEmail('');
    } catch (err) {
      console.error(err);
      const errorMessage = err.response?.data?.detail || 'An error occurred while uploading. Please check API connection and keys.';
      setStatus({ type: 'error', message: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1 className="title">Sales Insight Automator</h1>
        <p className="subtitle">AI-powered sales data analysis delivered to your inbox.</p>
      </div>

      <div className="upload-card">
        <form onSubmit={handleSubmit}>
          
          <div className="form-group">
            <label className="label">Sales Data File (.csv, .xlsx)</label>
            <div 
              className={`dropzone ${file ? 'has-file' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
                style={{ display: 'none' }} 
              />
              {file ? (
                <>
                  <FileSpreadsheet className="file-icon" size={48} />
                  <p className="file-name">{file.name}</p>
                </>
              ) : (
                <>
                  <UploadCloud className="file-icon" size={48} />
                  <p>Drag and drop your file here, or click to browse</p>
                </>
              )}
            </div>
          </div>

          <div className="form-group">
            <label className="label">Recipient Email</label>
            <input 
              type="email" 
              className="input" 
              placeholder="executive@company.com" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="label">API Key (Auth)</label>
            <div style={{ position: 'relative' }}>
              <Key size={18} style={{ position: 'absolute', left: '12px', top: '14px', color: '#94a3b8' }} />
              <input 
                type="password" 
                className="input" 
                style={{ paddingLeft: '40px' }}
                placeholder="Your secure API key" 
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading || !file || !email}>
            {loading ? (
              <>
                <Loader2 className="loader" size={24} /> Processing...
              </>
            ) : (
              <>
                <Send size={24} /> Generate Summary
              </>
            )}
          </button>

          {status.message && (
            <div className={`status-message status-${status.type}`}>
              {status.message}
            </div>
          )}
        </form>
      </div>

      {summary && (
        <div className="summary-card" style={{ marginTop: '2rem', backgroundColor: 'var(--card-bg)', borderRadius: '1rem', padding: '2.5rem', border: '1px solid var(--border-color)' }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--primary-color)' }}>AI Generated Summary:</h2>
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', color: 'var(--text-primary)' }}>
            {summary}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
