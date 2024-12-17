<script setup>
    import Content from '@/components/Content.vue'
    import Status from '@/components/Status.vue'

    import IconOK from '@/components/icons/IconOK.vue'
    import IconRSS from '@/components/icons/IconRSS.vue'
</script>

<template>
    <h2>Flask + Vue Template</h2>

    <Content>
        <template #icon>
            <IconOK />
        </template>
        <template #heading>Sådan, det ser ud til at køre!</template>
        
        Du har nu succesfuldt startet et nyt projekt med <a href="https://github.com/Randers-Kommune-Digitalisering/vue-python-template" target="_blank" rel="noopener">Randers Kommune's Flask + Vue template</a>.
    </Content>

    <Content>
        <template #icon>
            <IconRSS />
        </template>
        <template #heading>Status på opsætning</template>
        
        <Status />
    </Content>

</template>