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

      <!-- Main State Display -->
      <div class="bg-slate-800/50 rounded-2xl border border-slate-700 p-8 mb-6">

        <!-- Idle State -->
        <div v-if="interviewState === 'idle'" class="text-center">
          <div class="w-24 h-24 mx-auto mb-6 bg-slate-700 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">Ready to Practice?</h2>
          <p class="text-slate-400 mb-6">Start your mock interview with Sarah Mitchell</p>
          <button
            @click="startInterview"
            class="px-8 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-xl transition-all transform hover:scale-105"
          >
            Start Interview
          </button>
        </div>

        <!-- Initializing State -->
        <div v-else-if="interviewState === 'initializing'" class="text-center">
          <div class="w-24 h-24 mx-auto mb-6 relative">
            <div class="absolute inset-0 bg-yellow-500/20 rounded-full animate-ping"></div>
            <div class="relative w-full h-full bg-yellow-500/30 rounded-full flex items-center justify-center">
              <svg class="w-12 h-12 text-yellow-500 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">Initializing...</h2>
          <p class="text-slate-400">Connecting to the interview room</p>
          <div class="mt-4 flex justify-center gap-1">
            <span class="w-2 h-2 bg-yellow-500 rounded-full animate-bounce" style="animation-delay: 0s"></span>
            <span class="w-2 h-2 bg-yellow-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></span>
            <span class="w-2 h-2 bg-yellow-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
          </div>
        </div>

        <!-- Speaking State (Agent is speaking) -->
        <div v-else-if="interviewState === 'speaking'" class="text-center">
          <div class="w-32 h-32 mx-auto mb-6 relative">
            <!-- Animated rings -->
            <div class="absolute inset-0 bg-emerald-500/20 rounded-full animate-ping"></div>
            <div class="absolute inset-2 bg-emerald-500/30 rounded-full animate-pulse"></div>
            <div class="relative w-full h-full bg-emerald-600 rounded-full flex items-center justify-center">
              <span class="text-white text-3xl font-bold">SM</span>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">Sarah is Speaking</h2>
          <p class="text-emerald-400">Listen to the question...</p>
          <!-- Sound wave animation -->
          <div class="mt-6 flex justify-center items-end gap-1 h-12">
            <span v-for="i in 7" :key="i"
              class="w-2 bg-emerald-500 rounded-full animate-pulse"
              :style="{
                height: `${20 + Math.random() * 30}px`,
                animationDelay: `${i * 0.1}s`
              }"
            ></span>
          </div>
        </div>

        <!-- Thinking State (Agent is processing) -->
        <div v-else-if="interviewState === 'thinking'" class="text-center">
          <div class="w-32 h-32 mx-auto mb-6 relative">
            <div class="absolute inset-0 bg-purple-500/20 rounded-full animate-pulse"></div>
            <div class="relative w-full h-full bg-purple-600 rounded-full flex items-center justify-center">
              <span class="text-white text-3xl font-bold">SM</span>
            </div>
            <!-- Thinking dots -->
            <div class="absolute -bottom-1 -right-1 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
              <div class="flex gap-0.5">
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0s"></span>
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0.1s"></span>
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
              </div>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">Sarah is Thinking</h2>
          <p class="text-purple-400">Processing your response...</p>
          <!-- Thinking animation -->
          <div class="mt-6 flex justify-center gap-2">
            <span class="w-3 h-3 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0s"></span>
            <span class="w-3 h-3 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.15s"></span>
            <span class="w-3 h-3 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.3s"></span>
          </div>
        </div>

        <!-- Listening State (Agent is listening) -->
        <div v-else-if="interviewState === 'listening'" class="text-center">
          <div class="w-32 h-32 mx-auto mb-6 relative">
            <div class="relative w-full h-full bg-slate-700 rounded-full flex items-center justify-center border-4 border-blue-500">
              <span class="text-white text-3xl font-bold">SM</span>
            </div>
            <!-- Listening indicator -->
            <div class="absolute -bottom-1 -right-1 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">Your Turn</h2>
          <p class="text-blue-400">Sarah is listening to you...</p>
          <!-- Mic level indicator -->
          <div class="mt-6 max-w-xs mx-auto">
            <div class="h-3 bg-slate-700 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-blue-500 to-emerald-500 transition-all duration-100 rounded-full"
                :style="{ width: `${audioLevel}%` }"
              ></div>
            </div>
            <p class="text-slate-500 text-sm mt-2">Microphone level</p>
          </div>
        </div>

        <!-- User Speaking State -->
        <div v-else-if="interviewState === 'userSpeaking'" class="text-center">
          <div class="w-32 h-32 mx-auto mb-6 relative">
            <div class="absolute inset-0 bg-blue-500/20 rounded-full animate-ping"></div>
            <div class="relative w-full h-full bg-blue-600 rounded-full flex items-center justify-center">
              <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">You're Speaking</h2>
          <p class="text-blue-400">Keep going, Sarah is listening...</p>
          <!-- Sound wave animation -->
          <div class="mt-6 flex justify-center items-end gap-1 h-12">
            <span v-for="i in 7" :key="i"
              class="w-2 bg-blue-500 rounded-full"
              :style="{
                height: `${Math.max(8, audioLevel * 0.5 + Math.random() * 20)}px`,
                transition: 'height 0.1s'
              }"
            ></span>
          </div>
        </div>

        <!-- End Interview Button (when connected) -->
        <div v-if="interviewState !== 'idle' && interviewState !== 'initializing'" class="mt-8 pt-6 border-t border-slate-700 flex justify-center gap-4">
          <button
            @click="toggleMute"
            :class="[
              'px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
              isMuted ? 'bg-red-600 hover:bg-red-500 text-white' : 'bg-slate-700 hover:bg-slate-600 text-white'
            ]"
          >
            <svg v-if="!isMuted" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
            {{ isMuted ? 'Unmute' : 'Mute' }}
          </button>
          <button
            @click="endInterview"
            class="px-6 py-2 bg-red-600 hover:bg-red-500 text-white font-medium rounded-lg transition-colors"
          >
            End Interview
          </button>
        </div>
      </div>

      <!-- Status Bar -->
      <div v-if="interviewState !== 'idle'" class="bg-slate-800/50 rounded-xl border border-slate-700 p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div :class="[
              'w-2 h-2 rounded-full',
              interviewState === 'initializing' ? 'bg-yellow-500' :
              interviewState === 'thinking' ? 'bg-purple-500' :
              interviewState === 'speaking' ? 'bg-emerald-500' :
              interviewState === 'userSpeaking' ? 'bg-blue-500' :
              'bg-emerald-500'
            ]"></div>
            <span class="text-slate-400 text-sm">
              {{ statusText }}
            </span>
          </div>
          <div class="text-slate-500 text-sm">
            {{ formatDuration(interviewDuration) }}
          </div>
        </div>
      </div>

      <!-- Transcription -->
      <div v-if="interviewState !== 'idle' && interviewState !== 'initializing'" class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
        <h2 class="text-white font-medium mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          Conversation
        </h2>
        <div class="space-y-4 max-h-80 overflow-y-auto" ref="transcriptContainer">
          <div
            v-for="(message, index) in transcript"
            :key="index"
            :class="[
              'p-4 rounded-xl',
              message.speaker === 'agent'
                ? 'bg-emerald-900/30 border border-emerald-800/50 ml-0 mr-12'
                : 'bg-blue-900/30 border border-blue-800/50 ml-12 mr-0'
            ]"
          >
            <p class="text-xs text-slate-400 mb-1 flex items-center gap-2">
              <span :class="[
                'w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold',
                message.speaker === 'agent' ? 'bg-emerald-600 text-white' : 'bg-blue-600 text-white'
              ]">
                {{ message.speaker === 'agent' ? 'SM' : 'U' }}
              </span>
              {{ message.speaker === 'agent' ? 'Sarah Mitchell' : 'You' }}
            </p>
            <p class="text-white">{{ message.text }}</p>
          </div>
          <div v-if="transcript.length === 0" class="text-slate-500 text-center py-8">
            <svg class="w-12 h-12 mx-auto mb-3 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Waiting for the conversation to begin...
          </div>
        </div>
      </div>

      <!-- Instructions (when idle) -->
      <div v-if="interviewState === 'idle'" class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
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
import { Room, RoomEvent, Track, ConnectionState, RemoteTrack, RemoteParticipant, Participant } from 'livekit-client'

