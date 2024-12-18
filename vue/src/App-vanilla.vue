<script setup>
import { ref, onMounted } from 'vue'

var defaultState = ref({
    pdf: null,
    currentPage: 1,
    zoom: 1
})

// GET OUR PDF FILE
pdfjsLib.getDocument('/input.pdf').then((pdf) => {

    defaultState.value.pdf = pdf;
    render();

});

// RENDER PDF DOCUMENT
function render() {
    defaultState.value.pdf.getPage(defaultState.value.currentPage)
    .then((page) =>
    {
        var canvas = document.getElementById("pdf_renderer");
        var ctx = canvas.getContext('2d');

        var viewport = page.getViewport(defaultState.value.zoom);

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        page.render({
            canvasContext: ctx,
            viewport: viewport
        })
    })
}
</script>

<template>

    <div id="canvas_container">
        <canvas id="pdf_renderer"></canvas>
    </div>

</template>


<style scoped>
#canvas_container, #pdf_renderer
{
    max-height: 100vh;
    max-width: 50vw;
}
</style>