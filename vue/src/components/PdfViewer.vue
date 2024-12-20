<script setup>
    import { ref, onMounted, onUnmounted, watch } from 'vue'
    import * as pdfjsLib from 'pdfjs-dist'
    import 'pdfjs-dist/web/pdf_viewer.css'

    pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.js`

    const props = defineProps({
        source: {
            type: File,
            required: true
        }
    })

    watch(() => props.source, (newSource) =>
    {
        if (newSource) {
            loadPdf()
        }
    })

    const pdfViewerContainer = ref(null)

    const textSelection = ref(null)
    const emit = defineEmits(['text-selected', 'loading-complete'])
    const setSelectedText = (value, x, y) =>{
        emit('text-selected', value, x, y)
    }
    const notifyLoadingComplete = () =>{
        emit('loading-complete')
    }

    const onTextLayerMouseUp = (event) => {  
        const selectedText = window.getSelection().toString()
        if (selectedText && selectedText.trim().length > 0 && selectedText !== textSelection.value){
            const { clientX: x, clientY: y } = event
            setSelectedText(selectedText, x, y)
            textSelection.value = selectedText
        }
        else
            textSelection.value = null
    }

    const renderPage = (page, pdf) => {
        const containerWidth = pdfViewerContainer.value.clientWidth
        //console.log("containerWidth", containerWidth)
        const viewport = page.getViewport({ scale: 1 })
        const scale = containerWidth / viewport.width
        const scaledViewport = page.getViewport({ scale })

        const pageContainer = document.createElement('div')
        pageContainer.style.position = 'relative'
        pageContainer.style.marginBottom = '1rem'

        const canvas = document.createElement('canvas')
        const context = canvas.getContext('2d')
        canvas.height = scaledViewport.height
        canvas.width = containerWidth

        const renderContext = {
            canvasContext: context,
            viewport: scaledViewport
        }

        page.render(renderContext).promise.then(() => {
            const textLayerDiv = document.createElement('div')
            textLayerDiv.className = 'textLayer'
            textLayerDiv.style.height = `${scaledViewport.height}px`
            textLayerDiv.style.width = `${containerWidth}px`
            textLayerDiv.style.position = 'absolute'
            textLayerDiv.style.top = '0'
            textLayerDiv.style.left = '0'

            page.getTextContent().then(textContent => {
                pdfjsLib.renderTextLayer({
                    textContent: textContent,
                    container: textLayerDiv,
                    viewport: scaledViewport,
                    textDivs: []
                })

                textLayerDiv.addEventListener('mouseup', onTextLayerMouseUp)
            })

            pageContainer.appendChild(canvas)
            pageContainer.appendChild(textLayerDiv)
            pdfViewerContainer.value.appendChild(pageContainer)
        })
    }

    const debounce = (func, wait) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    };

    const loadPdf = async () => {
        if (!props.source) 
            return

        const reader = new FileReader()
        reader.onload = function(event) {
            const arrayBuffer = event.target.result
            const loadingTask = pdfjsLib.getDocument({ data: new Uint8Array(arrayBuffer) })

            loadingTask.promise.then(pdf =>
            {
                pdfViewerContainer.value.innerHTML = '' // Clear previous content
                for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                    pdf.getPage(pageNum).then(page => {
                        renderPage(page, pdf)
                    })
                }
            })
            .then(() => {
                notifyLoadingComplete()
            })
            .catch(error => {
                console.error('Error loading PDF:', error)
            })
        }
        reader.readAsArrayBuffer(props.source)
    }

    const debouncedLoadPdf = debounce(loadPdf, 300);

    onMounted(() => {
        loadPdf()
        window.addEventListener('resize', debouncedLoadPdf)
    })

    onUnmounted(() => {
        window.removeEventListener('resize', debouncedLoadPdf)
    })
</script>

<template>
    <div ref="pdfViewerContainer" class="pdf-viewer"></div>
</template>

<style scoped>
    .pdfViewerParent
    {
        position: relative;
    }
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
</style>