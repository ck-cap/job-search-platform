<template>
  <div class="structured-resume-display space-y-6">
    <!-- Contact Information -->
    <div v-if="resumeData.contact_info" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-blue-100">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <h3 class="section-title">Contact Information</h3>
        <button 
          @click="toggleEdit('contact_info')" 
          class="edit-button"
          v-if="!isEditing.contact_info"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('contact_info')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('contact_info')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.contact_info" class="contact-grid">
          <div class="contact-item">
            <span class="contact-label">Name:</span>
            <span class="contact-value">{{ resumeData.contact_info.name || 'Not provided' }}</span>
          </div>
          <div class="contact-item">
            <span class="contact-label">Email:</span>
            <span class="contact-value">{{ resumeData.contact_info.email || 'Not provided' }}</span>
          </div>
          <div class="contact-item">
            <span class="contact-label">Phone:</span>
            <span class="contact-value">{{ resumeData.contact_info.phone || 'Not provided' }}</span>
          </div>
          <div class="contact-item">
            <span class="contact-label">Location:</span>
            <span class="contact-value">{{ resumeData.contact_info.location || 'Not provided' }}</span>
          </div>
        </div>
        <textarea
          v-else
          v-model="editData.contact_info"
          class="edit-textarea"
          rows="4"
          placeholder="Contact information..."
        ></textarea>
      </div>
    </div>

    <!-- Summary -->
    <div v-if="resumeData.summary" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-green-100">
          <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h3 class="section-title">Professional Summary</h3>
        <div class="view-toggle">
          <button 
            @click="toggleView('summary')" 
            class="toggle-button"
            :class="{ 'active': expandedSections.summary }"
          >
            {{ expandedSections.summary ? 'Summary' : 'Full Text' }}
          </button>
        </div>
        <button 
          @click="toggleEdit('summary')" 
          class="edit-button"
          v-if="!isEditing.summary"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('summary')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('summary')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
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
          class="edit-textarea"
          rows="6"
          placeholder="Professional summary..."
        ></textarea>
      </div>
    </div>

    <!-- Experience -->
    <div v-if="resumeData.experience" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-purple-100">
          <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6.294A9.97 9.97 0 0112 16a9.97 9.97 0 01-8-3.706V8a2 2 0 012-2h12a2 2 0 012 2z"/>
          </svg>
        </div>
        <h3 class="section-title">Work Experience</h3>
        <div class="view-toggle">
          <button 
            @click="toggleView('experience')" 
            class="toggle-button"
            :class="{ 'active': expandedSections.experience }"
          >
            {{ expandedSections.experience ? 'Summary' : 'Full Text' }}
          </button>
        </div>
        <button 
          @click="toggleEdit('experience')" 
          class="edit-button"
          v-if="!isEditing.experience"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('experience')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('experience')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
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
          class="edit-textarea"
          rows="8"
          placeholder="Work experience..."
        ></textarea>
      </div>
    </div>

    <!-- Education -->
    <div v-if="resumeData.education" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-indigo-100">
          <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <h3 class="section-title">Education</h3>
        <div class="view-toggle">
          <button 
            @click="toggleView('education')" 
            class="toggle-button"
            :class="{ 'active': expandedSections.education }"
          >
            {{ expandedSections.education ? 'Summary' : 'Full Text' }}
          </button>
        </div>
        <button 
          @click="toggleEdit('education')" 
          class="edit-button"
          v-if="!isEditing.education"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('education')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('education')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
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
          class="edit-textarea"
          rows="6"
          placeholder="Education..."
        ></textarea>
      </div>
    </div>

    <!-- Skills -->
    <div v-if="resumeData.skills" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-yellow-100">
          <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
          </svg>
        </div>
        <h3 class="section-title">Skills & Technologies</h3>
        <div class="view-toggle">
          <button 
            @click="toggleView('skills')" 
            class="toggle-button"
            :class="{ 'active': expandedSections.skills }"
          >
            {{ expandedSections.skills ? 'Summary' : 'Full Text' }}
          </button>
        </div>
        <button 
          @click="toggleEdit('skills')" 
          class="edit-button"
          v-if="!isEditing.skills"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('skills')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('skills')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
      <div class="section-content">
        <div v-if="!isEditing.skills">
          <div v-if="expandedSections.skills" class="skills-summary">
            <p class="section-text">{{ resumeData.skills.summary }}</p>
          </div>
          <div v-else class="skills-detailed">
            <div class="skill-tags">
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
          class="edit-textarea"
          rows="6"
          placeholder="Skills and technologies..."
        ></textarea>
      </div>
    </div>

    <!-- Projects -->
    <div v-if="resumeData.projects" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-orange-100">
          <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14-7H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V6a2 2 0 00-2-2zM12 2v20"/>
          </svg>
        </div>
        <h3 class="section-title">Projects</h3>
        <div class="view-toggle">
          <button 
            @click="toggleView('projects')" 
            class="toggle-button"
            :class="{ 'active': expandedSections.projects }"
          >
            {{ expandedSections.projects ? 'Summary' : 'Full Text' }}
          </button>
        </div>
        <button 
          @click="toggleEdit('projects')" 
          class="edit-button"
          v-if="!isEditing.projects"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('projects')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('projects')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
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
          class="edit-textarea"
          rows="8"
          placeholder="Projects..."
        ></textarea>
      </div>
    </div>

    <!-- Certificates -->
    <div v-if="resumeData.certificates" class="section-card">
      <div class="section-header">
        <div class="section-icon bg-teal-100">
          <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
          </svg>
        </div>
        <h3 class="section-title">Certificates</h3>
        <div class="view-toggle">
          <button 
            @click="toggleView('certificates')" 
            class="toggle-button"
            :class="{ 'active': expandedSections.certificates }"
          >
            {{ expandedSections.certificates ? 'Summary' : 'Full Text' }}
          </button>
        </div>
        <button 
          @click="toggleEdit('certificates')" 
          class="edit-button"
          v-if="!isEditing.certificates"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <div v-else class="edit-actions">
          <button @click="saveEdit('certificates')" class="save-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </button>
          <button @click="cancelEdit('certificates')" class="cancel-button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
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
          class="edit-textarea"
          rows="4"
          placeholder="Certificates..."
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