const config = useRuntimeConfig()

// Interview states: idle -> initializing -> listening/thinking/speaking/userSpeaking
type InterviewState = 'idle' | 'initializing' | 'listening' | 'thinking' | 'speaking' | 'userSpeaking'

const interviewState = ref<InterviewState>('idle')
const isMuted = ref(false)
const audioLevel = ref(0)
const transcript = ref<Array<{ speaker: 'agent' | 'user', text: string }>>([])
const transcriptContainer = ref<HTMLElement | null>(null)
const interviewDuration = ref(0)
const agentState = ref<string>('listening') // State from backend

let room: Room | null = null
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let durationInterval: NodeJS.Timeout | null = null

const statusText = computed(() => {
  switch (interviewState.value) {
    case 'initializing': return 'Connecting to interview room...'
    case 'thinking': return 'Sarah is thinking...'
    case 'speaking': return 'Sarah is speaking'
    case 'listening': return 'Waiting for your response'
    case 'userSpeaking': return 'You are speaking'
    default: return ''
  }
})

const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Update interview state based on agent state from backend
const updateInterviewState = () => {
  if (interviewState.value === 'idle' || interviewState.value === 'initializing') return

  switch (agentState.value) {
    case 'speaking':
      interviewState.value = 'speaking'
      break
    case 'thinking':
      interviewState.value = 'thinking'
      break
    case 'listening':
      // Only set to listening if user is not currently speaking
      if (interviewState.value !== 'userSpeaking') {
        interviewState.value = 'listening'
      }
      break
    default:
      interviewState.value = 'listening'
  }
}

