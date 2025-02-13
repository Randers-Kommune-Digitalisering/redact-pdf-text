<script setup>
import { ref } from 'vue'
const isShowingGuidelines = ref(true)
const dontShowAgain = ref(false)

const closeGuidelines = () => {
    isShowingGuidelines.value = false
}
</script>

<template>
    <div class="guidelines" v-if="isShowingGuidelines" @click="closeGuidelines">
        <div @click.stop>
            <h2>Vejledning – Randers Kommunes anonymiseringsværktøj</h2>

            <p>Randers Kommunes anonymiseringsværktøj hjælper medarbejdere med at maskere ord og sætninger i en pdf-fil, så de permanent skjules og ikke kan genskabes. Værktøjet kan blandt andet bruges til at fjerne persondata fra dokumenter i overensstemmelse med gældende lovgivning om databeskyttelse.</p>

            <h3>Sådan bruger du værktøjet:</h3>

            <ol>
            <li>Upload den ønskede pdf-fil.</li>
            <li>Marker de ord eller sætninger, der skal anonymiseres, og klik på Anonymiser.</li>
            <li>Hvis dokumentet indeholder CPR-numre, kan du vælge at krydse feltet Anonymiser CPR-numre af for at fjerne dem automatisk.</li>
            <li>Gem den anonymiserede fil og verificér resultatet.</li>
            </ol>

            <h3>Det er brugerens ansvar at</h3>

            <ul>
            <li>Gennemlæse dokumentet grundigt efter anonymisering for at sikre, at alle relevante oplysninger, såsom CPR-numre, navne og andre følsomme data, er fjernet.</li>
            <li>Følge Randers Kommunes databeskyttelsespolitikker og de gældende regler for håndtering af personoplysninger, herunder GDPR.</li>
            </ul>

            <h3>Sletning af original fil</h3>

            <p>Når arbejdet er færdigt, skal den originale fil, hvis den indeholder persondata, slettes fra computeren i overensstemmelse med Randers Kommunes sletteregler. Dette er en vigtig del af at sikre korrekt databeskyttelse.</p>
        
            <div class="buttons">
                <div :class="['dontShowAgain', { 'green': dontShowAgain }]" v-if="false">
                    <input type="checkbox" id="dontShowAgain" name="dontShowAgain" value="dontShowAgain" v-model="dontShowAgain" />
                    <label for="dontShowAgain"><div>Vis ikke denne vejledning igen</div></label>
                </div>
                <button @click="closeGuidelines" class="yellow">Bekræft og fortsæt</button>
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
button.green {
    background-color: #d6efd6;
}
button.green:hover {
    background-color: #c7e7c7;
}
button.yellow {
        background-color: #e8eed2;
}
button.yellow:hover {
    background-color: #dfe4c6;
}
</style>