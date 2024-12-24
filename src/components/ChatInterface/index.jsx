import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, XCircle, Settings, Bot, User } from 'lucide-react';

const ChatMessage = ({ message, onRetry }) => {
  const isError = message.error;
  const isUser = message.sender === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex gap-3 max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className="flex flex-shrink-0 h-8 w-8 items-center justify-center rounded-full bg-gray-100">
          {isUser ? <User size={16} /> : <Bot size={16} />}
        </div>
        <div className={`flex flex-col space-y-2 ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`rounded-lg px-4 py-2 ${
            isUser
              ? 'bg-blue-500 text-white'
              : isError
              ? 'bg-red-50 text-red-600 border border-red-200'
              : 'bg-gray-100 text-gray-900'
          }`}>
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          </div>
          {isError && onRetry && (
            <button
              onClick={() => onRetry(message)}
              className="text-xs text-red-600 hover:text-red-700 px-2 py-1 rounded"
            >
              Retry message
            </button>
          )}
          <span className="text-xs text-gray-400">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>
      </div>
    </div>
  );
};

const CHAT_STYLES = [
  { label: 'Single Question', value: 'single_question' },
  { label: 'Normal', value: 'normal' },
  { label: 'Concise', value: 'concise' },
  { label: 'Explanatory', value: 'explanatory' },
  { label: 'Creative', value: 'creative' },
  { label: 'Knowledge', value: 'knowledge' }
];

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('normal');
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('chatApiKey') || '');
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleApiKeyChange = (newKey) => {
    setApiKey(newKey);
    localStorage.setItem('chatApiKey', newKey);
  };

  const sendMessage = async () => {
    if (!input.trim() || !apiKey) return;

    const newMessage = {
      content: input,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, newMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('https://ec2-13-229-209-181.ap-southeast-1.compute.amazonaws.com/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        },
        body: JSON.stringify({
          input: input,
          style: selectedStyle
        })
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();

      setMessages(prev => [...prev, {
        content: data.response,
        sender: 'bot',
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        content: 'Sorry, I encountered an error. Please check your API key and try again.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        error: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const retryMessage = (failedMessage) => {
    const userMessage = messages[messages.indexOf(failedMessage) - 1];
    if (userMessage) {
      setInput(userMessage.content);
      setMessages(messages.slice(0, messages.indexOf(failedMessage)));
    }
  };

  const getStyleDescription = (style) => {
    const descriptions = {
      single_question: 'Best for direct, one-off questions',
      normal: 'Standard conversational style',
      concise: 'Brief and to-the-point responses',
      explanatory: 'Detailed explanations and context',
      creative: 'Imaginative and expressive responses',
      knowledge: 'Focus on factual information'
    };
    return descriptions[style] || '';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg min-h-[600px] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b p-4">
        <div className="flex items-center space-x-2">
          <h2 className="text-lg font-semibold">Chat</h2>
          <span className="bg-gray-100 text-gray-700 text-sm px-2 py-1 rounded">
            {CHAT_STYLES.find(s => s.value === selectedStyle)?.label || selectedStyle}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={clearChat}
            className="p-2 hover:bg-gray-100 rounded-full"
            title="Clear chat"
          >
            <XCircle className="h-4 w-4" />
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 hover:bg-gray-100 rounded-full"
            title="Settings"
          >
            <Settings className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="border-b p-4 bg-gray-50">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => handleApiKeyChange(e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
                placeholder="Enter your API key"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Chat Style
              </label>
              <div className="grid grid-cols-2 gap-2">
                {CHAT_STYLES.map((style) => (
                  <button
                    key={style.value}
                    onClick={() => setSelectedStyle(style.value)}
                    className={`px-4 py-2 rounded-md transition-colors relative group ${
                      selectedStyle === style.value
                        ? 'bg-blue-500 text-white'
                        : 'bg-white border hover:bg-gray-50'
                    }`}
                    title={getStyleDescription(style.value)}
                  >
                    {style.label}
                    <span className="hidden group-hover:block absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-center text-white bg-gray-800 rounded-md whitespace-nowrap">
                      {getStyleDescription(style.value)}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 py-8">
            <Bot size={32} className="mx-auto mb-2 opacity-50" />
            <p>Start a conversation</p>
            <p className="text-sm mt-2">Current style: {getStyleDescription(selectedStyle)}</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message}
              onRetry={message.error ? retryMessage : undefined}
            />
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        {!apiKey && (
          <div className="mb-2 text-center">
            <button
              onClick={() => setShowSettings(true)}
              className="text-sm text-blue-500 hover:text-blue-700"
            >
              Please configure your API key in settings
            </button>
          </div>
        )}
        <div className="flex space-x-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading || !apiKey}
            className="flex-grow px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim() || !apiKey}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
