<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      title="База архивов"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :rows-per-page-options="[10]"
      binary-state-sort
    >
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="sm" color="primary" flat round dense @click="props.expand = !props.expand" :icon="props.expand ? mdiChevronUp : mdiChevronDown" />
          </q-td>
          <td>
            {{props.row.name}}
          </td>
          <td>
            {{props.row.docs.length}}
          </td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <q-list>
              <q-item dense v-for="item in props.row.docs" :key="item.file">
                <q-item-section>
                  <q-item-label class="tw-text-sm">
                    <NuxtLink :to="item.file" target="_blank">{{item.filename}}</NuxtLink>
                  </q-item-label>
                </q-item-section>
                <q-item-section>
                  <q-item-label caption class="tw-text-sm">{{ classesTranslate[item.predicted_class] }}</q-item-label>
                </q-item-section>
                <q-item-section>
                  <q-item-label caption class="tw-text-sm">{{ format(new Date(item.created_at), 'HH:mm:ss dd.MM.yyyy') }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>

          </q-td>
        </q-tr>
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
import { mdiUploadCircleOutline, mdiChevronDown, mdiChevronUp } from '@mdi/js';
import cloneDeep from 'lodash.clonedeep';
import { getFilesArchives } from '~/shared/api/index.js';
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
const rows = ref([]);
const pagination = ref({});

const columns = [
  {
    name: 'filename',
    required: true,
    label: 'Название aрхива',
    align: 'left',
    field: row => row.filename,
    format: val => `${val}`,
  },
  { name: 'docs', align: 'left', label: 'Количество документов', field: row => row.docs.length },

];
const classesTranslate = useClassesTranslate();
const classesOptions = useClassesTypes();

async function updatePage(page) {
  loading.value = true;
  filterParams.value.page = page;
  const filterParamsCopy = cloneDeep(filterParams.value);
  const temp = await getFilesArchives(filterParamsCopy);
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
  const temp = await getFilesArchives(filterParams);
  pagination.value.rowsNumber = temp.count;
  rows.value = temp.results;
  loading.value = false;
}
export default {
  methods: {
    format },
  async setup() {
    const data = await getFilesArchives(filterParams.value);
    rows.value = data.results;
    pagination.value = {
      page: 1,
      rowsPerPage: 10,
      rowsNumber: data.count,
    };
    return {
      pagination,
      mdiChevronDown,
      mdiChevronUp,
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
