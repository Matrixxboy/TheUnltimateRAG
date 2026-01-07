import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL;
// const API_BASE_URL = "http://localhost:8000"
console.log(API_BASE_URL)
if (!API_BASE_URL) {
    throw new Error('backend url is not defined in the environment variables');
}

// Ensure the base URL maps to the correct API version endpoint
const baseURL = API_BASE_URL.endsWith('/api/v1')
    ? API_BASE_URL
    : `${API_BASE_URL}/api/v1`;

const api = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const ingestDocument = async (file, userId, accessLevel = 'private') => {
    const formData = new FormData();
    formData.append('file', file);
    if (userId) formData.append('user_id', userId);
    formData.append('access_level', accessLevel);

    return api.post('/ingest', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

export const chat = async ({ query, sessionId, userId, systemPrompt, temperature = 0.7, maxTokens }) => {
    return api.post('/chat', {
        query,
        session_id: sessionId,
        user_id: userId,
        system_prompt: systemPrompt,
        temperature,
        max_tokens: maxTokens
    });
};

export default api;
