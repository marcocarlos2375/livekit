<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Header -->
    <header class="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold text-white">Interview Simulator</h1>
        <p class="text-slate-400 text-sm">Practice with AI interviewer Sarah Mitchell</p>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">
      <!-- Connection Status Card -->
      <div class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6 mb-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <div
              :class="[
                'w-3 h-3 rounded-full',
                connectionState === 'connected' ? 'bg-green-500 animate-pulse' :
                connectionState === 'connecting' ? 'bg-yellow-500 animate-pulse' :
                'bg-slate-500'
              ]"
            ></div>
            <span class="text-white font-medium">
              {{ connectionState === 'connected' ? 'Interview in Progress' :
                 connectionState === 'connecting' ? 'Connecting...' :
                 'Ready to Start' }}
            </span>
          </div>

          <button
            v-if="connectionState === 'disconnected'"
            @click="startInterview"
            :disabled="isLoading"
            class="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-600 text-white font-medium rounded-lg transition-colors"
          >
            {{ isLoading ? 'Starting...' : 'Start Interview' }}
          </button>

          <button
            v-else
            @click="endInterview"
            class="px-6 py-2 bg-red-600 hover:bg-red-500 text-white font-medium rounded-lg transition-colors"
          >
            End Interview
          </button>
        </div>

        <!-- Interviewer Info -->
        <div v-if="connectionState === 'connected'" class="flex items-center gap-4 p-4 bg-slate-700/50 rounded-xl">
          <div class="w-12 h-12 bg-emerald-600 rounded-full flex items-center justify-center">
            <span class="text-white text-lg font-bold">SM</span>
          </div>
          <div>
            <p class="text-white font-medium">Sarah Mitchell</p>
            <p class="text-slate-400 text-sm">Engineering Hiring Manager</p>
          </div>
          <div class="ml-auto flex items-center gap-2">
            <div v-if="agentSpeaking" class="flex items-center gap-1">
              <span class="w-1 h-4 bg-emerald-500 rounded-full animate-pulse"></span>
              <span class="w-1 h-6 bg-emerald-500 rounded-full animate-pulse" style="animation-delay: 0.1s"></span>
              <span class="w-1 h-4 bg-emerald-500 rounded-full animate-pulse" style="animation-delay: 0.2s"></span>
            </div>
            <span class="text-slate-400 text-sm">{{ agentSpeaking ? 'Speaking...' : 'Listening' }}</span>
          </div>
        </div>
      </div>

      <!-- Audio Visualization -->
      <div v-if="connectionState === 'connected'" class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6 mb-6">
        <h2 class="text-white font-medium mb-4">Your Microphone</h2>
        <div class="flex items-center gap-4">
          <button
            @click="toggleMute"
            :class="[
              'w-14 h-14 rounded-full flex items-center justify-center transition-colors',
              isMuted ? 'bg-red-600 hover:bg-red-500' : 'bg-emerald-600 hover:bg-emerald-500'
            ]"
          >
            <svg v-if="!isMuted" class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            <svg v-else class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
          </button>
          <div class="flex-1">
            <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                class="h-full bg-emerald-500 transition-all duration-100"
                :style="{ width: `${audioLevel}%` }"
              ></div>
            </div>
            <p class="text-slate-400 text-sm mt-2">{{ isMuted ? 'Microphone muted' : 'Speak clearly into your microphone' }}</p>
          </div>
        </div>
      </div>

      <!-- Transcription -->
      <div v-if="connectionState === 'connected'" class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
        <h2 class="text-white font-medium mb-4">Conversation</h2>
        <div class="space-y-4 max-h-96 overflow-y-auto" ref="transcriptContainer">
          <div
            v-for="(message, index) in transcript"
            :key="index"
            :class="[
              'p-4 rounded-xl',
              message.speaker === 'agent' ? 'bg-emerald-900/30 border border-emerald-800' : 'bg-slate-700/50'
            ]"
          >
            <p class="text-xs text-slate-400 mb-1">{{ message.speaker === 'agent' ? 'Sarah Mitchell' : 'You' }}</p>
            <p class="text-white">{{ message.text }}</p>
          </div>
          <div v-if="transcript.length === 0" class="text-slate-500 text-center py-8">
            Waiting for the interview to begin...
          </div>
        </div>
      </div>

      <!-- Instructions (when not connected) -->
      <div v-if="connectionState === 'disconnected'" class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
        <h2 class="text-white font-medium mb-4">How it works</h2>
        <ol class="space-y-3 text-slate-300">
          <li class="flex gap-3">
            <span class="w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">1</span>
            <span>Click "Start Interview" to connect with Sarah, your AI interviewer</span>
          </li>
          <li class="flex gap-3">
            <span class="w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">2</span>
            <span>Allow microphone access when prompted</span>
          </li>
          <li class="flex gap-3">
            <span class="w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">3</span>
            <span>Sarah will introduce herself and ask questions based on your resume</span>
          </li>
          <li class="flex gap-3">
            <span class="w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center text-white text-sm flex-shrink-0">4</span>
            <span>Answer naturally - it's just like a real interview!</span>
          </li>
        </ol>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { Room, RoomEvent, Track, ConnectionState, RemoteTrack, RemoteParticipant } from 'livekit-client'

