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
          class="text-teal"
        >
          <q-tab name="requirements" label="Предъявляемые требования" />
          <q-tab name="common" :disable="requirements.classes.length && requirements.classes[0].value === '' || requirements.classes.length === 0" label="Загрузка файлов" />
          <q-tab name="archives" label="База архивов" />
          <q-tab name="files" label="База файлов" />
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

          <q-tab-panel name="bank" class="tw-p-20">
            <FilesArchive />
          </q-tab-panel>

          <q-tab-panel name="lawyer">
            <div class="text-h4 q-mb-md">Movies</div>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
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
