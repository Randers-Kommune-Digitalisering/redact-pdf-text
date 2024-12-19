<script setup>
    import { onMounted, onUnmounted } from 'vue'
    const emit = defineEmits(['files-dropped'])

    function onDrop(e) {
        e.preventDefault()
        const files = [...e.dataTransfer.files]
        // files.forEach(file => {
        //     const reader = new FileReader()
        //     reader.onload = (event) => {
        //         const arrayBuffer = event.target.result
        //     }
        //     reader.readAsArrayBuffer(file)
        // })
        emit('files-dropped', files);
        // emit('files-dropped', [...e.dataTransfer.files])
    }

    function preventDefaults(e) {
        e.preventDefault()
    }

    const events = ['dragenter', 'dragover', 'dragleave', 'drop']

    onMounted(() => {
        events.forEach((eventName) => {
            document.body.addEventListener(eventName, preventDefaults)
        })
    })

    onUnmounted(() => {
        events.forEach((eventName) => {
            document.body.removeEventListener(eventName, preventDefaults)
        })
    })
</script>

<template>
    <div @drop.prevent="onDrop" class="dropZone">
        <div class="dropOverlay">
            <div>
                <div class="header">Træk og slip</div>
                <div class="subheader">en PDF-fil her for at starte</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .dropZone {
        background-color: rgb(237, 238, 234);
        width: 100%;
        height: 100vh;
    }
    .dropOverlay {
        width: 100%;
        height: 100%;
        padding: 1rem;
        color: rgb(168, 168, 168);
    }
    .dropOverlay > div {
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