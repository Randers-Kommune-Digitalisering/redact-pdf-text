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
        <slot></slot>
    </div>
</template>

<style scoped>
    .dropZone {
        background-color: aquamarine;
        width: 100%;
        height: 100vh;
    }
</style>