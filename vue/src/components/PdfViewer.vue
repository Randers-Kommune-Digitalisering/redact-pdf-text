<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as pdfjsLib from 'pdfjs-dist'
import 'pdfjs-dist/web/pdf_viewer.css'

pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.js`

const props = defineProps({
  source: {
    type: String,
    required: true
  }
})

watch(() => props.source, (newSource) => {
    if (newSource) {
        loadPdf()
    }
})

// const pdfSource = ref(null)
const pdfViewerContainer = ref(null)
const popup = ref(null)
const textSelection = ref(null)

// const handleTextSelection = (selectedText) => {
//     console.log('Selected text:', selectedText)
// }

const showPopup = (x, y, text) => {
    popup.value.style.left = `${x - 50}px`
    popup.value.style.top = `${y - 50}px`
    popup.value.textContent = text
    popup.value.style.display = 'block'
}

const hidePopup = () => {
    popup.value.style.display = 'none'
}

const onTextLayerMouseUp = (event) => {  
    const selectedText = window.getSelection().toString()
    if (selectedText && selectedText.trim().length > 0 && selectedText !== textSelection.value){
        const { clientX: x, clientY: y } = event
        showPopup(x, y, selectedText)
        //handleTextSelection(selectedText)
        textSelection.value = selectedText
    }
    else
    {
        hidePopup()
        textSelection.value = null
    }
}

const renderPage = (page) => {
    const containerWidth = pdfViewerContainer.value.clientWidth
    console.log("containerWidth", containerWidth)
    const viewport = page.getViewport({ scale: 1 })
    const scale = containerWidth / viewport.width
    const scaledViewport = page.getViewport({ scale })

    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    canvas.height = scaledViewport.height
    canvas.width = containerWidth

    const renderContext = {
        canvasContext: context,
        viewport: scaledViewport
    }
    page.render(renderContext)

    const textLayerDiv = document.createElement('div')
    textLayerDiv.className = 'textLayer'
    pdfViewerContainer.value.appendChild(textLayerDiv)

    page.getTextContent().then(textContent => {
        pdfjsLib.renderTextLayer({
            textContent: textContent,
            container: textLayerDiv,
            viewport: scaledViewport,
            textDivs: []
        })

        textLayerDiv.addEventListener('mouseup', onTextLayerMouseUp)
    })

    pdfViewerContainer.value.appendChild(canvas)
}

const loadPdf = () => {
    if(props.source === null) return
    const loadingTask = pdfjsLib.getDocument(props.source)
    loadingTask.promise.then(pdf => {
        pdf.getPage(1).then(page => {
            pdfViewerContainer.value.innerHTML = '' // Clear previous content
            renderPage(page)
        })
    })
}

onMounted(() => {
    loadPdf()
    window.addEventListener('resize', loadPdf)
})

onUnmounted(() => {
    window.removeEventListener('resize', loadPdf)
})
</script>

<template>
    <div ref="pdfViewerContainer" class="pdf-viewer"></div>
    <div ref="popup" class="popup"></div>
</template>

<style scoped>
    .pdf-viewer {
        width: 100%;
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
    .popup {
        position: absolute;
        display: none;
        background: #fff;
        border: 1px solid #ccc;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        border-radius: 0.5rem;
        padding: 0.8rem;
    }
</style>