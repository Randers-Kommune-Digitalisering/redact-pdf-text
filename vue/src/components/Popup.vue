<script setup>
    import { ref, watch } from 'vue'

    const xOffset = -10
    const yOffset = -50

    const popup = ref(null)
    const isVisible = ref(false)
    const props = defineProps({
        isVisible: {
            type: Boolean,
            default: false
        },
        x: {
            type: Number,
            default: 0
        },
        y: {
            type: Number,
            default: 0
        }
    })

    watch(() => props.isVisible, (newValue) => {
        isVisible.value = newValue
        popup.value.style.display = isVisible.value ? 'block' : 'none'
    })

    watch(() => props.x, (newValue) => {
        popup.value.style.left = `${newValue + xOffset}px`
    })

    watch(() => props.y, (newValue) => {
        popup.value.style.top = `${newValue + yOffset}px`
    })

    const emit = defineEmits(['redact-text-selection'])
    const redactText = () =>{
        isVisible.value = false
        popup.value.style.display = 'none'
        emit('redact-text-selection')
    }

</script>

<template>
    <div ref="popup" class="popup button" @click="redactText()">+ Anonymiser</div>
</template>

<style scoped>
    .popup {
        font-size: 0.8em;
        position: absolute;
        display: none;
        box-shadow: 0 0px 5px rgba(0, 0, 0, 0.2);
        z-index: 1000;
    }
</style>