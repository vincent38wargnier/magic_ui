export const dynamic = 'force-dynamic'
export const fetchCache = 'force-no-store'

import { Bot, webhookCallback } from 'grammy'

const token = process.env.TELEGRAM_BOT_TOKEN

if (!token) {
  throw new Error('TELEGRAM_BOT_TOKEN environment variable not found.')
}

const bot = new Bot(token)

// Simple middleware to log incoming messages
bot.use(async (ctx, next) => {
  console.log('=================== TELEGRAM MESSAGE ===================')
  console.log('Received at:', new Date().toISOString())
  
  if (ctx.message?.text) {
    console.log('👤 User:', {
      id: ctx.from?.id,
      username: ctx.from?.username,
      first_name: ctx.from?.first_name
    })
    console.log('💬 Message:', ctx.message.text)
    console.log('📍 Chat ID:', ctx.chat?.id)
  }
  
  await next()
})

// Handle all text messages
bot.on('message:text', async (ctx) => {
  const userMessage = ctx.message.text
  const userId = ctx.from.id
  const chatId = ctx.chat.id
  
  console.log(`📝 Processing message: "${userMessage}" from user ${userId}`)
  
  try {
    // Send immediate acknowledgment to user first
    await ctx.reply('Message processing...')
    
    // Send message to conversation agent (fire and forget)
    fetch('http://localhost:8000/conversation_agent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage,
        chatId: chatId,
        userId: userId
      })
    }).catch(error => {
      console.error('❌ Error calling conversation agent:', error)
    })
    
  } catch (error) {
    console.error('❌ Error sending request:', error)
    await ctx.reply('Sorry, I could not process your request right now. Please try again later.')
  }
})

// Error handling
bot.catch((err) => {
  console.error('❌ Bot error:', err)
})

export const POST = webhookCallback(bot, 'std/http') 