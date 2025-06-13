<template>
  <div class="structured-resume-display space-y-6">
    <!-- Contact Information -->
    <div v-if="resumeData.contact_info" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-blue-100 text-blue-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
            <h3 class="section-title">Contact Information</h3>
          </div>
          
          <!-- Right side: Edit Button -->
          <div class="flex items-center space-x-2">
            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.contact_info"
              @click="toggleEdit('contact_info')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('contact_info')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('contact_info')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.contact_info" class="contact-grid">
          <!-- Name -->
          <div class="contact-item">
            <div class="contact-field">
              <div class="contact-icon">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">Name</span>
                <span class="contact-value">{{ resumeData.contact_info.name || 'Not provided' }}</span>
              </div>
            </div>
          </div>
          
          <!-- Email -->
          <div class="contact-item">
            <div class="contact-field">
              <div class="contact-icon">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">Email</span>
                <a 
                  v-if="resumeData.contact_info.email" 
                  :href="`mailto:${resumeData.contact_info.email}`"
                  class="contact-value contact-link"
                >
                  {{ resumeData.contact_info.email }}
                </a>
                <span v-else class="contact-value">Not provided</span>
              </div>
            </div>
          </div>
          
          <!-- Phone -->
          <div class="contact-item">
            <div class="contact-field">
              <div class="contact-icon">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">Phone</span>
                <a 
                  v-if="resumeData.contact_info.phone" 
                  :href="`tel:${resumeData.contact_info.phone}`"
                  class="contact-value contact-link"
                >
                  {{ resumeData.contact_info.phone }}
                </a>
                <span v-else class="contact-value">Not provided</span>
              </div>
            </div>
          </div>
          
          <!-- Location -->
          <div class="contact-item">
            <div class="contact-field">
              <div class="contact-icon">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">Location</span>
                <span class="contact-value">{{ resumeData.contact_info.location || 'Not provided' }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="contact-edit-grid space-y-4">
          <div class="form-field">
            <label class="form-label">Name</label>
            <input 
              v-model="contactEditData.name"
              type="text" 
              class="form-input"
              placeholder="Enter your full name"
            />
          </div>
          <div class="form-field">
            <label class="form-label">Email</label>
            <input 
              v-model="contactEditData.email"
              type="email" 
              class="form-input"
              placeholder="Enter your email address"
            />
          </div>
          <div class="form-field">
            <label class="form-label">Phone</label>
            <input 
              v-model="contactEditData.phone"
              type="tel" 
              class="form-input"
              placeholder="Enter your phone number"
            />
          </div>
          <div class="form-field">
            <label class="form-label">Location</label>
            <input 
              v-model="contactEditData.location"
              type="text" 
              class="form-input"
              placeholder="Enter your location"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Summary -->
    <div v-if="resumeData.summary" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-green-100 text-green-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <h3 class="section-title">Professional Summary</h3>
          </div>
          
          <!-- Right side: Toggle and Edit Buttons -->
          <div class="flex items-center space-x-2">
            <!-- View Toggle Button -->
            <Button 
              v-if="!isEditing.summary"
              @click="toggleView('summary')" 
              variant="outline"
              size="sm"
              :class="expandedSections.summary ? 'toggle-active' : 'toggle-inactive'"
            >
              <svg class="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="expandedSections.summary" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              {{ expandedSections.summary ? 'Show Full Text' : 'Show Summary' }}
            </Button>
            
            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.summary"
              @click="toggleEdit('summary')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('summary')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('summary')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.summary">
          <p class="section-text">
            {{ expandedSections.summary ? resumeData.summary.summary : resumeData.summary.full_text }}
          </p>
        </div>
        <textarea
          v-else
          v-model="editData.summary"
          class="form-textarea"
          rows="6"
          :placeholder="expandedSections.summary ? 'Professional summary...' : 'Full professional summary details...'"
        ></textarea>
      </div>
    </div>

    <!-- Experience -->
    <div v-if="resumeData.experience" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-purple-100 text-purple-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6.294A9.97 9.97 0 0112 16a9.97 9.97 0 01-8-3.706V8a2 2 0 012-2h12a2 2 0 012 2z"/>
              </svg>
            </div>
            <h3 class="section-title">Work Experience</h3>
          </div>
          
          <!-- Right side: Toggle and Edit Buttons -->
          <div class="flex items-center space-x-2">
            <!-- View Toggle Button -->
            <Button 
              v-if="!isEditing.experience"
              @click="toggleView('experience')" 
              variant="outline"
              size="sm"
              :class="expandedSections.experience ? 'toggle-active' : 'toggle-inactive'"
            >
              <svg class="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="expandedSections.experience" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              {{ expandedSections.experience ? 'Show Full Text' : 'Show Summary' }}
            </Button>
            
            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.experience"
              @click="toggleEdit('experience')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('experience')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('experience')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.experience">
          <p class="section-text whitespace-pre-line">
            {{ expandedSections.experience ? resumeData.experience.summary : resumeData.experience.full_text }}
          </p>
        </div>
        <textarea
          v-else
          v-model="editData.experience"
          class="form-textarea"
          rows="8"
          :placeholder="expandedSections.experience ? 'Work experience summary...' : 'Full work experience details...'"
        ></textarea>
      </div>
    </div>

    <!-- Education -->
    <div v-if="resumeData.education" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-indigo-100 text-indigo-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
            </div>
            <h3 class="section-title">Education</h3>
          </div>
          
          <!-- Right side: Toggle and Edit Buttons -->
          <div class="flex items-center space-x-2">
                        <!-- View Toggle Button -->
            <Button 
              v-if="!isEditing.education"
              @click="toggleView('education')" 
              variant="outline"
              size="sm"
              :class="expandedSections.education ? 'toggle-active' : 'toggle-inactive'"
            >
              <svg class="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="expandedSections.education" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              {{ expandedSections.education ? 'Show Full Text' : 'Show Summary' }}
            </Button>

            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.education"
              @click="toggleEdit('education')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('education')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('education')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.education">
          <p class="section-text whitespace-pre-line">
            {{ expandedSections.education ? resumeData.education.summary : resumeData.education.full_text }}
          </p>
        </div>
        <textarea
          v-else
          v-model="editData.education"
          class="form-textarea"
          rows="6"
          :placeholder="expandedSections.education ? 'Education summary...' : 'Full education details...'"
        ></textarea>
      </div>
    </div>

    <!-- Skills -->
    <div v-if="resumeData.skills" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-yellow-100 text-yellow-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </div>
            <h3 class="section-title">Skills & Technologies</h3>
          </div>
          
          <!-- Right side: Toggle and Edit Buttons -->
          <div class="flex items-center space-x-2">
            <!-- View Toggle Button -->
            <Button 
              v-if="!isEditing.skills"
              @click="toggleView('skills')" 
              variant="outline"
              size="sm"
              :class="expandedSections.skills ? 'toggle-active' : 'toggle-inactive'"
            >
              <svg class="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="expandedSections.skills" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              {{ expandedSections.skills ? 'Show Full Text' : 'Show Summary' }}
            </Button>
            
            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.skills"
              @click="toggleEdit('skills')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('skills')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('skills')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.skills">
          <div v-if="expandedSections.skills" class="skills-summary">
            <!-- Summary view with skill tags -->
            <div class="skill-tags">
              <span 
                v-for="skill in parseSkillsFromText(resumeData.skills.summary)" 
                :key="skill" 
                class="skill-tag"
              >
                {{ skill }}
              </span>
            </div>
          </div>
          <div v-else class="skills-detailed">
            <!-- Categorized Skills Display -->
            <div v-if="getCategorizedSkills()" class="skills-categorized">
              <div 
                v-for="(skills, category) in getCategorizedSkills()" 
                :key="category"
                class="skill-category"
              >
                <span class="skill-category-label">{{ category }}</span>
                <span class="skill-category-separator">:</span>
                <div class="skill-tags-inline">
                  <span 
                    v-for="(skill, index) in skills" 
                    :key="skill" 
                    class="skill-tag"
                  >
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
            <!-- Fallback to simple tags if no categorization -->
            <div v-else class="skill-tags">
              <span 
                v-for="skill in parseSkillsFromText(resumeData.skills.full_text)" 
                :key="skill" 
                class="skill-tag"
              >
                {{ skill }}
              </span>
            </div>
          </div>
        </div>
        <textarea
          v-else
          v-model="editData.skills"
          class="form-textarea"
          rows="6"
          :placeholder="expandedSections.skills ? 'Skills summary (comma-separated)...' : 'Full skills and technologies (use categories if desired)...'"
        ></textarea>
      </div>
    </div>

    <!-- Projects -->
    <div v-if="resumeData.projects" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-orange-100 text-orange-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14-7H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V6a2 2 0 00-2-2zM12 2v20"/>
              </svg>
            </div>
            <h3 class="section-title">Projects</h3>
          </div>
          
          <!-- Right side: Toggle and Edit Buttons -->
          <div class="flex items-center space-x-2">
            <!-- View Toggle Button -->
            <Button 
              v-if="!isEditing.projects"
              @click="toggleView('projects')" 
              variant="outline"
              size="sm"
              :class="expandedSections.projects ? 'toggle-active' : 'toggle-inactive'"
            >
              <svg class="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="expandedSections.projects" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              {{ expandedSections.projects ? 'Show Full Text' : 'Show Summary' }}
            </Button>
            
            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.projects"
              @click="toggleEdit('projects')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('projects')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('projects')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.projects">
          <p class="section-text whitespace-pre-line">
            {{ expandedSections.projects ? resumeData.projects.summary : resumeData.projects.full_text }}
          </p>
        </div>
        <textarea
          v-else
          v-model="editData.projects"
          class="form-textarea"
          rows="8"
          :placeholder="expandedSections.projects ? 'Projects summary...' : 'Full project details...'"
        ></textarea>
      </div>
    </div>

    <!-- Certificates -->
    <div v-if="resumeData.certificates" class="section-card">
      <div class="section-header">
        <div class="flex items-center justify-between w-full">
          <!-- Left side: Icon and Title -->
          <div class="flex items-center space-x-3">
            <div class="section-icon w-10 h-10 rounded-lg flex items-center justify-center bg-teal-100 text-teal-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
              </svg>
            </div>
            <h3 class="section-title">Certificates</h3>
          </div>
          
          <!-- Right side: Toggle and Edit Buttons -->
          <div class="flex items-center space-x-2">
            <!-- View Toggle Button -->
            <Button 
              v-if="!isEditing.certificates"
              @click="toggleView('certificates')" 
              variant="outline"
              size="sm"
              :class="expandedSections.certificates ? 'toggle-active' : 'toggle-inactive'"
            >
              <svg class="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="expandedSections.certificates" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              {{ expandedSections.certificates ? 'Show Full Text' : 'Show Summary' }}
            </Button>
            
            <!-- Edit Button -->
            <Button 
              v-if="!isEditing.certificates"
              @click="toggleEdit('certificates')" 
              variant="outline"
              size="icon"
              class="h-9 w-9"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </Button>
            
            <!-- Save/Cancel Buttons -->
            <div v-else class="flex items-center space-x-2">
              <Button 
                @click="saveEdit('certificates')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-green-600 border-green-300 hover:bg-green-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </Button>
              <Button 
                @click="cancelEdit('certificates')" 
                variant="outline" 
                size="icon"
                class="h-9 w-9 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.certificates">
          <p class="section-text whitespace-pre-line">
            {{ expandedSections.certificates ? resumeData.certificates.summary : resumeData.certificates.full_text }}
          </p>
        </div>
        <textarea
          v-else
          v-model="editData.certificates"
          class="form-textarea"
          rows="4"
          :placeholder="expandedSections.certificates ? 'Certificates summary...' : 'Full certificate details...'"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { Button } from '@/components/ui/button';

interface Props {
  resumeData: any;
  modelValue?: Record<string, any>;
}

interface Emits {
  (e: 'update:modelValue', value: Record<string, any>): void;
  (e: 'section-updated', section: string, data: any): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const isEditing = ref<Record<string, boolean>>({});
const editData = reactive<Record<string, any>>({});
const contactEditData = reactive({
  name: '',
  email: '',
  phone: '',
  location: ''
});
const expandedSections = reactive<Record<string, boolean>>({
  summary: true,
  experience: true,
  education: true,
  skills: true,
  projects: true,
  certificates: true,
});

function toggleView(section: string) {
  expandedSections[section] = !expandedSections[section];
}

function parseSkillsFromText(skillsText: string): string[] {
  if (!skillsText) return [];
  return skillsText
    .split(/[,\n•\-\*\|]/)
    .map(skill => skill.trim())
    .filter(skill => skill && skill.length > 1)
    .slice(0, 20); // Limit to top 20 skills for display
}

// Function to get categorized skills from the text
function getCategorizedSkills() {
  if (!props.resumeData.skills?.full_text) return null;
  
  // Try to detect if the text has categorized format
  const text = props.resumeData.skills.full_text;
  
  // Look for patterns like "Category: skill1, skill2" or "Category - skill1, skill2"
  const categoryPattern = /([^:]+)[:]\s*([^;]+)/g;
  const categories: Record<string, string[]> = {};
  let match;
  
  while ((match = categoryPattern.exec(text)) !== null) {
    const categoryName = match[1].trim();
    const skillsText = match[2].trim();
    const skills = skillsText.split(',').map((s: string) => s.trim()).filter((s: string) => s.length > 0);
    categories[categoryName] = skills;
  }
  
  // If we found categories, return them; otherwise return null for fallback
  return Object.keys(categories).length > 0 ? categories : null;
}



function toggleEdit(section: string) {
  isEditing.value[section] = !isEditing.value[section];
  
  if (isEditing.value[section]) {
    // Initialize edit data based on section
    if (section === 'contact_info') {
      const contact = props.resumeData.contact_info || {};
      contactEditData.name = contact.name || '';
      contactEditData.email = contact.email || '';
      contactEditData.phone = contact.phone || '';
      contactEditData.location = contact.location || '';
    } else if (props.resumeData[section]) {
      // For sections with summary/full_text, choose based on current view
      if (expandedSections[section]) {
        // Summary view - edit summary
        editData[section] = props.resumeData[section].summary || '';
      } else {
        // Full-text view - edit full_text
        editData[section] = props.resumeData[section].full_text || '';
      }
    }
  }
}

function saveEdit(section: string) {
  isEditing.value[section] = false;
  
  if (section === 'contact_info') {
    const contactData = {
      name: contactEditData.name,
      email: contactEditData.email,
      phone: contactEditData.phone,
      location: contactEditData.location
    };
    
    // Emit both events for compatibility
    emit('section-updated', section, contactData);
    emit('update:modelValue', { 
      ...props.modelValue, 
      [section]: contactData
    });
  } else {
    // For other sections, create the updated data structure
    const updatedData = { ...props.modelValue };
    let sectionData;
    
    if (props.resumeData[section] && typeof props.resumeData[section] === 'object') {
      // For sections with summary/full_text structure, save based on current view
      if (expandedSections[section]) {
        // Summary view - save to summary
        sectionData = {
          ...props.resumeData[section],
          summary: editData[section]
        };
      } else {
        // Full-text view - save to full_text
        sectionData = {
          ...props.resumeData[section],
          full_text: editData[section]
        };
      }
      updatedData[section] = sectionData;
    } else {
      // For simple text sections
      sectionData = editData[section];
      updatedData[section] = sectionData;
    }
    
    // Emit both events for compatibility
    emit('section-updated', section, sectionData);
    emit('update:modelValue', updatedData);
  }
}

function cancelEdit(section: string) {
  isEditing.value[section] = false;
  if (section === 'contact_info') {
    // Reset contact edit data
    const contact = props.resumeData.contact_info || {};
    contactEditData.name = contact.name || '';
    contactEditData.email = contact.email || '';
    contactEditData.phone = contact.phone || '';
    contactEditData.location = contact.location || '';
  } else if (props.resumeData[section]) {
    // Reset to original data based on current view
    if (expandedSections[section]) {
      // Summary view - reset to summary
      editData[section] = props.resumeData[section].summary || '';
    } else {
      // Full-text view - reset to full_text
      editData[section] = props.resumeData[section].full_text || '';
    }
  } else {
    delete editData[section];
  }
}
</script>

<style scoped>
/* Main Container */
.structured-resume-display {
  max-width: 4xl;
  margin: 0 auto;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: #f9fafb;
  min-height: 100vh;
  padding: 1.5rem;
}

/* Section Cards */
.section-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* Section Headers */
.section-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  letter-spacing: -0.025em;
}

/* Section Content */
.section-content {
  color: #374151;
  line-height: 1.6;
}

.section-text {
  color: #4b5563;
  line-height: 1.6;
}

/* Contact Information */
.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.contact-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
}

