import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [assistantId, setAssistantId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [chatStatus, setChatStatus] = useState('');
  const [fileId, setFileId] = useState(null);

  useEffect(() => {
    const createAssistant = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await axios.post('http://localhost:8000/assistant/create', {
          name: 'Math Teacher',
          instructions: `You are a friendly and patient math teacher and tutor for students aged 8-11.
          Your goal is to explain math concepts in a simple and engaging way, as if talking to a child.
          Use everyday examples and simple language.
          If the student doesn't understand, try explaining differently using analogies or visual descriptions.
          Ask questions to ensure the student is following your explanation.
          Always be encouraging and supportive.
          Break down complex ideas into small, easy-to-understand parts.
          If you need to use math terms, always explain what they mean.
          Remember, you're replacing a real teacher, so your explanations should be very clear and accessible.
          Respond in the same language as the student's question.`
          });
        setAssistantId(response.data.id);
      } catch (error) {
        console.error('Error creating assistant:', error);
        setError('Failed to create assistant. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
    createAssistant();
  }, []);

  const sendMessage = useCallback(async () => {
    if (input.trim() === '' || !assistantId) return;
    const userMessage = { role: 'user', content: input };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);
    setChatStatus('Sending message...');
    try {
      const chatData = {
        content: input,
        assistant_id: assistantId,
        session_id: sessionId,
      };
      
      if (fileId) {
        chatData.attachments = [{ file_id: fileId }];
      }

      const response = await axios.post('http://localhost:8000/assistant/chat', chatData);
      console.log('Full server response:', JSON.stringify(response.data, null, 2));
      const assistantMessage = { role: 'assistant', content: response.data.response };
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
      setSessionId(response.data.session_id);
      setChatStatus('Message sent and response received');
    } catch (error) {
      console.error('Error sending message:', error);
      setError(`Error: ${error.message}`);
      setChatStatus('Failed to send message');
    } finally {
      setIsLoading(false);
      setFileId(null);  // Reset fileId after sending
      setUploadStatus('');  // Clear upload status
    }
  }, [input, assistantId, sessionId, fileId]);

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  const uploadFile = useCallback(async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    setIsLoading(true);
    setError(null);
    setUploadStatus('Uploading file...');
    try {
      const response = await axios.post('http://localhost:8000/assistant/upload-file', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      console.log('File uploaded successfully:', response.data.file_id);
      setFileId(response.data.file_id);
      setUploadStatus(`File uploaded successfully: ${file.name}`);
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('Failed to upload file. Please try again.');
      setUploadStatus('File upload failed');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const startNewTopic = useCallback(() => {
    setSessionId(null);
    setMessages([]);
    setChatStatus('Started a new topic');
  }, []);

  return (
    <div className="App">
      <h1>Math Tutor AI</h1>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.content}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage} disabled={isLoading}>Send</button>
        <label className="file-upload-label">
          Upload File
          <input type="file" className="file-upload-input" onChange={uploadFile} />
        </label>
        <button onClick={startNewTopic}>New Topic</button>
      </div>
      {error && <div className="error-message">{error}</div>}
      {isLoading && <div className="loading">Loading...</div>}
      <div className="status-container">
        <p>Upload status: {uploadStatus}</p>
        <p>Chat status: {chatStatus}</p>
      </div>
    </div>
  );
}

export default App;
