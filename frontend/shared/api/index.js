import { useBaseFetch } from '~/composables/useBaseFetch.js';

export async function getFilesClasses(file) {
  const formData = new FormData();
  formData.append('file', file);

  const { data } = await useBaseFetch('/classification', {
    method: 'POST',
    body: formData,
  });

  return data.value;
}
