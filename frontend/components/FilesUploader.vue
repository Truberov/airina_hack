<template>
  <div class="column">
    <q-file
      :model-value="files"
      @update:model-value="updateFiles"
      label="Выбирите файлы"
      outlined
      multiple
      dense
      use-chips
      :loading="loading"
      accept=".pdf, .docx, .doc"
      :clearable="!isUploading"
      style="max-width: 600px"
      counter
      :max-files="requirements.classes.length"
    >
      <template v-slot:prepend>
        <q-icon name="attach_file" />
      </template>
      <template v-slot:file="{ index, file }">
        <q-chip
          class="full-width q-my-xs"
          square
          removable
          @remove="cancelFile(index)"
        >

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
          @click="upload"
          :disable="!canUpload"
          :loading="isUploading"
        />
      </template>
    </q-file>
  </div>
</template>

<script>
import { ref, computed, onBeforeUnmount } from 'vue';
import cloneDeep from 'lodash.clonedeep';
import { getFilesClasses, loadFilesClasses } from '~/shared/api/index.js';

export default {
  setup() {
    const loading = ref(false);
    const classes = useState('classes', () => []);
    const files = useState('files', () => []);
    const uploadProgress = ref([]);
    const uploading = ref(null);
    const requirements = useState('requirements');
    function cleanUp() {
      clearTimeout(uploading.value);
    }
    async function updateUploadProgress() {
      loading.value = true;
      const requirementsCopy = cloneDeep(requirements.value);

      for (const file of files.value) {
        try {
          const temp = await getFilesClasses(file);
          temp.isCheck = false;
          requirementsCopy.classes = requirementsCopy.classes.filter((item) => {
            console.log(item);
            if (item.value.value === temp.result) {
              temp.isCheck = true;
            } else {
              return item;
            }
          });
          console.log(requirementsCopy);
          classes.value.push(temp);
        } catch (e) {
          console.error(e);
          classes.value.push({
            file: file.name,
            result: 'none',
          });
        }
      }

      loading.value = false;

      // uploadProgress.value = uploadProgress.value.map(progress => {
      //   if (progress.percent === 1 || progress.error === true) {
      //     return progress;
      //   }
      //
      //   const percent = Math.min(1, progress.percent + Math.random() / 10);
      //   const error = percent < 1 && Math.random() > 0.95;
      //
      //   if (error === false && percent < 1 && done === true) {
      //     done = false;
      //   }
      //
      //   return {
      //     ...progress,
      //     error,
      //     color: error === true ? 'red-2' : 'green-2',
      //     percent,
      //   };
      // });
      //
      // uploading.value = done !== true
      //   ? setTimeout(updateUploadProgress, 300)
      //   : null;
    }

    onBeforeUnmount(cleanUp);
    watch(() => files.value, () => {
      if (!files.value) {
        classes.value = [];
      }
    });
    return {
      loading,
      files,
      uploadProgress,
      requirements,
      uploading,

      isUploading: computed(() => uploading.value !== null),
      canUpload: computed(() => files.value?.length > 0),

      cancelFile(index) {
        files.value = files.value.filter((f, i) => i !== index);
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
