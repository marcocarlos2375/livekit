<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Header -->
    <header class="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold text-white">{{ selectedLanguage === 'fr' ? 'Simulateur d\'Entretien' : 'Interview Simulator' }}</h1>
        <p class="text-slate-400 text-sm">{{ selectedLanguage === 'fr' ? 'Entraînez-vous avec Marie Dubois, recruteuse IA' : 'Practice with AI interviewer Sarah Mitchell' }}</p>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">

      <!-- Setup Phase: Select Resume and Job -->
      <div v-if="interviewState === 'setup'" class="space-y-6">

        <!-- Language Tabs -->
        <div class="flex justify-center gap-2">
          <button
            @click="selectedLanguage = 'en'"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2',
              selectedLanguage === 'en'
                ? 'bg-white text-slate-900'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            ]"
          >
            <span class="text-lg">🇬🇧</span>
            English
          </button>
          <button
            @click="selectedLanguage = 'fr'"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2',
              selectedLanguage === 'fr'
                ? 'bg-white text-slate-900'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            ]"
          >
            <span class="text-lg">🇫🇷</span>
            Français
          </button>
        </div>

        <!-- Resume Selection -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Select Resume
          </h2>

          <!-- Resume Options -->
          <div class="grid gap-3 mb-4">
            <button
              v-for="resume in filteredResumes"
              :key="resume.id"
              @click="selectedResume = resume"
              :class="[
                'p-4 rounded-xl border text-left transition-all',
                selectedResume?.id === resume.id
                  ? 'border-emerald-500 bg-emerald-500/10'
                  : 'border-slate-600 hover:border-slate-500 bg-slate-700/30'
              ]"
            >
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="font-medium text-white">{{ resume.name }}</h3>
                  <p class="text-sm text-slate-400 mt-1">{{ resume.experience[0]?.title }} at {{ resume.experience[0]?.company }}</p>
                  <div class="flex flex-wrap gap-1 mt-2">
                    <span
                      v-for="skill in resume.skills.languages.slice(0, 4)"
                      :key="skill"
                      class="px-2 py-0.5 text-xs bg-slate-600 text-slate-300 rounded"
                    >
                      {{ skill }}
                    </span>
                  </div>
                </div>
                <div v-if="selectedResume?.id === resume.id" class="text-emerald-500">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                </div>
              </div>
            </button>
          </div>

          <!-- Custom Resume Toggle -->
          <button
            @click="showCustomResume = !showCustomResume"
            class="text-sm text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Or paste custom resume JSON
          </button>

          <div v-if="showCustomResume" class="mt-3">
            <textarea
              v-model="customResumeJson"
              placeholder='{"name": "Your Name", "summary": "...", "experience": [...], "skills": {...}}'
              class="w-full h-32 bg-slate-700 border border-slate-600 rounded-lg p-3 text-white text-sm font-mono placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
            ></textarea>
            <button
              @click="parseCustomResume"
              class="mt-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm rounded-lg"
            >
              Use Custom Resume
            </button>
            <p v-if="customResumeError" class="mt-2 text-red-400 text-sm">{{ customResumeError }}</p>
          </div>
        </div>

        <!-- Job Description Selection -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Select Job Description
          </h2>

          <!-- Job Options -->
          <div class="grid gap-3 mb-4">
            <button
              v-for="job in filteredJobs"
              :key="job.id"
              @click="selectedJob = job"
              :class="[
                'p-4 rounded-xl border text-left transition-all',
                selectedJob?.id === job.id
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-slate-600 hover:border-slate-500 bg-slate-700/30'
              ]"
            >
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="font-medium text-white">{{ job.title }}</h3>
                  <p class="text-sm text-slate-400 mt-1">{{ job.company }}</p>
                  <div class="flex flex-wrap gap-1 mt-2">
                    <span
                      v-for="req in job.requirements.must_have.slice(0, 3)"
                      :key="req"
                      class="px-2 py-0.5 text-xs bg-slate-600 text-slate-300 rounded"
                    >
                      {{ req.split(' ').slice(0, 3).join(' ') }}...
                    </span>
                  </div>
                </div>
                <div v-if="selectedJob?.id === job.id" class="text-blue-500">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                </div>
              </div>
            </button>
          </div>

          <!-- Custom Job Toggle -->
          <button
            @click="showCustomJob = !showCustomJob"
            class="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Or paste custom job description JSON
          </button>

          <div v-if="showCustomJob" class="mt-3">
            <textarea
              v-model="customJobJson"
              placeholder='{"title": "Job Title", "company": "...", "requirements": {...}}'
              class="w-full h-32 bg-slate-700 border border-slate-600 rounded-lg p-3 text-white text-sm font-mono placeholder-slate-500 focus:border-blue-500 focus:outline-none"
            ></textarea>
            <button
              @click="parseCustomJob"
              class="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm rounded-lg"
            >
              Use Custom Job
            </button>
            <p v-if="customJobError" class="mt-2 text-red-400 text-sm">{{ customJobError }}</p>
          </div>
        </div>

        <!-- Voice Selection -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            Select Interviewer Voice
          </h2>

          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <button
              v-for="voice in filteredVoices"
              :key="voice.id"
              @click="selectedVoice = voice"
              :class="[
                'p-3 rounded-xl border text-left transition-all',
                selectedVoice?.id === voice.id
                  ? 'border-purple-500 bg-purple-500/10'
                  : 'border-slate-600 hover:border-slate-500 bg-slate-700/30'
              ]"
            >
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-white">{{ voice.name }}</h3>
                  <p class="text-xs text-slate-400 mt-1">{{ voice.description }}</p>
                </div>
                <div v-if="selectedVoice?.id === voice.id" class="text-purple-500">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                </div>
              </div>
            </button>
          </div>
        </div>

        <!-- Start Button -->
        <div class="text-center pt-4">
          <button
            @click="startInterview"
            :disabled="!selectedResume || !selectedJob || !selectedVoice"
            :class="[
              'px-8 py-4 text-lg font-medium rounded-xl transition-all transform',
              selectedResume && selectedJob && selectedVoice
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white hover:scale-105'
                : 'bg-slate-700 text-slate-500 cursor-not-allowed'
            ]"
          >
            <span v-if="selectedResume && selectedJob && selectedVoice">Start Interview</span>
            <span v-else>Select Resume, Job, and Voice to Continue</span>
          </button>
          <p v-if="selectedResume && selectedJob && selectedVoice" class="mt-3 text-slate-400 text-sm">
            Interviewing <span class="text-emerald-400">{{ selectedResume.name }}</span>
            for <span class="text-blue-400">{{ selectedJob.title }}</span> at {{ selectedJob.company }}
            <span class="text-purple-400">({{ selectedVoice.name }} voice)</span>
          </p>
        </div>
      </div>

      <!-- Main State Display (Interview Phase) -->
      <div v-else class="bg-slate-800/50 rounded-2xl border border-slate-700 p-8 mb-6">

        <!-- Initializing State -->
        <div v-if="interviewState === 'initializing'" class="text-center">
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
            <div class="absolute inset-0 bg-emerald-500/20 rounded-full animate-ping"></div>
            <div class="absolute inset-2 bg-emerald-500/30 rounded-full animate-pulse"></div>
            <div class="relative w-full h-full bg-emerald-600 rounded-full flex items-center justify-center">
              <span class="text-white text-3xl font-bold">{{ interviewerInitials }}</span>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">{{ selectedLanguage === 'fr' ? `${interviewerName} parle` : `${interviewerName} is Speaking` }}</h2>
          <p class="text-emerald-400">{{ selectedLanguage === 'fr' ? 'Écoutez la question...' : 'Listen to the question...' }}</p>
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
              <span class="text-white text-3xl font-bold">{{ interviewerInitials }}</span>
            </div>
            <div class="absolute -bottom-1 -right-1 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
              <div class="flex gap-0.5">
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0s"></span>
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0.1s"></span>
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
              </div>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">{{ selectedLanguage === 'fr' ? `${interviewerName} réfléchit` : `${interviewerName} is Thinking` }}</h2>
          <p class="text-purple-400">{{ selectedLanguage === 'fr' ? 'Traitement de votre réponse...' : 'Processing your response...' }}</p>
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
              <span class="text-white text-3xl font-bold">{{ interviewerInitials }}</span>
            </div>
            <div class="absolute -bottom-1 -right-1 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-2">{{ selectedLanguage === 'fr' ? 'À votre tour' : 'Your Turn' }}</h2>
          <p class="text-blue-400">{{ selectedLanguage === 'fr' ? `${interviewerName} vous écoute...` : `${interviewerName} is listening to you...` }}</p>
          <div class="mt-6 max-w-xs mx-auto">
            <div class="h-3 bg-slate-700 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-blue-500 to-emerald-500 transition-all duration-100 rounded-full"
                :style="{ width: `${audioLevel}%` }"
              ></div>
            </div>
            <p class="text-slate-500 text-sm mt-2">{{ selectedLanguage === 'fr' ? 'Niveau du microphone' : 'Microphone level' }}</p>
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
          <h2 class="text-2xl font-bold text-white mb-2">{{ selectedLanguage === 'fr' ? 'Vous parlez' : 'You\'re Speaking' }}</h2>
          <p class="text-blue-400">{{ selectedLanguage === 'fr' ? `Continuez, ${interviewerName} vous écoute...` : `Keep going, ${interviewerName} is listening...` }}</p>
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
        <div v-if="interviewState !== 'setup'" class="mt-8 pt-6 border-t border-slate-700 flex justify-center gap-4">
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
            {{ selectedLanguage === 'fr' ? (isMuted ? 'Réactiver' : 'Couper') : (isMuted ? 'Unmute' : 'Mute') }}
          </button>
          <button
            @click="endInterview"
            class="px-6 py-2 bg-red-600 hover:bg-red-500 text-white font-medium rounded-lg transition-colors"
          >
            {{ selectedLanguage === 'fr' ? 'Terminer l\'entretien' : 'End Interview' }}
          </button>
        </div>
      </div>

      <!-- Status Bar -->
      <div v-if="interviewState !== 'setup'" class="bg-slate-800/50 rounded-xl border border-slate-700 p-4 mb-6">
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
          <div class="flex items-center gap-4 text-slate-500 text-sm">
            <span v-if="selectedResume">{{ selectedResume.name }}</span>
            <span>{{ formatDuration(interviewDuration) }}</span>
          </div>
        </div>
      </div>

      <!-- Transcription -->
      <div v-if="interviewState !== 'setup' && interviewState !== 'initializing'" class="bg-slate-800/50 rounded-2xl border border-slate-700 p-6">
        <h2 class="text-white font-medium mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          {{ selectedLanguage === 'fr' ? 'Conversation' : 'Conversation' }}
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
                {{ message.speaker === 'agent' ? interviewerInitials : (selectedLanguage === 'fr' ? 'V' : 'U') }}
              </span>
              {{ message.speaker === 'agent' ? interviewerName : (selectedLanguage === 'fr' ? 'Vous' : 'You') }}
            </p>
            <p class="text-white">{{ message.text }}</p>
          </div>
          <div v-if="transcript.length === 0" class="text-slate-500 text-center py-8">
            <svg class="w-12 h-12 mx-auto mb-3 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            {{ selectedLanguage === 'fr' ? 'En attente du début de la conversation...' : 'Waiting for the conversation to begin...' }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { Room, RoomEvent, Track, ConnectionState, RemoteTrack, RemoteParticipant, Participant } from 'livekit-client'
