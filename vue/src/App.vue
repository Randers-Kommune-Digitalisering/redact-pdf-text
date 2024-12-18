<script setup>
    import PdfViewer from './components/PdfViewer.vue'
    import { onMounted, ref } from 'vue'

    const pdfContainer = ref(null)
    const pdfViewer = ref(null)
    const popup = ref(null)

    const onSelectText = (text, x, y) => {
        console.log(`Selected text: ${text}`)
        console.log(`Coordinates: x=${x}, y=${y}`)
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

    // onMounted(() => {
    //     if (pdfContainer.value) {
    //         pdfContainer.value.addEventListener('scroll', () => {
    //             console.log('pdfContainer scrolled')
    //         });
    //     }
    // });
</script>

<template>
    <div class="mainContainer">

        <div ref="pdfContainer" class="pdfContainer">
            <PdfViewer :ref="pdfViewer" source="./input.pdf" @selectText="onSelectText" />
        </div>
        <div class="optionsContainer">Test 2</div>
        
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