<template>
  <div class="tw-p-20">
    <q-dialog v-model="dialogUploading">
      <q-card>
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Загрузка документов в базу</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <FileUploaderDB @end-load="updateDB" />
        </q-card-section>
      </q-card>
    </q-dialog>
    <div class="tw-flex tw-items-center tw-justify-between">
      <div class="tw-mb-10 tw-mr-10 tw-w-1/5">
        <q-select clearable filled label="Фильтр классов" v-model="filter" :options="classesOptions" dense class="tw-w-full tw-mr-10" />
      </div>
      <div class="tw-mb-10">
        <q-icon @click="dialogUploading = true" color="primary" class="tw-cursor-pointer" size="32px" :name="mdiUploadCircleOutline" />

      </div>
    </div>
    <q-table
      flat
      bordered
      title="База файлов"
      :rows="rows"
      :columns="columns"
      :loading="loading"
      row-key="name"
      :rows-per-page-options="[10]"
      binary-state-sort
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="filename" :props="props">
            <NuxtLink target="_blank" :to="props.row.file">
              {{ props.row.filename }}
            </NuxtLink>
          </q-td>
          <q-td key="predicted_class" :props="props">
            {{ classesTranslate[props.row.predicted_class] }}
          </q-td>
          <q-td key="created_at" :props="props">
            {{ format(new Date(props.row.created_at), 'HH:mm:ss dd.MM.yyyy') }}
          </q-td>
        </q-tr>
      </template>
      <template v-slot:top-right>
        <div class="tw-flex">
          <q-input dense debounce="300" v-model="search" placeholder="Поиск">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </template>
      <template v-slot:pagination>
        <div class="row justify-start">
          <q-pagination
            v-if="10 < pagination.rowsNumber"
            v-model="pagination.page"
            @update:model-value="updatePage(pagination.page)"
            :max="Math.ceil(pagination.rowsNumber / pagination.rowsPerPage)"
            direction-links
            flat
            active-color="primary"
          />
        </div>
      </template>
    </q-table>
  </div>
</template>

<script>
import { ref } from 'vue';
import { format } from 'date-fns';
import { mdiUploadCircleOutline } from '@mdi/js';
import cloneDeep from 'lodash.clonedeep';
import { getFiles } from '~/shared/api/index.js';
import { useClassesTranslate, useClassesTypes } from '~/composables/classesDict.js';

const dialogUploading = ref(false);
const loading = ref(false);
const files = ref(null);
const filter = ref('');
const search = ref('');
const filterParams = ref({
  page: 1,
  ordering: '-created_at',
});
const columns = [
  {
    name: 'filename',
    required: true,
    label: 'Название документа',
    align: 'left',
    field: row => row.filename,
    format: val => `${val}`,
  },
  { name: 'predicted_class', align: 'left', label: 'Класс документа', field: row => classesTranslate.value[row.predicted_class] },
  { name: 'created_at', align: 'left', label: 'Дата загрузки', field: row => format(new Date(row.created_at), 'HH:mm:ss dd.MM.yyyy'), sortable: true },

];
const classesTranslate = useClassesTranslate();
const classesOptions = useClassesTypes();
const rows = ref([]);
const data = await getFiles(filterParams.value);
rows.value = data.results;
const pagination = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: data.count,
});
async function updatePage(page) {
  loading.value = true;
  filterParams.value.page = page;
  const filterParamsCopy = cloneDeep(filterParams.value);
  const temp = await getFiles(filterParamsCopy);
  rows.value = temp.results;
  pagination.value.rowsNumber = temp.count;
  loading.value = false;
}
watch(() => search.value, () => {
  if (search.value) {
    filterParams.value.filename = search.value;
  } else {
    delete filterParams.value.filename;
  }
  updatePage(1);
});
watch(() => filter.value, () => {
  if (filter.value?.value) {
    filterParams.value.predicted_class = filter.value.value;
  } else {
    delete filterParams.value.predicted_class;
  }
  updatePage(1);
});

async function updateDB() {
  dialogUploading.value = false;
  loading.value = true;
  filterParams.value = { page: 1 };
  const temp = await getFiles(filterParams);
  pagination.value.rowsNumber = temp.count;
  rows.value = temp.results;
  loading.value = false;
}
export default {
  methods: {
    format },
  setup() {
    return {
      pagination,
      updatePage,
      search,
      loading,
      dialogUploading,
      updateDB,
      mdiUploadCircleOutline,
      filter,
      classesOptions,
      classesTranslate,
      columns,
      files,
      rows: ref(rows),
    };
  },
};
</script>
