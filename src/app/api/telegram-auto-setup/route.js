import { NextResponse } from 'next/server'
import { validateBotToken, setBotWebhook } from '../../../lib/telegram-helper'

export async function POST(request) {
  try {
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    const webhookUrl = process.env.WEBHOOK_URL
    
    if (!botToken) {
      return NextResponse.json({ 
        success: false, 
        error: 'TELEGRAM_BOT_TOKEN not found in environment variables' 
      }, { status: 500 })
    }

    if (!webhookUrl) {
      return NextResponse.json({ 
        success: false, 
        error: 'WEBHOOK_URL not found in environment variables. Set it in your .env file.' 
      }, { status: 400 })
    }

    // Validate bot token
    const validation = await validateBotToken(botToken)
    if (!validation.success) {
      return NextResponse.json(validation, { status: 400 })
    }

    // Set webhook using env variable
    const webhookResult = await setBotWebhook(botToken, webhookUrl)
    
    return NextResponse.json({
      success: webhookResult.success,
      message: webhookResult.success ? 'Webhook set automatically using WEBHOOK_URL env variable! 🚀' : 'Failed to set webhook',
      bot_info: validation.bot_info,
      webhook_url: `${webhookUrl}/api/telegram-bot`,
      webhook_info: webhookResult.webhook_info,
      error: webhookResult.error
    })

  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: error.message 
    }, { status: 500 })
  }
} 