.contact-field {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.contact-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  min-width: 0;
  flex: 1;
}

.contact-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.contact-value {
  color: #111827;
  font-weight: 500;
  font-size: 0.95rem;
  line-height: 1.4;
  word-break: break-word;
}

.contact-link {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.2s ease-in-out;
}

  .contact-link:hover {
    color: #1d4ed8;
    text-decoration: underline;
  }
  
  /* Toggle Buttons */
  .toggle-active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
    font-weight: 500;
  }
  
  .toggle-active:hover {
    background: #2563eb;
    border-color: #2563eb;
  }
  
  .toggle-inactive {
    background: white;
    color: #6b7280;
    border-color: #d1d5db;
  }
  
  .toggle-inactive:hover {
    background: #f9fafb;
    color: #374151;
    border-color: #9ca3af;
  }
  
  /* Form Elements */
.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s ease-in-out;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  resize: vertical;
  font-family: inherit;
  font-size: 0.875rem;
  transition: all 0.2s ease-in-out;
}

.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Skills */
.skills-categorized {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}

.skill-category {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.skill-category-label {
  background: #f3f4f6;
  color: #374151;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: 1px solid #e5e7eb;
  white-space: nowrap;
}

.skill-category-separator {
  font-weight: 500;
  color: #6b7280;
  margin: 0 0.25rem;
}

.skill-tags-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.skill-tag {
  background: #f3f4f6;
  color: #374151;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid #e5e7eb;
}

.skill-tag:hover {
  background: #e5e7eb;
  color: #111827;
}

/* Responsive Design */
@media (max-width: 768px) {
  .section-card {
    padding: 1rem;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header .flex {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}
</style> 