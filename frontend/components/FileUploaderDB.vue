<template>
  <div class="column">
    <q-file
      :model-value="files"
      @update:model-value="updateFiles"
      label="Выбирите файлы"
      outlined
      multiple
      dense
      :loading="loading"
      accept=".pdf, .docx, .doc"
      :clearable="!isUploading"
      style="max-width: 400px"
    >
      <template v-slot:prepend>
        <q-icon name="attach_file" />
      </template>
      <template v-slot:file="{ index, file }">
        <q-chip
          class="full-width q-my-xs"
          :removable="isUploading && uploadProgress[index].percent < 1"
          square
          @remove="cancelFile(index)"
        >
          <q-linear-progress
            class="absolute-full full-height"
            :value="uploadProgress[index].percent"
            :color="uploadProgress[index].color"
            track-color="grey-2"
          />

          <q-avatar>
            <q-icon :name="uploadProgress[index].icon" />
          </q-avatar>

          <div class="ellipsis relative-position">
            {{ file.name }}
          </div>

          <q-tooltip>
            {{ file.name }}
          </q-tooltip>
        </q-chip>
      </template>

      <template v-slot:after v-if="canUpload">
        <q-btn
          color="primary"
          dense
          icon="cloud_upload"
          round
          @click="loadFiles"
          :disable="!canUpload"
          :loading="isUploading"
        />
      </template>
    </q-file>
  </div>
</template>

<script>
import { ref, computed, onBeforeUnmount } from 'vue';
import { getFilesClasses, loadFilesClasses } from '~/shared/api/index.js';

export default {
  emits: ['endLoad'],

  setup(props, ctx) {
    const loading = ref(false);
    const classes = useState('classes', () => []);
    const files = useState('files', () => []);
    const uploadProgress = ref([]);
    const uploading = ref(null);

    function cleanUp() {
      clearTimeout(uploading.value);
    }
    const $q = useQuasar();
    async function loadFiles() {
      try {
        loading.value = true;
        for (const file of files.value) {
          try {
            const temp = await getFilesClasses(file);
            classes.value.push(temp);
          } catch (e) {
            classes.value.push({
              file: file.name,
              result: 'none',
            });
          }
        }
        await loadFilesClasses(files.value, classes.value);
        $q.notify({
          message: 'Документы успешно загружены',
          color: 'green',
          position: 'top',
        });
        loading.value = false;
        ctx.emit('endLoad');
      } catch (e) {
        console.error(e);
      }
    }

    onBeforeUnmount(cleanUp);
    watch(() => files.value, () => {
      if (!files.value) {
        classes.value = [];
      }
    });
    return {
      loadFiles,
      loading,
      files,
      uploadProgress,
      uploading,

      isUploading: computed(() => uploading.value !== null),
      canUpload: computed(() => files.value?.length > 0),

      cancelFile(index) {
        this.uploadProgress[index] = {
          ...this.uploadProgress[index],
          error: true,
          color: 'orange-2',
        };
      },

      updateFiles(newFiles) {
        files.value = newFiles;
        uploadProgress.value = (newFiles || []).map(file => ({
          error: false,
          color: 'green-2',
          percent: 0,
          icon: file.type.indexOf('video/') === 0
            ? 'movie'
            : (file.type.indexOf('image/') === 0
              ? 'photo'
              : (file.type.indexOf('audio/') === 0
                ? 'audiotrack'
                : 'insert_drive_file'
              )
            ),
        }));
      },

      upload() {
        cleanUp();

        const allDone = uploadProgress.value.every(progress => progress.percent === 1);

        uploadProgress.value = uploadProgress.value.map(progress => ({
          ...progress,
          error: false,
          color: 'green-2',
          percent: allDone === true ? 0 : progress.percent,
        }));

        updateUploadProgress();
      },
    };
  },
};
</script>
