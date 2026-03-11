import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadSalesData = async (file, email, apiKey) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('email', email);

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'X-API-Key': apiKey,
    },
  });

  return response.data;
};