import { sampleResumes, sampleJobs, availableVoices, type Resume, type JobDescription, type Voice, type Language } from '~/data/samples'

const config = useRuntimeConfig()

// Interview states: setup -> initializing -> listening/thinking/speaking/userSpeaking
type InterviewState = 'setup' | 'initializing' | 'listening' | 'thinking' | 'speaking' | 'userSpeaking'

const interviewState = ref<InterviewState>('setup')
const isMuted = ref(false)
const audioLevel = ref(0)
const transcript = ref<Array<{ speaker: 'agent' | 'user', text: string }>>([])
const transcriptContainer = ref<HTMLElement | null>(null)
const interviewDuration = ref(0)
const agentState = ref<string>('listening')
const agentHasSpoken = ref(false)

// Selection state
const selectedLanguage = ref<Language>('en')
const selectedResume = ref<Resume | null>(null)
const selectedJob = ref<JobDescription | null>(null)
const selectedVoice = ref<Voice | null>(availableVoices[0]) // Default to first voice
const showCustomResume = ref(false)
const showCustomJob = ref(false)
const customResumeJson = ref('')
const customJobJson = ref('')
const customResumeError = ref('')
const customJobError = ref('')

// Computed filtered lists by language
const filteredResumes = computed(() => sampleResumes.filter(r => r.language === selectedLanguage.value))
const filteredJobs = computed(() => sampleJobs.filter(j => j.language === selectedLanguage.value))
const filteredVoices = computed(() => availableVoices.filter(v => v.language === selectedLanguage.value))

