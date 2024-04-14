<template>
  <div>
    <h1 class="tw-text-3xl">Загрузите файлы</h1>
    <p class="tw-mb-5 tw-text-gray-400 tw-text-base"> {{ docsTypes }}</p>
    <FilesUploader class="tw-mb-10" />

    <ClassifiedTable />

  </div>
</template>

<script setup>
import { mdiHelpCircleOutline } from '@mdi/js';

const requirements = useState('requirements');
const docsTypes = ref('');
onMounted(() => {
  docsTypes.value = requirements.value.classes.map((cls) => cls.value.label).join(', ');
});
</script>
