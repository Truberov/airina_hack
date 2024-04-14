<template>
  <div>
    <q-dialog v-model="isNotRequirement" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="tw-text-lg">Найдено несовпадение в предоставленых типах документов. Рекомендуется проверить загруженые документы</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn no-caps label="Иcправить" color="primary" v-close-popup />
          <q-btn no-caps outline label="Все равно отправить" @click="loadFilesAny" color="red" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-list v-if="classes.length > 0">
      <q-item>
        <q-item-section>
          <q-item-label class="tw-text-lg tw-font-bold">Название документа</q-item-label>
        </q-item-section>
        <q-item-section top>
          <q-item-label class="tw-text-lg tw-font-bold">Класс</q-item-label>
        </q-item-section>
        <q-item-section top>
          <q-item-label class="tw-text-lg tw-font-bold">Проверка</q-item-label>
        </q-item-section>
      </q-item>

      <div v-for="item in classes" :key="item.file">
        <q-item>
          <q-item-section>
            <q-item-label class="tw-text-lg">{{item.file}}</q-item-label>
          </q-item-section>

          <q-item-section top>
            <q-item-label caption class="tw-text-lg">{{ classesTranslate[item.result] }}</q-item-label>
          </q-item-section>
          <q-item-section top>
            <q-item-label class="tw-text-lg">
              <q-icon v-if="item.isCheck" color="green" :name="mdiCheckBold" />
              <q-icon v-else color="red" :name="mdiCloseThick" />
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-separator inset />
      </div>
      <q-item>
        <q-btn
          no-caps
          @click="loadFiles"
          color="primary"
          class="tw-mt-10"
        >
          Отправить на проверку
        </q-btn>
      </q-item>
    </q-list>

  </div>
</template>
<script setup>
import { mdiCloseThick, mdiCheckBold } from '@mdi/js';

import { loadFilesClasses } from '~/shared/api/index.js';

const isNotRequirement = ref(false);
const classes = useState('classes');
const files = useState('files');
const classesTranslate = useClassesTranslate();
const requirements = useState('requirements');
function isRequirement() {
  const checkerClasses = {};
  for (const cls of classes.value) {
    if (cls.result in checkerClasses) {
      checkerClasses[cls.result] += 1;
    } else {
      checkerClasses[cls.result] = 1;
    }
  }
  console.log(checkerClasses);
  const checkerRequirements = {};
  for (const cls of requirements.value.classes) {
    checkerRequirements[cls.value.value] = cls.number;
  }
  console.log(checkerRequirements);
  for (const cls of Object.keys(checkerRequirements)) {
    if (!checkerClasses[cls]) {
      return false;
    }
    if (checkerClasses[cls] !== checkerRequirements[cls]) {
      return false;
    }
  }
  return true;
}
const $q = useQuasar();

async function loadFilesAny() {
  try {
    await loadFilesClasses(files.value, classes.value, requirements.value.name);
    $q.notify({
      message: 'Ваши документы успешно отправлены',
      color: 'green',
      position: 'top',
    });
  } catch (e) {
    console.error(e);
  }
}
async function loadFiles() {
  if (isRequirement()) {
    await loadFilesClasses(files.value, classes.value, requirements.value.name);
    $q.notify({
      message: 'Ваши документы успешно отправлены',
      color: 'green',
    });
  } else {
    isNotRequirement.value = true;
  }
}
</script>