interface Props {
  resumeData: any;
  modelValue?: Record<string, any>;
}

interface Emits {
  (e: 'update:modelValue', value: Record<string, any>): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const isEditing = ref<Record<string, boolean>>({});
const editData = reactive<Record<string, any>>({});
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

function toggleEdit(section: string) {
  isEditing.value[section] = !isEditing.value[section];
  
  if (isEditing.value[section]) {
    // Initialize edit data based on section
    if (section === 'contact_info') {
      const contact = props.resumeData.contact_info;
      editData[section] = `${contact.name || ''}\n${contact.email || ''}\n${contact.phone || ''}\n${contact.location || ''}`.trim();
    } else if (props.resumeData[section]) {
      // For sections with summary/full_text, use the full_text for editing
      editData[section] = props.resumeData[section].full_text || props.resumeData[section].summary || '';
    }
  }
}

function saveEdit(section: string) {
  isEditing.value[section] = false;
  // Emit the updated data
  emit('update:modelValue', { ...props.modelValue, [section]: editData[section] });
}

function cancelEdit(section: string) {
  isEditing.value[section] = false;
  delete editData[section];
}
</script>

<style scoped>
.structured-resume-display {
  @apply space-y-6;
}

.section-card {
  @apply bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow;
}

.section-header {
  @apply flex items-center justify-between p-4 bg-gray-50 border-b border-gray-200;
}

.section-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center mr-3;
}

.section-title {
  @apply text-lg font-semibold text-gray-900 flex-1;
}

.view-toggle {
  @apply mr-3;
}

.toggle-button {
  @apply px-3 py-1 text-sm rounded-full border border-gray-300 text-gray-600 hover:bg-gray-100 transition-colors;
}

.toggle-button.active {
  @apply bg-primary-100 border-primary-300 text-primary-700;
}

.edit-button {
  @apply p-2 text-gray-400 hover:text-primary-600 transition-colors rounded-lg hover:bg-gray-100;
}

.edit-actions {
  @apply flex items-center space-x-2;
}

.save-button {
  @apply p-2 text-green-600 hover:text-green-700 transition-colors rounded-lg hover:bg-green-50;
}

.cancel-button {
  @apply p-2 text-red-600 hover:text-red-700 transition-colors rounded-lg hover:bg-red-50;
}

.section-content {
  @apply p-4;
}

.section-text {
  @apply text-gray-700 leading-relaxed;
}

.edit-textarea {
  @apply w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm;
}

/* Contact Information */
.contact-grid {
  @apply grid grid-cols-1 md:grid-cols-2 gap-4;
}

.contact-item {
  @apply flex flex-col;
}

.contact-label {
  @apply text-sm font-medium text-gray-600 mb-1;
}

.contact-value {
  @apply text-gray-900;
}

/* Skills */
.skills-summary {
  @apply mb-4;
}

.skills-detailed {
  @apply space-y-3;
}

.skill-tags {
  @apply flex flex-wrap gap-2;
}

.skill-tag {
  @apply px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full border border-yellow-200;
}
</style> 