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

  // Get resume and job from request body
  const { resume, job } = body

  if (!resume || !job) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Resume and job description are required'
    })
  }

  // Generate a unique room name and participant identity
  const roomName = `interview-${Date.now()}`
  const participantIdentity = `user-${Math.random().toString(36).substring(7)}`

  // Create room with metadata containing resume and job
  const roomMetadata = JSON.stringify({ resume, job })

  // Create room service client to create room with metadata
  const wsUrl = livekitUrl as string
  const httpUrl = wsUrl.replace('wss://', 'https://').replace('ws://', 'http://')

  const roomService = new RoomServiceClient(httpUrl, apiKey, apiSecret)

  try {
    await roomService.createRoom({
      name: roomName,
      metadata: roomMetadata,
      emptyTimeout: 300, // 5 minutes
      maxParticipants: 2
    })
  } catch (error: any) {
    console.error('Failed to create room:', error)
    // Room might already exist, continue anyway
  }

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
