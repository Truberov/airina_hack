<template>
  <div class="">
    <q-splitter
      class="tw-h-screen"
      v-model="splitterModel"
    >

      <template v-slot:before>

        <q-tabs
          v-model="tab"
          vertical
          class="tw-text-gray-400 tw-py-20"
        >
          <p align="center" class="tw-text-black tw-font-bold tw-text">Заказчик</p>
          <q-tab no-caps name="requirements" label="Предъявляемые требования" />

          <q-tab no-caps name="archives" label="База архивов" />
          <q-tab no-caps name="files" label="Все файлы" />
          <q-separator inset />
          <p align="center" class="tw-text-black tw-font-bold tw-text tw-pt-20">Пользователь</p>

          <q-tab no-caps name="common" id="load" :disable="requirements.classes.length && requirements.classes[0].value === '' || requirements.classes.length === 0" label="Загрузка файлов" />
          <q-tooltip v-if="requirements.classes.length && requirements.classes[0].value === '' || requirements.classes.length === 0" class="tw-text-base tw-w-40" target="#load">
            Заказчику нужно предъявить требования перед тем как пользователю загрузить документы
          </q-tooltip>
          <div class="tw-opacity-70 tw-h-3/5 tw-justify-end tw-text-sky-500 tw-flex tw-flex-col hover:tw-pb-0 tw-align-bottom tw-items-center tw-text-3xl tw-font-bold">
            <p align="center" class="tw-text-gray-400 tw-w-2/3 tw-text-base tw-font-normal tw-pb-5">
              Кейс ООО «Акселератор Возможностей» при ИНТЦ МГУ «Воробьевы горы»:
              "Семантическая классификация документов"</p>
            <div class="tw-flex tw-items-center">
              <q-icon class="hover:tw-animate-bounce tw-mr-2 tw-bg-gradient-to-r tw-from-sky-500 tw-to-indigo-500 tw-bg-clip-text tw-inline-block tw-text-transparent" name="font_download" />
              <span class="tablet:tw-block tw-hidden">AiRina</span>
            </div>
          </div>
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab"
          animated
          swipeable
          vertical
          transition-prev="jump-up"
          transition-next="jump-up"
          class="tw-flex tw-h-full"
        >
          <q-tab-panel name="requirements" class="tw-p-20 tw-h-full">
            <RequirementsField />
          </q-tab-panel>
          <q-tab-panel name="common" class="tw-p-20">
            <FilesUploaderView />
          </q-tab-panel>

          <q-tab-panel name="archives" class="tw-p-20">
            <FilesArchive />
          </q-tab-panel>

          <q-tab-panel name="files">
            <AllFiles />
          </q-tab-panel>
        </q-tab-panels>
      </template>

    </q-splitter>
  </div>
</template>

<script setup>
import RequirementsField from '~/components/RequirementsField.vue';

function getRandomId() {
  return Math.random().toString(36).substr(2, 9);
}
const requirements = useState('requirements', () => ({
  name: '',
  classes: [{
    id: getRandomId(),
    value: '',
    number: 1,
  }],
}));
const tab = useState('tab', () => 'requirements');
const splitterModel = ref(20);

</script>
