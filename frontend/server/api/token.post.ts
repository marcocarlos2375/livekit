import { AccessToken } from 'livekit-server-sdk'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)

  const apiKey = config.livekitApiKey
  const apiSecret = config.livekitApiSecret

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

  // Create access token with metadata containing the IDs
  const token = new AccessToken(apiKey, apiSecret, {
    identity: participantIdentity,
    ttl: '1h',
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
