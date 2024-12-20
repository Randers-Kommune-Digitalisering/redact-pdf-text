<script>
    const options = ref([
            { id: 1, value: "" }
    ])
    function addOption(text){
        options.value.push({ id: options.value.length + 1, value: text ?? "" })
    }
    function resetOptions(){
        options.value = [{ id: 1, value: "" }]
    }
    export default {
        addOption, resetOptions
    }
</script>
<script setup>
    import { ref, watch } from 'vue'
    const emit = defineEmits(['options-updated'])

    const redactCpr = ref(false)
    const redactCprRegex = "((((0[1-9]|[12][0-9]|3[01])(0[13578]|10|12)(\\d{2}))|(([0][1-9]|[12][0-9]|30)(0[469]|11)(\\d{2}))|((0[1-9]|1[0-9]|2[0-8])(02)(\\d{2}))|((29)(02)(00))|((29)(02)([2468][048]))|((29)(02)([13579][26])))[-]*\\d{4})/regex"
    const redactDateRegex = "(((0[1-9]|[12][0-9]|3[01])(0[13578]|10|12)(\\d{2}))|(([0][1-9]|[12][0-9]|30)(0[469]|11)(\\d{2}))|((0[1-9]|1[0-9]|2[0-8])(02)(\d{2}))|((29)(02)(00))|((29)(02)([2468][048]))|((29)(02)([13579][26])))/regex"
    
    watch(options.value, (newOptions) => {
        emitOptions(newOptions)
    }, { deep: true })

    watch(redactCpr, (newRedactCpr) => {
        emitOptions(options.value)
    })

    const emitOptions = (newOptions) => {
        var optionList = options.value.map(option => option.value)

        if (redactCpr.value)
            optionList.push(redactDateRegex)

        optionList = optionList.filter(option => option.trim() !== "")

        emit('options-updated', optionList)
    }
</script>

<template>
    <div class="optionsParent">
        <span class="header">Hvad skal anonymiseres?</span>
        <div :class="['redact-cpr', { 'green': redactCpr }]">
            <input type="checkbox" id="redact-cpr" name="redact-cpr" value="redact-cpr" v-model="redactCpr" />
            <label for="redact-cpr">Anonymiser CPR-numre</label>
        </div>
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
    .header {
        font-size: 1.2em;
        color: #4d4d4d;
        font-weight: 400;
        margin-bottom: 0.3rem;
    }
    .optionsParent {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        padding-top: 0.8rem;
        padding-left: 0.3rem;
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

    .redact-cpr {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background-color: #efd6d6;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
    .redact-cpr.green {
        background-color: #d6efd6;
    }
    .redact-cpr, .redact-cpr label, .redact-cpr input {
        cursor: pointer;
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