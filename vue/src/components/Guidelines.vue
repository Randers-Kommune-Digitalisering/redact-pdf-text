<script setup>
    import { ref, onMounted } from 'vue'
    import { marked } from 'marked'
    import axios from 'axios'
    import { useCookies } from 'vue3-cookies'

    onMounted(() => {
        const dontShow = cookies.get(cookieName)
        if (dontShow)
            isShowingGuidelines.value = false
        else 
            fetchGuidelines()
    })
</script>
<script>
    const isShowingGuidelines = ref(true)
    const dontShowAgain = ref(false)
    const { cookies } = useCookies()
    const cookieName = 'rk_anonymisering_dontShowGuidelines'

    const guidelinesContent = ref('')

    const fetchGuidelines = async () => {
        try {
            const response = await axios.get('/guidelines.md')
            guidelinesContent.value = marked(response.data)
        } catch (error) {
            console.error('Error fetching guidelines:', error)
        }
    }

    const closeGuidelines = (ignoreSelection = false) => {
        if (!ignoreSelection && dontShowAgain.value)
            cookies.set(cookieName, true, '7d')
        else if (!ignoreSelection)
            cookies.remove(cookieName)
        
        isShowingGuidelines.value = false
    }

    const showGuidelines = () => {
        if (!guidelinesContent.value)
            fetchGuidelines()
        
        isShowingGuidelines.value = true
        dontShowAgain.value = false
    }

    export default {
        showGuidelines
    }
</script>

<template>
    <div class="guidelines" v-if="isShowingGuidelines" @click="closeGuidelines(true)">
        <div @click.stop>
            <div v-html="guidelinesContent"></div>
            <div class="buttons">
            <div :class="['dontShowAgain', { 'green': dontShowAgain }]">
                <input type="checkbox" id="dontShowAgain" name="dontShowAgain" value="dontShowAgain" v-model="dontShowAgain" />
                <label for="dontShowAgain" v-if="!dontShowAgain"><div>Vis ikke denne vejledning igen</div></label>
                <label for="dontShowAgain" v-if="dontShowAgain"><div>Vejledningen skjules i en uge</div></label>
            </div>
            <button @click="closeGuidelines(false)" class="yellow">Bekræft og fortsæt</button>
        </div>
        </div>
        
    </div>
</template>

<style scoped>
.guidelines {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100vh;
    position: fixed;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 11;
}
.guidelines > div {
    font-size: 0.9em;
    color:rgba(7, 7, 7);
    background-color: #f8f8f8;
    padding: 0.8rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 0px 5px rgba(0, 0, 0, 0.2);
    max-width: 60rem;
    margin: 0 1rem;
}
.buttons {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.buttons button {
    font-size: 1em;
}
.dontShowAgain {
    display:flex;
    gap: 0.4rem;
    transform: translateY(0rem);
}
.dontShowAgain > label {
    transform: translateY(-0.03rem);
}
</style>