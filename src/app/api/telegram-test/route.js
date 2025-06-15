import { NextResponse } from 'next/server'
import { validateBotToken, getWebhookInfo } from '../../../lib/telegram-helper'

export async function GET(request) {
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    
    if (!botToken) {
      return NextResponse.json({ 
        success: false, 
        error: 'TELEGRAM_BOT_TOKEN not found in environment variables',
        message: 'Add TELEGRAM_BOT_TOKEN to your .env.local file'
      }, { status: 500 })
    }

    // Test bot token
    const validation = await validateBotToken(botToken)
    
    if (!validation.success) {
      return NextResponse.json({
        success: false,
        error: validation.error,
        message: 'Bot token is invalid'
      }, { status: 400 })
    }

    // Get current webhook info
    const webhookInfo = await getWebhookInfo(botToken)

    return NextResponse.json({
      success: true,
      message: 'Bot token is valid! ✅',
      bot_info: validation.bot_info,
      webhook_info: webhookInfo.webhook_info,
      next_steps: [
        '1. Go to /telegram-admin to set up your webhook',
        '2. Use ngrok for local development: ngrok http 3000',
        '3. Set webhook URL in the admin panel',
        '4. Test your bot!'
      ]
    })

  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: error.message 
    }, { status: 500 })
  }
} 