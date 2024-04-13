<template>
  <div>
    <h1 class="tw-text-3xl tw-mb-5">Загрузите файлы</h1>
    <FilesUploader class="tw-mb-10" />

    <ClassifiedTable />

  </div>
</template>

<script setup>
const splitterModel = ref(50);
</script>
