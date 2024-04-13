<template>
  <div>
    <q-dialog v-model="isNotRequirement" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="tw-text-lg">Найдено не совпадение в предоставленых типах документов. Рекомендуется проветь загруженые документы</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn no-caps label="Назад" color="primary" v-close-popup />
          <q-btn no-caps flat label="Все равно сохранить" @click="loadFilesAny" color="red" v-close-popup />
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
      </q-item>

      <div v-for="item in classes" :key="item.file">
        <q-item>
          <q-item-section>
            <q-item-label class="tw-text-lg">{{item.file}}</q-item-label>
          </q-item-section>
          <q-item-section top>
            <q-item-label caption class="tw-text-lg">{{ classesTranslate[item.result] }}</q-item-label>
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
          Сохранить
        </q-btn>
      </q-item>
    </q-list>

  </div>
</template>
<script setup>
import { loadFilesClasses } from '~/shared/api/index.js';

const isNotRequirement = ref(false);
const classes = useState('classes');
const files = useState('files');
const classesTranslate = {
  proxy: 'Доверенность',
  contract: 'Договор',
  act: 'Акт',
  application: 'Заявление',
  order: 'Приказ',
  invoice: 'Счет',
  bill: 'Приложение',
  arrangement: 'Соглашение',
  contractOffer: 'Договор оферты',
  statute: 'Устав',
  determination: 'Решение',
};
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
    await loadFilesClasses(files.value, classes.value);
    $q.notify({
      message: 'Пакет документов сохранен. Из-за несовпадения время проверки увеличено',
      color: 'green',
      position: 'top',
    });
  } catch (e) {
    console.error(e);
  }
}
async function loadFiles() {
  if (isRequirement()) {
    await loadFilesClasses(files.value, classes.value);
    $q.notify({
      message: 'Пакет документов сохранен',
      color: 'green',
    });
  } else {
    isNotRequirement.value = true;
  }
}
</script>
