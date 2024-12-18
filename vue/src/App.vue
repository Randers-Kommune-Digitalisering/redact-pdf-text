<script setup>
    import PdfViewer from './components/PdfViewer.vue';
</script>

<template>
<div class="mainContainer">
    <div class="pdfContainer"><PdfViewer source="./input.pdf" /></div>
    <div class="optionsContainer">Test 2</div>
</div>
</template>

<style scoped>
    .mainContainer {
        display: flex;
        width: 100%;
        max-height: 100vh;
    }

    .mainContainer > * {
        overflow-y: auto;
        scrollbar-gutter: stable; /* Use scrollbar-gutter property */
        overflow-x: hidden;
    }
    
    .pdfContainer {
        width: 60%;
    }

    .optionsContainer {
        flex-grow: 1;
        background-color: #eeeeee;
    }
</style>