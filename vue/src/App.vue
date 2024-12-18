<script setup>
import { ref, onMounted } from 'vue';
import * as pdfjsLib from 'pdfjs-dist';
import 'pdfjs-dist/web/pdf_viewer.css';

pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.js`;

const pdfSource = ref(null);
const pdfViewerContainer = ref(null);

const handleTextSelection = (selectedText) => {
  console.log('Selected text:', selectedText);
};

onMounted(() => {
  const loadingTask = pdfjsLib.getDocument('./input.pdf');
  loadingTask.promise.then(pdf => {
    pdf.getPage(1).then(page => {
      const scale = 1.5;
      const viewport = page.getViewport({ scale });

      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      const renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      page.render(renderContext);

      const textLayerDiv = document.createElement('div');
      textLayerDiv.className = 'textLayer';
      pdfViewerContainer.value.appendChild(textLayerDiv);

      page.getTextContent().then(textContent => {
        pdfjsLib.renderTextLayer({
          textContent: textContent,
          container: textLayerDiv,
          viewport: viewport,
          textDivs: []
        });
      });

      pdfViewerContainer.value.appendChild(canvas);
    });
  });
});
</script>

<template>
  <div ref="pdfViewerContainer" class="pdf-viewer"></div>
</template>

<style scoped>
  .pdf-viewer {
    height: 100vh;
    position: relative;
  }
  .textLayer {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
  }
  .textLayer div {
    pointer-events: all;
  }
</style>