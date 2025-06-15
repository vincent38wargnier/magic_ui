'use client'

import { useState, useEffect } from 'react'

export default function TelegramAdmin() {
  const [webhookUrl, setWebhookUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)
  const [checking, setChecking] = useState(true)
  const [sendChatId, setSendChatId] = useState('')
  const [sendMessage, setSendMessage] = useState('')

  // Check bot status on load
  useEffect(() => {
    checkBotStatus()
  }, [])

  const checkBotStatus = async () => {
    setChecking(true)
    try {
      const response = await fetch('/api/telegram-test')
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      setStatus({ success: false, error: error.message })
    } finally {
      setChecking(false)
    }
  }

  const handleAutoSetup = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/telegram-auto-setup', {
        method: 'POST'
      })
      const data = await response.json()
      setResult(data)
      if (data.success) {
        await checkBotStatus() // Refresh status
      }
    } catch (error) {
      setResult({ success: false, error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!sendChatId || !sendMessage) {
      setResult({ success: false, error: 'Please enter both Chat ID and message' })
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/telegram-send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          chatId: sendChatId, 
          message: sendMessage 
        }),
      })
      
      const data = await response.json()
      setResult(data)
      if (data.success) {
        setSendMessage('')
      }
    } catch (error) {
      setResult({ success: false, error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleSetWebhook = async () => {
    if (!webhookUrl) {
      setResult({ success: false, error: 'Please enter a webhook URL' })
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/telegram-webhook-setup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ webhookUrl }),
      })
      
      const data = await response.json()
      setResult(data)
      if (data.success) {
        await checkBotStatus() // Refresh status
      }
    } catch (error) {
      setResult({ success: false, error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleGetWebhookInfo = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/telegram-webhook-setup?action=info')
      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({ success: false, error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteWebhook = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/telegram-webhook-setup', {
        method: 'DELETE'
      })
      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({ success: false, error: error.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-6">
            🤖 Telegram Bot Admin
          </h1>

          {/* Status Panel */}
          <div className="mb-6">
            {checking ? (
              <div className="bg-gray-50 border rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                  <span className="text-gray-600">Checking bot status...</span>
                </div>
              </div>
            ) : status ? (
              <div className={`border rounded-lg p-4 ${status.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className={`font-medium ${status.success ? 'text-green-800' : 'text-red-800'}`}>
                      {status.success ? '✅ Bot Status: Ready' : '❌ Bot Status: Issues Found'}
                    </h3>
                    {status.bot_info && (
                      <p className="text-sm text-gray-600 mt-1">
                        Bot: @{status.bot_info.username} ({status.bot_info.first_name})
                      </p>
                    )}
                    {status.webhook_info?.url && (
                      <p className="text-xs text-gray-500 mt-1">
                        Webhook: {status.webhook_info.url}
                      </p>
                    )}
                  </div>
                  <button
                    onClick={checkBotStatus}
                    className="text-sm bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded"
                  >
                    Refresh
                  </button>
                </div>
              </div>
            ) : null}
          </div>

          {/* Auto Setup Button */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-blue-800 mb-2">🚀 Quick Auto Setup</h3>
            <p className="text-sm text-blue-700 mb-3">
              If you have WEBHOOK_URL in your environment variables, click here to auto-setup:
            </p>
            <button
              onClick={handleAutoSetup}
              disabled={loading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-4 py-2 rounded-md font-medium"
            >
              {loading ? 'Setting up...' : '⚡ Auto Setup Webhook'}
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Webhook URL (your ngrok or deployed URL)
              </label>
              <input
                type="url"
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                placeholder="https://your-domain.ngrok.io (or set WEBHOOK_URL in env)"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 placeholder-gray-500"
              />
              <p className="text-sm text-gray-500 mt-1">
                💡 <strong>Tip:</strong> Set WEBHOOK_URL in your .env file to auto-fill this field. Don't include /api/telegram-bot - it will be added automatically.
              </p>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={handleSetWebhook}
                disabled={loading}
                className="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-4 py-2 rounded-md font-medium"
              >
                {loading ? 'Setting...' : 'Set Webhook'}
              </button>
              
              <button
                onClick={handleGetWebhookInfo}
                disabled={loading}
                className="bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white px-4 py-2 rounded-md font-medium"
              >
                {loading ? 'Getting...' : 'Get Info'}
              </button>
              
              <button
                onClick={handleDeleteWebhook}
                disabled={loading}
                className="bg-red-500 hover:bg-red-600 disabled:bg-red-300 text-white px-4 py-2 rounded-md font-medium"
              >
                {loading ? 'Deleting...' : 'Delete Webhook'}
              </button>
            </div>

            {result && (
              <div className={`p-4 rounded-md ${result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                <h3 className={`font-medium ${result.success ? 'text-green-800' : 'text-red-800'}`}>
                  {result.success ? '✅ Success' : '❌ Error'}
                </h3>
                <pre className={`mt-2 text-sm ${result.success ? 'text-green-800' : 'text-red-800'} whitespace-pre-wrap font-mono`}>
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}

            <div className="border-t pt-6">
              <h3 className="font-medium text-gray-800 mb-3">📋 Quick Setup Guide:</h3>
              <ol className="list-decimal list-inside space-y-2 text-sm text-gray-600">
                <li>Add TELEGRAM_BOT_TOKEN to your environment variables</li>
                <li>Start your development server or deploy to production</li>
                <li>If local: Start ngrok with `ngrok http 3000`</li>
                <li>Copy your ngrok URL (or production URL) and paste it above</li>
                <li>Click "Set Webhook"</li>
                <li>Test your bot by sending a message!</li>
              </ol>
            </div>

            <div className="border-t pt-6">
              <h3 className="font-medium text-gray-800 mb-3">🔗 Manual Setup (Alternative):</h3>
              <p className="text-sm text-gray-600 mb-2">You can also set the webhook manually using this URL:</p>
              <code className="block bg-gray-100 p-2 rounded text-xs break-all text-gray-800 font-mono">
                https://api.telegram.org/bot{'{YOUR_BOT_TOKEN}'}/setWebhook?url={'{YOUR_WEBHOOK_URL}'}/api/telegram-bot&amp;drop_pending_updates=true
              </code>
            </div>
          </div>
        </div>

        {/* Send Message Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-xl font-bold text-gray-800 mb-6">📤 Send Test Message</h2>

          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Chat ID</label>
                <input
                  type="text"
                  value={sendChatId}
                  onChange={(e) => setSendChatId(e.target.value)}
                  placeholder="123456789"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 placeholder-gray-500"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Message</label>
                <input
                  type="text"
                  value={sendMessage}
                  onChange={(e) => setSendMessage(e.target.value)}
                  placeholder="Hello from admin panel!"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 placeholder-gray-500"
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                />
              </div>
            </div>
            <button
              onClick={handleSendMessage}
              disabled={loading}
              className="bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white px-4 py-2 rounded-md font-medium"
            >
              {loading ? 'Sending...' : '📤 Send Message'}
            </button>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm text-yellow-800">
                💡 <strong>Tip:</strong> Check your terminal/console logs to see incoming webhook data when users send messages to your bot!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 