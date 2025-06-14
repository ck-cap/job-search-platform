<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Upload Your Resume</h1>
    <div
      class="border p-6 rounded-lg shadow-md transition-colors duration-200"
      :class="{ 'border-blue-400 bg-blue-50': isDragging }"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      tabindex="0"
      aria-label="Resume upload dropzone"
    >
      <div class="mb-4">
        <label for="resume-file" class="block text-sm font-medium text-gray-700">Resume File (PDF, DOC, DOCX)</label>
        <input
          id="resume-file"
          type="file"
          @change="handleFileUpload"
          accept=".pdf,.doc,.docx"
          class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
          aria-describedby="resume-file-help"
        />
        <span id="resume-file-help" class="text-xs text-gray-400">You can also drag and drop your file here.</span>
      </div>
      <div v-if="fileName" class="mb-4 flex items-center gap-2">
        <p class="text-sm text-gray-600">Selected file: {{ fileName }}</p>
        <button @click="clearFile" class="ml-2 px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300" aria-label="Clear selected file">Clear</button>
      </div>
      <button
        @click="submitResume"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="!file || isUploading"
        aria-busy="isUploading"
      >
        <span v-if="isUploading">
          <svg class="inline w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
          Uploading...
        </span>
        <span v-else>Upload</span>
      </button>
      <div v-if="uploadStatus === 'success'" class="mt-4 text-green-600">Resume uploaded successfully!</div>
      <div v-if="uploadStatus === 'error'" class="mt-4 text-red-600">Failed to upload resume. Please try again.</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const file = ref<File | null>(null);
const fileName = ref<string | null>(null);
const isDragging = ref(false);
const isUploading = ref(false);
const uploadStatus = ref<'idle' | 'success' | 'error'>('idle');

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    file.value = target.files[0];
    fileName.value = file.value.name;
    uploadStatus.value = 'idle';
  } else {
    file.value = null;
    fileName.value = null;
  }
};

const clearFile = () => {
  file.value = null;
  fileName.value = null;
  uploadStatus.value = 'idle';
};

const onDragOver = () => {
  isDragging.value = true;
};
const onDragLeave = () => {
  isDragging.value = false;
};
const onDrop = (event: DragEvent) => {
  isDragging.value = false;
  if (event.dataTransfer && event.dataTransfer.files.length > 0) {
    const droppedFile = event.dataTransfer.files[0];
    if (["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(droppedFile.type) || /\.pdf$|\.docx?$/.test(droppedFile.name)) {
      file.value = droppedFile;
      fileName.value = droppedFile.name;
      uploadStatus.value = 'idle';
    } else {
      uploadStatus.value = 'error';
      file.value = null;
      fileName.value = null;
    }
  }
};

const submitResume = async () => {
  if (!file.value) {
    alert('Please select a file to upload.');
    return;
  }
  isUploading.value = true;
  uploadStatus.value = 'idle';
  try {
    // Simulate upload delay
    await new Promise((resolve) => setTimeout(resolve, 2000));
    // Placeholder for actual upload logic
    // e.g., await uploadResume(file.value)
    uploadStatus.value = 'success';
    clearFile();
  } catch (e) {
    uploadStatus.value = 'error';
  } finally {
    isUploading.value = false;
  }
};
</script>

<style scoped>
[aria-busy="true"] {
  pointer-events: none;
}
</style> 