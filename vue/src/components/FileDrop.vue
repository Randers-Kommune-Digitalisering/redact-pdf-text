<script setup>
    import { ref, onMounted, onUnmounted } from 'vue'
    import Notification from './Notification.vue'

    const emit = defineEmits(['files-dropped', 'open-file-dialog'])
    const isDragging = ref(false)
    const showErrorNotification = ref(false)
    const dragDepth = ref(0)

    function onDrop(e) {
        e.preventDefault()
        dragDepth.value = 0
        isDragging.value = false
        const files = [...e.dataTransfer.files]
        const pdfFiles = files.filter(file => file.type === 'application/pdf')
        if (pdfFiles.length > 0) {
            emit('files-dropped', pdfFiles)
        } else {
            showErrorNotification.value = true
            setTimeout(() => {
                showErrorNotification.value = false
            }, 8000)
        }
    }

    function preventDefaults(e) {
        e.preventDefault()
    }

    function handleDragEnter(e) {
        preventDefaults(e)
        dragDepth.value += 1
        isDragging.value = true
    }

    function handleDragLeave(e) {
        preventDefaults(e)
        dragDepth.value = Math.max(0, dragDepth.value - 1)
        isDragging.value = dragDepth.value > 0
    }

    function onOpenFileDialog() {
        if (isDragging.value) {
            return
        }
        emit('open-file-dialog')
    }

    onMounted(() => {
        window.addEventListener('dragenter', handleDragEnter)
        window.addEventListener('dragover', preventDefaults)
        window.addEventListener('dragleave', handleDragLeave)
        window.addEventListener('drop', onDrop)
    })

    onUnmounted(() => {
        window.removeEventListener('dragenter', handleDragEnter)
        window.removeEventListener('dragover', preventDefaults)
        window.removeEventListener('dragleave', handleDragLeave)
        window.removeEventListener('drop', onDrop)
    })
</script>

<template>
    <div @drop.prevent.stop="onDrop" :class="['dropZone', { 'dragging': isDragging }]" ></div>
    <div class="dropOverlay">
        <div>
            <div class="header">Træk og slip</div>
            <div class="subheader">en <span class="heavy">PDF</span>-fil her for at starte, eller</div>
            <div :class="['button', { 'button-disabled': isDragging }]" @click="onOpenFileDialog">Tryk her for at vælge en fil</div>
        </div>
    </div>
    <Notification title="Forkert filtype" text="Det er kun muligt at anonymisere PDF-filer" v-if="showErrorNotification" />
</template>

<style scoped>
.dropZone {
    position: absolute;
    width: 100%;
    height: 100vh;
    z-index: 1;
}
    .dropZone.dragging ~ .dropOverlay {
        background-color: rgb(251, 252, 247);
    }
    .dropZone.dragging ~ .dropOverlay > div {
        border: 0.8rem dashed rgba(175, 207, 173, 0.5);
        color: rgb(175, 207, 173);
    }

.dropOverlay {
    position: relative;
    z-index: 2;
    pointer-events: none;
    background-color: rgb(237, 238, 234);
    transition: 0.3s;

    width: 100%;
    height: 100%;
    padding: 1rem;
    color: rgb(168, 168, 168);
    user-select: none;
}
    .dropOverlay > div {
        transition: 0.3s;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 1rem;
        border: 0.8rem dashed rgb(187, 186, 186, 0.5);
    }
    .dropOverlay .header {
        font-size: 2.5em;
        font-weight: 400;
    }
    .dropOverlay .subheader {
        font-size: 1.5em;
    }
    .heavy {
        font-weight: 400;
    }
.button {
    pointer-events: auto;
    cursor: pointer;
    font-size: 1em;
    color: rgb(129, 129, 129);
    transition: opacity 0.3s, background-color 0.2s;
}
.button-disabled {
    pointer-events: none;
    opacity: 0.3;
}
</style>