// Reset selections when language changes
watch(selectedLanguage, () => {
  selectedResume.value = null
  selectedJob.value = null
  selectedVoice.value = filteredVoices.value[0] || null
})

let room: Room | null = null
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let durationInterval: NodeJS.Timeout | null = null

// Maximum interview duration in seconds (25 minutes)
const MAX_INTERVIEW_DURATION = 25 * 60
const WARNING_THRESHOLD = 23 * 60 // Show warning at 23 minutes

// Time remaining warning
const timeRemaining = computed(() => MAX_INTERVIEW_DURATION - interviewDuration.value)
const showTimeWarning = computed(() => interviewDuration.value >= WARNING_THRESHOLD && interviewDuration.value < MAX_INTERVIEW_DURATION)

// Interviewer info based on language
const interviewerName = computed(() => selectedLanguage.value === 'fr' ? 'Marie Dubois' : 'Sarah Mitchell')
const interviewerInitials = computed(() => selectedLanguage.value === 'fr' ? 'MD' : 'SM')

const statusText = computed(() => {
  const name = interviewerName.value
  if (selectedLanguage.value === 'fr') {
    switch (interviewState.value) {
      case 'initializing': return 'Connexion à la salle d\'entretien...'
      case 'thinking': return `${name} réfléchit...`
      case 'speaking': return `${name} parle`
      case 'listening': return 'En attente de votre réponse'
      case 'userSpeaking': return 'Vous parlez'
      default: return ''
    }
  }
  switch (interviewState.value) {
    case 'initializing': return 'Connecting to interview room...'
    case 'thinking': return `${name} is thinking...`
    case 'speaking': return `${name} is speaking`
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

// Parse custom resume JSON
const parseCustomResume = () => {
  try {
    const parsed = JSON.parse(customResumeJson.value)
    if (!parsed.name || !parsed.experience) {
      throw new Error('Resume must have name and experience fields')
    }
    selectedResume.value = { id: 'custom', ...parsed }
    customResumeError.value = ''
    showCustomResume.value = false
  } catch (e: any) {
    customResumeError.value = e.message || 'Invalid JSON'
  }
}

// Parse custom job JSON
const parseCustomJob = () => {
  try {
    const parsed = JSON.parse(customJobJson.value)
    if (!parsed.title || !parsed.company) {
      throw new Error('Job must have title and company fields')
    }
    selectedJob.value = { id: 'custom', ...parsed }
    customJobError.value = ''
    showCustomJob.value = false
  } catch (e: any) {
    customJobError.value = e.message || 'Invalid JSON'
  }
}

// Update interview state based on agent state from backend
const updateInterviewState = () => {
  if (interviewState.value === 'setup') return

  switch (agentState.value) {
    case 'speaking':
      agentHasSpoken.value = true
      interviewState.value = 'speaking'
      break
    case 'thinking':
      if (agentHasSpoken.value) {
        interviewState.value = 'thinking'
      }
      break
    case 'listening':
      if (agentHasSpoken.value) {
        if (interviewState.value !== 'userSpeaking') {
          interviewState.value = 'listening'
        }
      } else {
        interviewState.value = 'initializing'
      }
      break
    default:
      if (!agentHasSpoken.value) {
        interviewState.value = 'initializing'
      }
  }
}

const startInterview = async () => {
  if (!selectedResume.value || !selectedJob.value) return

  interviewState.value = 'initializing'

  try {
    // Get token from API with resume, job, voice IDs, and language
    const { token } = await $fetch<{ token: string }>('/api/token', {
      method: 'POST',
      body: {
        resumeId: selectedResume.value.id,
        jobId: selectedJob.value.id,
        voiceId: selectedVoice.value?.id || 'aura-2-thalia-en',
        language: selectedLanguage.value
      }
    })

    // Create and connect to room
    room = new Room()

    room.on(RoomEvent.ConnectionStateChanged, (state: ConnectionState) => {
      if (state === ConnectionState.Connected) {
        // Stay in initializing until agent speaks
        durationInterval = setInterval(() => {
          interviewDuration.value++
          // Auto-end interview after max duration
          if (interviewDuration.value >= MAX_INTERVIEW_DURATION) {
            console.log('Interview timed out after 25 minutes')
            endInterview()
          }
        }, 1000)
      } else if (state === ConnectionState.Disconnected) {
        interviewState.value = 'setup'
      }
    })

    // Handle agent audio
    room.on(RoomEvent.TrackSubscribed, (track: RemoteTrack, _publication, participant: RemoteParticipant) => {
      if (track.kind === Track.Kind.Audio && participant.identity.startsWith('agent')) {
        const audioElement = track.attach()
        document.body.appendChild(audioElement)
      }
    })

    room.on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack) => {
      if (track.kind === Track.Kind.Audio) {
        const elements = track.detach()
        elements.forEach(el => el.remove())
      }
    })

    // Listen for agent state changes from backend
    room.on(RoomEvent.ParticipantAttributesChanged, (changedAttributes: Record<string, string>, participant: Participant) => {
      console.log('Attributes changed:', participant.identity, changedAttributes)
      if (participant.identity.startsWith('agent')) {
        // Check if agent ended the interview
        if (changedAttributes.interview_ended === 'true') {
          console.log('Agent ended the interview')
          // Wait 30 seconds for final audio to finish, then end
          setTimeout(() => {
            endInterview()
          }, 30000)
          return
        }

        if (changedAttributes.agent_state) {
          agentState.value = changedAttributes.agent_state
          console.log('Agent state from backend:', agentState.value)
          updateInterviewState()
        }

      }
    })

    // Check existing participants
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

    // Handle active speaker changes
    room.on(RoomEvent.ActiveSpeakersChanged, (speakers) => {
      const userIsSpeaking = speakers.some(s => !s.identity.startsWith('agent'))

      if (userIsSpeaking && agentState.value === 'listening' && agentHasSpoken.value) {
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
          nextTick(() => {
            if (transcriptContainer.value) {
              transcriptContainer.value.scrollTop = transcriptContainer.value.scrollHeight
            }
          })
        }
      }
    })

    await room.connect(config.public.livekitUrl, token)
    await room.localParticipant.setMicrophoneEnabled(true)
    setupAudioMonitoring()

  } catch (error) {
    console.error('Failed to connect:', error)
    interviewState.value = 'setup'
  }
}

