<script setup>
import { ref } from 'vue';
import PdfViewer from 'pdf-viewer-vue';

const pdfSource = ref(null);

// Function to handle text selection
const handleTextSelection = (selectedText) => {
  console.log('Selected text:', selectedText);
};

// Simulate loading a PDF buffer (replace with actual buffer loading logic)
fetch('./input.pdf')
  .then(response => response.blob())
  .then(blob => {
    pdfSource.value = URL.createObjectURL(blob);
  });
</script>

<template>
  <div>
    <PdfViewer
      v-if="pdfSource"
      :source="pdfSource"
      @text-selected="handleTextSelection"
      textLayer
    />
  </div>
</template>

<style scoped>
  .pdf-viewer {
    height: 100vh;
    max-width: 50vw;
    position: relative;
  }
  .pdf-viewer .textLayer {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
  }
  .pdf-viewer .textLayer div {
    pointer-events: all;
  }
</style>