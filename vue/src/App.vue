<script setup>
    import FileDrop from './components/FileDrop.vue';
    import PdfViewer from './components/PdfViewer.vue'
    import OptionList from './components/OptionList.vue'
    import Popup from './components/Popup.vue'
    import { ref, watch } from 'vue'

    const pdfContainer = ref(null)
    const pdfViewer = ref(null)
    const popup = ref(null)

    const originalFile = ref(null)
    const currentFilename = ref(null)
    const currentFile = ref(null)
    const currentOptions = ref([])
    const isLoading = ref(false)
    const isShowingPopup = ref(false)
    const popUpCoords = ref({ x: 0, y: 0 })
    const initialPopupY = ref(0)
    const initialScrollY = ref(0)
    const currentSelectedText = ref(null)

    const onSelectText = (text, x = 0, y = 0) => {
        currentSelectedText.value = text
        togglePopUp(text, x, y)
    }

    const onFileDrop = (files) => {
        originalFile.value = currentFile.value = files[0]
        currentFilename.value = files[0].name
    }

    const onLoadingComplete = () => {
        isLoading.value = false
    }

    const onRedactTextSelection = () => {
        OptionList.addOption(currentSelectedText.value)
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

    const togglePopUp = (text, x, y) => {
        if(text == null) {
            isShowingPopup.value = false
            return
        }
        popUpCoords.value = { x, y }
        initialScrollY.value = pdfContainer.value.scrollTop
        initialPopupY.value = y
        isShowingPopup.value = true
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
        
        isLoading.value = true

        try {
            const formData = new FormData()
            formData.append('file', originalFile.value)
            formData.append('pattern', JSON.stringify(currentOptions.value))
            const response = await fetch('/api/redact', {
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
                    console.log('Recieved JSON response:', data)
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
        OptionList.resetOptions()
    }

    watch(() => pdfContainer.value, () => {
        if (pdfContainer.value) {
            pdfContainer.value.addEventListener('scroll', () => {
                let x = popUpCoords.value.x - pdfContainer.value.scrollLeft
                let y = initialPopupY.value - pdfContainer.value.scrollTop + initialScrollY.value
                popUpCoords.value = { x: x, y: y }
            })
        }
    })
</script>

<template>
    <FileDrop @files-dropped="onFileDrop" v-if="currentFile == null" />
    <div class="mainContainer" v-if="currentFile != null">

        <div ref="pdfContainer" :class="['pdfContainer', { 'no-scroll': isLoading }]">
            <div class="loading-screen" v-if="isLoading">
                <span>Indlæser ...</span>
            </div>
            <PdfViewer :ref="pdfViewer" :source="currentFile" @loading-complete="onLoadingComplete" @text-selected="onSelectText" />
        </div>
        <div class="optionsContainer">
            <div class="options">
                <OptionList ref="optionList" @options-updated="onOptionsUpdate" />
            </div>
            <div class="actions">
                <span @click="resetFile()" class="button">
                    <div class="icon-container"><i class="fa-solid fa-rotate-left"></i></div>
                    Start forfra</span>
                <span @click="downloadFile()" class="button yellow">
                    <div class="icon-container"><i class="fa-solid fa-download"></i></div>
                    Download</span>
            </div>
        </div>
        
    </div>
    <Popup :ref="popup" :isVisible="isShowingPopup" :x="popUpCoords.x" :y="popUpCoords.y" @redact-text-selection="onRedactTextSelection" />
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
    .loading-screen {
        position: absolute;
        width: 60%;
        height: 100vh;
        left: 0;
        top: 0;
        background-color: rgba(255, 255, 255, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        pointer-events: none;
    }
    .loading-screen > span {
        transform: translateY(-2rem);
        font-size: 1.5em;
        color: rgb(168, 168, 168);
        font-weight: 400;
    }
    .no-scroll {
        overflow: hidden;
        scrollbar-gutter: stable;
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
        margin-top:1rem;
    }
    .actions > span {
        display: flex;
        gap: 0.5rem;
    }
    .actions > .button {
        font-size: 1em;
    }
    .actions > .button.yellow {
        background-color: #e8eed2;
    }
    .actions > .button.yellow:hover {
        background-color: #dfe4c6;
    }
    .actions > .button.green {
        background-color: #d6efd6;
    }
    .actions > .button.green:hover {
        background-color: #c7e7c7;
    }
    .icon-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .fa-solid {
        color: #2b2b2b;
        font-size: 0.7em;
    }
</style>