<script setup>
    import FileDrop from './components/FileDrop.vue';
    import PdfViewer from './components/PdfViewer.vue'
    import OptionList from './components/OptionList.vue'
    import { onMounted, ref } from 'vue'

    const pdfContainer = ref(null)
    const pdfViewer = ref(null)
    const popup = ref(null)

    const originalFile = ref(null)
    const currentFilename = ref(null)
    const currentFile = ref(null)
    const currentOptions = ref([])

    const onSelectText = (text, x, y) => {
        console.log(`Selected text: ${text}`)
        console.log(`Coordinates: x=${x}, y=${y}`)
    }

    const onFileDrop = (files) => {
        originalFile.value = currentFile.value = files[0]
        currentFilename.value = files[0].name
    }

    let redactTimeout = ref(null)
    const onOptionsUpdate = (options) => {
        if (JSON.stringify(currentOptions.value) === JSON.stringify(options))
            return

        currentOptions.value = options

        if (redactTimeout.value) {
            clearTimeout(redactTimeout.value)
        }
        redactTimeout.value = setTimeout(() => {
            redactFileData()
        }, 1000)
    }

    const showPopup = (x, y, text) => {
        popup.value.style.left = `${x - 50}px`
        popup.value.style.top = `${y - 50}px`
        popup.value.textContent = text
        popup.value.style.display = 'block'
    }

    const hidePopup = () => {
        popup.value.style.display = 'none'
    }

    const redactFileData = async () => {
        if (!originalFile.value) {
            console.error('No file to redact')
            return
        }
        if (currentOptions.value.length === 0) {
            console.log('No redaction options, resetting file')
            currentFile.value = originalFile.value
            return
        }

        try {
            const formData = new FormData()
            formData.append('file', originalFile.value)
            formData.append('pattern', JSON.stringify(currentOptions.value))
            const response = await fetch('http://localhost:3000/api/redact', {
                method: 'POST',
                body: formData
            })
            
            if (response.headers.get('content-type') === 'application/pdf') {
                const blob = await response.blob()
                const file = new File([blob], 'redacted.pdf', { type: 'application/pdf' })
                currentFile.value = file
            } else {
                try {
                    const data = await response.json()
                }
                catch (error) {
                    console.error('Error parsing redaction response:', error)
                }
            }
        } catch (error) {
            console.error('Error redacting file:', error)
        }

    }

    const downloadFile = async () => {
        // Force download
        const fileBuffer = await currentFile.value.arrayBuffer()
        const blob = new Blob([fileBuffer], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = currentFilename.value ?? 'anonymiseret.pdf'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    const resetFile = () => {
        originalFile.value = null
        currentFile.value = null
        currentFilename.value = null
    }

    // onMounted(() => {
    //     if (pdfContainer.value) {
    //         pdfContainer.value.addEventListener('scroll', () => {
    //             console.log('pdfContainer scrolled')
    //         });
    //     }
    // });
</script>

<template>
    <FileDrop @files-dropped="onFileDrop" v-if="currentFile == null" />
    <div class="mainContainer" v-if="currentFile != null">

        <div ref="pdfContainer" class="pdfContainer">
            <PdfViewer :ref="pdfViewer" :source="currentFile" @text-selected="onSelectText" />
        </div>
        <div class="optionsContainer">
            <div class="options">
                <OptionList @options-updated="onOptionsUpdate" />
            </div>
            <div class="actions">
                <span @click="resetFile()">Start forfra</span>
                <span @click="downloadFile()">Download</span>
            </div>
        </div>
        
    </div>
    
    <div ref="popup" class="popup"></div>
</template>

<style scoped>
    .mainContainer {
        display: flex;
        width: 100%;
        height: 100vh;
    }

    .mainContainer > * {
        overflow-y: auto;
        scrollbar-gutter: stable; /* Use scrollbar-gutter property */
        overflow-x: hidden;
    }
    
    .pdfContainer {
        width: 60%;
    }

    .optionsContainer {
        flex-grow: 1;
        background-color: #eeeeee;
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }

    .options {
        flex-grow: 1;
    }
    .actions {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
        .actions span {
            cursor: pointer;
            background-color: #9fc0e4;
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
        }
        .actions span:hover {
            background-color: #91b2d5;
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