const endInterview = async () => {
  if (room) {
    // Clean up all audio elements before disconnecting
    room.remoteParticipants.forEach(participant => {
      participant.audioTrackPublications.forEach(pub => {
        if (pub.track) {
          const elements = pub.track.detach()
          elements.forEach(el => el.remove())
        }
      })
    })
    await room.disconnect()
    room = null
  }
  if (durationInterval) {
    clearInterval(durationInterval)
    durationInterval = null
  }
  interviewState.value = 'setup'
  transcript.value = []
  audioLevel.value = 0
  interviewDuration.value = 0
  agentHasSpoken.value = false
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
    if (!analyser || interviewState.value === 'setup') return
    analyser.getByteFrequencyData(dataArray)
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length
    audioLevel.value = Math.min(100, average * 1.5)

    if (agentState.value === 'listening' && agentHasSpoken.value) {
      if (audioLevel.value > 15) {
        interviewState.value = 'userSpeaking'
        if (silenceTimer) {
          clearTimeout(silenceTimer)
          silenceTimer = null
        }
      } else if (audioLevel.value < 10 && interviewState.value === 'userSpeaking') {
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
      updateInterviewState()
    }

    requestAnimationFrame(updateLevel)
  }
  updateLevel()
}

onUnmounted(() => {
  if (room) {
    // Clean up all audio elements
    room.remoteParticipants.forEach(participant => {
      participant.audioTrackPublications.forEach(pub => {
        if (pub.track) {
          const elements = pub.track.detach()
          elements.forEach(el => el.remove())
        }
      })
    })
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