const config = useRuntimeConfig()

const connectionState = ref<'disconnected' | 'connecting' | 'connected'>('disconnected')
const isLoading = ref(false)
const isMuted = ref(false)
const audioLevel = ref(0)
const agentSpeaking = ref(false)
const transcript = ref<Array<{ speaker: 'agent' | 'user', text: string }>>([])
const transcriptContainer = ref<HTMLElement | null>(null)

let room: Room | null = null
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null

const startInterview = async () => {
  isLoading.value = true

  try {
    // Get token from API
    const { token } = await $fetch<{ token: string }>('/api/token')

    // Create and connect to room
    room = new Room()

    room.on(RoomEvent.ConnectionStateChanged, (state: ConnectionState) => {
      if (state === ConnectionState.Connected) {
        connectionState.value = 'connected'
      } else if (state === ConnectionState.Disconnected) {
        connectionState.value = 'disconnected'
      }
    })

    // Handle agent audio
    room.on(RoomEvent.TrackSubscribed, (track: RemoteTrack, _publication, participant: RemoteParticipant) => {
      if (track.kind === Track.Kind.Audio && participant.identity.startsWith('agent')) {
        const audioElement = track.attach()
        document.body.appendChild(audioElement)
        agentSpeaking.value = true
      }
    })

    room.on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack) => {
      if (track.kind === Track.Kind.Audio) {
        track.detach()
        agentSpeaking.value = false
      }
    })

    // Handle transcription
    room.on(RoomEvent.TranscriptionReceived, (segments) => {
      for (const segment of segments) {
        if (segment.final) {
          const isAgent = segment.participantIdentity?.startsWith('agent')
          transcript.value.push({
            speaker: isAgent ? 'agent' : 'user',
            text: segment.text
          })
          // Auto-scroll
          nextTick(() => {
            if (transcriptContainer.value) {
              transcriptContainer.value.scrollTop = transcriptContainer.value.scrollHeight
            }
          })
        }
      }
    })

    connectionState.value = 'connecting'
    await room.connect(config.public.livekitUrl, token)

    // Enable microphone
    await room.localParticipant.setMicrophoneEnabled(true)

    // Set up audio level monitoring
    setupAudioMonitoring()

  } catch (error) {
    console.error('Failed to connect:', error)
    connectionState.value = 'disconnected'
  } finally {
    isLoading.value = false
  }
}

const endInterview = async () => {
  if (room) {
    await room.disconnect()
    room = null
  }
  connectionState.value = 'disconnected'
  transcript.value = []
  audioLevel.value = 0
  agentSpeaking.value = false
}

const toggleMute = async () => {
  if (room) {
    isMuted.value = !isMuted.value
    await room.localParticipant.setMicrophoneEnabled(!isMuted.value)
  }
}

const setupAudioMonitoring = () => {
  if (!room) return

  const localTrack = room.localParticipant.getTrackPublication(Track.Source.Microphone)
  if (!localTrack?.track) return

  const mediaStream = new MediaStream([localTrack.track.mediaStreamTrack])
  audioContext = new AudioContext()
  analyser = audioContext.createAnalyser()
  const source = audioContext.createMediaStreamSource(mediaStream)
  source.connect(analyser)
  analyser.fftSize = 256

  const dataArray = new Uint8Array(analyser.frequencyBinCount)

  const updateLevel = () => {
    if (!analyser || connectionState.value !== 'connected') return
    analyser.getByteFrequencyData(dataArray)
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length
    audioLevel.value = Math.min(100, average * 1.5)
    requestAnimationFrame(updateLevel)
  }
  updateLevel()
}

onUnmounted(() => {
  if (room) {
    room.disconnect()
  }
  if (audioContext) {
    audioContext.close()
  }
})
</script>
