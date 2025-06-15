// Simple Telegram bot helpers for Magic Yeti

export async function validateBotToken(botToken) {
  try {
    const response = await fetch(`https://api.telegram.org/bot${botToken}/getMe`)
    const data = await response.json()
    
    if (!data.ok) {
      return {
        success: false,
        error: 'Invalid bot token'
      }
    }
    
    return {
      success: true,
      bot_info: data.result
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}

export async function setBotWebhook(botToken, webhookUrl) {
  try {
    const fullWebhookUrl = `${webhookUrl}/api/telegram-bot`
    
    console.log('Setting webhook:', {
      botToken: botToken.substring(0, 10) + '...',
      webhookUrl: fullWebhookUrl
    })
    
    const response = await fetch(`https://api.telegram.org/bot${botToken}/setWebhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: fullWebhookUrl,
        allowed_updates: ['message', 'callback_query'],
        drop_pending_updates: true
      }),
    })
    
    const data = await response.json()
    
    if (!data.ok) {
      return {
        success: false,
        error: data.description || 'Failed to set webhook'
      }
    }
    
    return {
      success: true,
      webhook_info: data.result
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}

export async function getWebhookInfo(botToken) {
  try {
    const response = await fetch(`https://api.telegram.org/bot${botToken}/getWebhookInfo`)
    const data = await response.json()
    
    if (!data.ok) {
      return {
        success: false,
        error: data.description
      }
    }
    
    return {
      success: true,
      webhook_info: data.result
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}

export async function deleteWebhook(botToken) {
  try {
    const response = await fetch(`https://api.telegram.org/bot${botToken}/deleteWebhook`, {
      method: 'POST'
    })
    const data = await response.json()
    
    return {
      success: data.ok,
      result: data.result
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}

export async function sendTelegramMessage(chatId, messageData) {
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    
    const response = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: chatId,
        parse_mode: 'Markdown',
        ...messageData
      })
    })
    
    const data = await response.json()
    
    if (!data.ok) {
      throw new Error(data.description || 'Failed to send message')
    }
    
    return data.result
  } catch (error) {
    console.error('Error sending Telegram message:', error)
    throw error
  }
}

export async function sendTelegramVideo(chatId, videoUrl, caption) {
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    
    const response = await fetch(`https://api.telegram.org/bot${botToken}/sendVideo`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: chatId,
        video: videoUrl,
        caption: caption
      })
    })
    
    const data = await response.json()
    
    if (!data.ok) {
      throw new Error(data.description || 'Failed to send video')
    }
    
    return data.result
  } catch (error) {
    console.error('Error sending Telegram video:', error)
    throw error
  }
}

/**
 * Send a photo to Telegram by downloading from URL first
 * @param {string} chatId - Chat ID to send to
 * @param {string} photoUrl - URL of the photo to download and send
 * @param {string} caption - Caption for the photo
 * @param {Object} options - Additional Telegram options
 * @returns {Object} Telegram API response
 */
export async function sendTelegramPhoto(chatId, photoUrl, caption, options = {}) {
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    
    console.log(`📸 Downloading photo from: ${photoUrl}`)
    
    // Download the photo first
    const photoResponse = await fetch(photoUrl)
    if (!photoResponse.ok) {
      throw new Error(`Failed to download photo: ${photoResponse.status} ${photoResponse.statusText}`)
    }
    
    const photoBuffer = await photoResponse.arrayBuffer()
    console.log(`📁 Photo downloaded, size: ${photoBuffer.byteLength} bytes`)
    
    // Create form data
    const formData = new FormData()
    formData.append('chat_id', chatId)
    formData.append('photo', new Blob([photoBuffer]), 'photo.png')
    
    if (caption) {
      formData.append('caption', caption)
      formData.append('parse_mode', 'Markdown')
    }
    
    // Add any additional options
    Object.entries(options).forEach(([key, value]) => {
      if (key !== 'chat_id' && key !== 'photo' && key !== 'caption') {
        formData.append(key, typeof value === 'object' ? JSON.stringify(value) : value)
      }
    })
    
    console.log(`📤 Sending photo to chat ${chatId}`)
    
    const response = await fetch(`https://api.telegram.org/bot${botToken}/sendPhoto`, {
      method: 'POST',
      body: formData
    })
    
    const data = await response.json()
    
    if (!data.ok) {
      throw new Error(data.description || 'Failed to send photo')
    }
    
    console.log(`✅ Photo sent successfully`)
    return data.result
    
  } catch (error) {
    console.error('❌ Error sending Telegram photo:', error)
    throw error
  }
}

