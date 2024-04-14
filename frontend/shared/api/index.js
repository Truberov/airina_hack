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
export async function loadFilesClasses(files, predicted, name = '') {
  const formData = new FormData();
  console.log(files);
  formData.append('name', name);
  files.map((file) => {
    formData.append('docs', file);
  });

  files.map((file) => {
    formData.append('docs_names', file.name);
  });
  predicted.map((p) => {
    formData.append('docs_classes', p.result);
  });
  const { data } = await useBaseFetch('http://10.0.24.56:8000/api/archives/', {
    method: 'POST',
    body: formData,
  });

  return data.value;
}
export async function getFiles(params) {
  const { data } = await useBaseFetch('http://10.0.24.56:8000/api/documents/', {
    method: 'GET',
    query: params,
  });

  return data.value;
}

export async function getFilesArchives(params) {
  const { data } = await useBaseFetch('', {
    method: 'GET',
    query: params,
  });

  return data.value;
}
