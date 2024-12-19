<script setup>
    import { ref, watch } from 'vue'
    const emit = defineEmits(['options-updated'])

    const options = ref([
        { id: 1, value: "" }
    ])
    
    watch(options.value, (newOptions) => {
        var optionList = newOptions.map(option => option.value)
        emit('options-updated', optionList)
    }, { deep: true })
</script>

<template>
    <div class="optionsContainer">
        <div v-for="option in options" :key="option.id" class="option">
            <input type="text" v-model="option.value" placeholder="Tekst der skal anonymiseres .." />
            <span class="delete">
                <button @click="options.splice(options.indexOf(option), 1)">X</button>
            </span>
        </div>
        <button @click="options.push({ id: options.length + 1, value: '' })">Tilføj anonymisering</button>
    </div>
</template>

<style scoped>
    .optionsContainer {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .option {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .option input {
        width: 100%;
        line-height: 2em;
        padding: 0 0.5rem;
        font-size: 1em;
    }

    .delete {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    button {
        padding: 0.5rem 1rem;
        background-color: #9fc0e4;
        border: none;
        cursor: pointer;
        border-radius: 0.25rem;
    }
    .delete > button {
        background-color: #d7d0d0;
    }
</style>