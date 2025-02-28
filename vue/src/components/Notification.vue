<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
    title: {
        type: String
    },
    text: {
        type: String
    }
})

const notification = ref(null);

onMounted(() => {
    setTimeout(() => {
        notification.value.classList.add('fade');
    }, 100); // Add a short delay before adding the fade class
})
</script>

<template>
    <div ref="notification" class="notification">
        <div>
            <span class="title">{{title}}</span>
            <span>{{text}}</span>
        </div>
    </div>
</template>

<style scoped>
.notification {
    position: absolute;
    top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    z-index: 12;
    opacity: 1;
}
.notification > div {
    font-size: 0.9em;
    color:rgb(58, 58, 58);
    background-color: #efd6d6;
    padding: 0.8rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 0px 5px rgba(0, 0, 0, 0.05);
    max-width: 50rem;
    margin: 0 0.5rem;
    margin-top: 10vh;

    display: flex;
    flex-direction: column;
    align-items: center;
}
.title {
    font-size: 1.3em;
    margin-bottom: 0.5rem;
    color:rgb(37, 37, 37);
}
.fade {
    opacity: 0;
    transition: opacity 3s;
    transition-delay: 5s;
}
</style>