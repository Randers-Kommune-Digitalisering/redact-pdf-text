<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
const emit = defineEmits(['files-dropped'])
const isDragging = ref(false)

function onDrop(e) {
    e.preventDefault()
    isDragging.value = false
    const files = [...e.dataTransfer.files]
    emit('files-dropped', files)
}

function preventDefaults(e) {
    e.preventDefault()
}

function handleDragEnter() {
    isDragging.value = true
}

function handleDragLeave(e) {
    isDragging.value = false
}

const events = ['dragenter', 'dragover', 'dragleave', 'drop']

onMounted(() => {
    const dropZone = document.querySelector('.dropZone')
    if (dropZone) {
        events.forEach((eventName) => {
            dropZone.addEventListener(eventName, preventDefaults)
        })
        dropZone.addEventListener('dragenter', handleDragEnter)
        dropZone.addEventListener('dragleave', handleDragLeave)
        dropZone.addEventListener('drop', handleDragLeave)
    }
})

onUnmounted(() => {
    const dropZone = document.querySelector('.dropZone')
    if (dropZone) {
        events.forEach((eventName) => {
            dropZone.removeEventListener(eventName, preventDefaults)
        })
        dropZone.removeEventListener('dragenter', handleDragEnter)
        dropZone.removeEventListener('dragleave', handleDragLeave)
        dropZone.removeEventListener('drop', handleDragLeave)
    }
})
</script>

<template>
    <div @drop.prevent="onDrop" :class="['dropZone', { 'dragging': isDragging }]"></div>
    <div class="dropOverlay">
        <div>
            <div class="header">Træk og slip</div>
            <div class="subheader">en PDF-fil her for at starte</div>
        </div>
    </div>
</template>

<style scoped>
.dropZone {
    position: absolute;
    width: 100%;
    height: 100vh;
}
    .dropZone.dragging ~ .dropOverlay {
        background-color: rgb(251, 252, 247);
    }
    .dropZone.dragging ~ .dropOverlay > div {
        border: 0.8rem dashed rgba(175, 207, 173, 0.5);
        color: rgb(175, 207, 173);
    }

.dropOverlay {
    background-color: rgb(237, 238, 234);
    transition: 0.3s;

    width: 100%;
    height: 100%;
    padding: 1rem;
    color: rgb(168, 168, 168);
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
</style>