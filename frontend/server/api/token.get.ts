import { AccessToken } from 'livekit-server-sdk'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()

  const apiKey = config.livekitApiKey
  const apiSecret = config.livekitApiSecret

  if (!apiKey || !apiSecret) {
    throw createError({
      statusCode: 500,
      statusMessage: 'LiveKit API credentials not configured'
    })
  }

  // Generate a unique room name and participant identity
  const roomName = `interview-${Date.now()}`
  const participantIdentity = `user-${Math.random().toString(36).substring(7)}`

  // Create access token
  const token = new AccessToken(apiKey, apiSecret, {
    identity: participantIdentity,
    ttl: '1h'
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