/**
 * Send a video to Telegram by downloading from URL first
 * @param {string} chatId - Chat ID to send to
 * @param {string} videoUrl - URL of the video to download and send
 * @param {string} caption - Caption for the video
 * @param {Object} options - Additional Telegram options
 * @returns {Object} Telegram API response
 */
export async function sendTelegramVideoFile(chatId, videoUrl, caption, options = {}) {
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    
    console.log(`🎥 Downloading video from: ${videoUrl}`)
    
    // Download the video first
    const videoResponse = await fetch(videoUrl)
    if (!videoResponse.ok) {
      throw new Error(`Failed to download video: ${videoResponse.status} ${videoResponse.statusText}`)
    }
    
    const videoBuffer = await videoResponse.arrayBuffer()
    console.log(`📁 Video downloaded, size: ${videoBuffer.byteLength} bytes`)
    
    // Create form data
    const formData = new FormData()
    formData.append('chat_id', chatId)
    formData.append('video', new Blob([videoBuffer]), 'video.mp4')
    
    if (caption) {
      formData.append('caption', caption)
      formData.append('parse_mode', 'Markdown')
    }
    
    // Add any additional options
    Object.entries(options).forEach(([key, value]) => {
      if (key !== 'chat_id' && key !== 'video' && key !== 'caption') {
        formData.append(key, typeof value === 'object' ? JSON.stringify(value) : value)
      }
    })
    
    console.log(`📤 Sending video to chat ${chatId}`)
    
    const response = await fetch(`https://api.telegram.org/bot${botToken}/sendVideo`, {
      method: 'POST',
      body: formData
    })
    
    const data = await response.json()
    
    if (!data.ok) {
      throw new Error(data.description || 'Failed to send video')
    }
    
    console.log(`✅ Video sent successfully`)
    return data.result
    
  } catch (error) {
    console.error('❌ Error sending Telegram video:', error)
    throw error
  }
}

/**
 * Universal media sending function - similar to your Python example
 * @param {string} chatId - Chat ID to send to
 * @param {string} text - Message text or caption
 * @param {Object} options - Message options
 * @param {string} messageContentType - Type: "text", "photo", "video"
 * @param {string} mediaUrl - URL of media to download and send
 * @param {string} mediaType - MIME type of media
 * @param {string} caption - Caption override
 * @returns {Object} Telegram API response
 */
export async function sendMessage(
  chatId,
  text = '',
  options = {},
  messageContentType = 'text',
  mediaUrl = null,
  mediaType = null,
  caption = null
) {
  try {
    console.log('\n=== Telegram API Request Validation ===')
    console.log(`Chat ID: ${chatId}`)
    console.log(`Message length: ${text?.length || 0} characters`)
    console.log(`Message content type: ${messageContentType}`)
    console.log(`Media URL: ${mediaUrl}`)
    
    // Input validation
    if (!chatId) {
      throw new Error('Chat ID is required')
    }
    
    const finalCaption = caption || text
    
    // Handle different message types
    switch (messageContentType.toLowerCase()) {
      case 'photo':
      case 'image':
        if (!mediaUrl) {
          throw new Error('media_url is required for photo messages')
        }
        console.log('📸 Sending photo message...')
        return await sendTelegramPhoto(chatId, mediaUrl, finalCaption, options)
        
      case 'video':
        if (!mediaUrl) {
          throw new Error('media_url is required for video messages')
        }
        console.log('🎥 Sending video message...')
        return await sendTelegramVideoFile(chatId, mediaUrl, finalCaption, options)
        
      case 'text':
      default:
        if (!text) {
          throw new Error('Text is required for text messages')
        }
        console.log('💬 Sending text message...')
        return await sendTelegramMessage(chatId, {
          text: text,
          ...options
        })
    }
    
  } catch (error) {
    console.error('\n❌ Error in sendMessage:', error)
    console.error(`Error type: ${error.constructor.name}`)
    console.error(`Error message: ${error.message}`)
    throw error
  }
} 