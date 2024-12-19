<script setup>
    import { ref, watch } from 'vue'
    const emit = defineEmits(['options-updated'])

    const options = ref([
        { id: 1, value: "Test1" },
        { id: 2, value: "Test2" }
    ])
    
    watch(options.value, (newOptions) => {
        var optionList = newOptions.map(option => option.value)
        emit('options-updated', optionList)
    }, { deep: true })
</script>

<template>
    <div v-for="option in options" :key="option.id" class="option">
        <input type="text" v-model="option.value" />
    </div>
</template>