const startInterview = async () => {
  interviewState.value = 'initializing'

  try {
    // Get token from API
    const { token } = await $fetch<{ token: string }>('/api/token')

    // Create and connect to room
    room = new Room()

    room.on(RoomEvent.ConnectionStateChanged, (state: ConnectionState) => {
      if (state === ConnectionState.Connected) {
        interviewState.value = 'listening'
        // Start duration timer
        durationInterval = setInterval(() => {
          interviewDuration.value++
        }, 1000)
      } else if (state === ConnectionState.Disconnected) {
        interviewState.value = 'idle'
      }
    })

    // Handle agent audio - attach audio element
    room.on(RoomEvent.TrackSubscribed, (track: RemoteTrack, _publication, participant: RemoteParticipant) => {
      if (track.kind === Track.Kind.Audio && participant.identity.startsWith('agent')) {
        const audioElement = track.attach()
        document.body.appendChild(audioElement)
      }
    })

    room.on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack) => {
      if (track.kind === Track.Kind.Audio) {
        track.detach()
      }
    })

    // Listen for agent state changes from backend (the reliable source)
    room.on(RoomEvent.ParticipantAttributesChanged, (changedAttributes: Record<string, string>, participant: Participant) => {
      console.log('Attributes changed:', participant.identity, changedAttributes)
      if (participant.identity.startsWith('agent') && changedAttributes.agent_state) {
        agentState.value = changedAttributes.agent_state
        console.log('Agent state from backend:', agentState.value)
        updateInterviewState()
      }
    })

    // Also check existing participants for attributes when they connect
    room.on(RoomEvent.ParticipantConnected, (participant: RemoteParticipant) => {
      console.log('Participant connected:', participant.identity, participant.attributes)
      if (participant.identity.startsWith('agent')) {
        const state = participant.attributes?.agent_state
        if (state) {
          agentState.value = state
          updateInterviewState()
        }
      }
    })

    // Check all remote participants on connect for agent
    room.on(RoomEvent.Connected, () => {
      room?.remoteParticipants.forEach((participant) => {
        console.log('Existing participant:', participant.identity, participant.attributes)
        if (participant.identity.startsWith('agent')) {
          const state = participant.attributes?.agent_state
          if (state) {
            agentState.value = state
            updateInterviewState()
          }
        }
      })
    })

    // Handle active speaker changes (for detecting user speaking)
    room.on(RoomEvent.ActiveSpeakersChanged, (speakers) => {
      const userIsSpeaking = speakers.some(s => !s.identity.startsWith('agent'))

      // Only update to userSpeaking if agent is in listening state
      if (userIsSpeaking && agentState.value === 'listening') {
        interviewState.value = 'userSpeaking'
      } else {
        updateInterviewState()
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

    await room.connect(config.public.livekitUrl, token)

    // Enable microphone
    await room.localParticipant.setMicrophoneEnabled(true)

    // Set up audio level monitoring
    setupAudioMonitoring()

  } catch (error) {
    console.error('Failed to connect:', error)
    interviewState.value = 'idle'
  }
}

const endInterview = async () => {
  if (room) {
    await room.disconnect()
    room = null
  }
  if (durationInterval) {
    clearInterval(durationInterval)
    durationInterval = null
  }
  interviewState.value = 'idle'
  transcript.value = []
  audioLevel.value = 0
  interviewDuration.value = 0
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
  let silenceTimer: NodeJS.Timeout | null = null

  const updateLevel = () => {
    if (!analyser || interviewState.value === 'idle') return
    analyser.getByteFrequencyData(dataArray)
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length
    audioLevel.value = Math.min(100, average * 1.5)

    // Only handle user speaking detection when agent is listening
    if (agentState.value === 'listening') {
      if (audioLevel.value > 15) {
        // User is speaking
        interviewState.value = 'userSpeaking'
        if (silenceTimer) {
          clearTimeout(silenceTimer)
          silenceTimer = null
        }
      } else if (audioLevel.value < 10 && interviewState.value === 'userSpeaking') {
        // User stopped speaking - wait a bit before switching to listening
        if (!silenceTimer) {
          silenceTimer = setTimeout(() => {
            if (agentState.value === 'listening') {
              interviewState.value = 'listening'
            }
            silenceTimer = null
          }, 800)
        }
      }
    } else {
      // Agent is speaking or thinking - follow agent state
      updateInterviewState()
    }

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
  if (durationInterval) {
    clearInterval(durationInterval)
  }
})
</script>
