import { AccessToken, RoomServiceClient } from 'livekit-server-sdk'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)

  const apiKey = config.livekitApiKey
  const apiSecret = config.livekitApiSecret
  const livekitUrl = config.public.livekitUrl

  if (!apiKey || !apiSecret) {
    throw createError({
      statusCode: 500,
      statusMessage: 'LiveKit API credentials not configured'
    })
  }

  // Get resume, job, voice IDs, and language from request body
  const { resumeId, jobId, voiceId, language } = body

  if (!resumeId || !jobId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Resume ID and job ID are required'
    })
  }

  // Generate a unique room name and participant identity
  const roomName = `interview-${Date.now()}`
  const participantIdentity = `user-${Math.random().toString(36).substring(7)}`

  // Create room with auto-cleanup settings
  // Handle both local (ws://) and cloud (wss://) URLs
  const httpUrl = livekitUrl
    .replace('wss://', 'https://')
    .replace('ws://', 'http://')
  const roomService = new RoomServiceClient(httpUrl, apiKey, apiSecret)

  try {
    await roomService.createRoom({
      name: roomName,
      emptyTimeout: 60,          // Delete room 60 seconds after last participant leaves
      maxParticipants: 2,        // Only user + agent
      metadata: JSON.stringify({ resumeId, jobId, language: language || 'en' })
    })
  } catch (error) {
    console.log('Room may already exist or will be created on join:', error)
  }

  // Create access token with metadata containing the IDs
  const token = new AccessToken(apiKey, apiSecret, {
    identity: participantIdentity,
    ttl: '30m',  // Token expires in 30 minutes
    metadata: JSON.stringify({ resumeId, jobId, voiceId: voiceId || 'aura-2-thalia-en', language: language || 'en' })
  })

  token.addGrant({
    roomJoin: true,
    room: roomName,
    canPublish: true,
    canSubscribe: true,
    canPublishData: true
  })

  return {
    token: await token.toJwt(),
    room: roomName,
    identity: participantIdentity
  }
})
