<script setup>
    import FileDrop from './components/FileDrop.vue';
    import PdfViewer from './components/PdfViewer.vue'
    import { onMounted, ref } from 'vue'

    const pdfContainer = ref(null)
    const pdfViewer = ref(null)
    const popup = ref(null)

    const currentFile = ref(null)

    const onSelectText = (text, x, y) => {
        console.log(`Selected text: ${text}`)
        console.log(`Coordinates: x=${x}, y=${y}`)
    }

    const onFileDrop = (files) => {
        currentFile.value = files[0]
        console.log('File dropped:', files[0])
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
        try {
            // const fileBuffer = await currentFile.value.arrayBuffer()
            const formData = new FormData();
            formData.append('file', currentFile.value);
            formData.append('pattern', 'person');
            const response = await fetch('http://localhost:3000/api/redact', {
                method: 'POST',
                body: formData
            })
            
            if (response.headers.get('content-type') === 'application/pdf') {
                const blob = await response.blob();
                const file = new File([blob], 'redacted.pdf', { type: 'application/pdf' });
                currentFile.value = file;
                // Force download
                // const url = URL.createObjectURL(blob);
                // const link = document.createElement('a');
                // link.href = url;
                // link.download = 'redacted.pdf';
                // document.body.appendChild(link);
                // link.click();
                // document.body.removeChild(link);
            } else {
                try {
                    const data = await response.json();
                    console.log('Redaction response:', data);
                }
                catch (error) {
                    console.error('Error parsing redaction response:', error);
                }
            }




        } catch (error) {
            console.error('Error redacting file:', error);
        }

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
            <PdfViewer :ref="pdfViewer" :source="currentFile" @selectText="onSelectText" />
        </div>
        <div class="optionsContainer"><span @click="redactFileData()">Test 2</span></div>
        
    </div>
    
    <div ref="popup" class="popup"></div>
</template>

<style scoped>
    .mainContainer {
        display: flex;
        width: 100%;
        max-height: 100vh;
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