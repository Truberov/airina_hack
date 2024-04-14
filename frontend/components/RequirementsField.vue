<template>
  <div class="tw-h-full">
    <h1 class="tw-text-3xl tw-mb-10">Выставление требований</h1>
    <q-form
      ref="formRequirements"
      class="q-gutter-md tw-h-full tw-flex tw-flex-col tw-justify-between tw-w-1/2"
    >
      <div>
        <q-input
          filled
          type="string"
          v-model="requirements.name"
          label="Названия пакета документов"
          lazy-rules
          :rules="[
            val => val !== null && val !== '' || 'Пожалуйста введите название пакета',
          ]"
        />
        <div>
          <div v-if="requirements.classes.length" class="tw-text-lg tw-flex tw-justify-between">
            <div>
              Название класса
            </div>
            <!--            <div class="w-1/3">-->
            <!--              Количество-->
            <!--            </div>-->
          </div>
          <div
            v-for="cls in requirements.classes"
            :key="cls.id"
            class="tw-flex tw-justify-between tw-mb-5"
          >
            <div class="tw-grow">
              <q-select
                v-model="cls.value"
                option-label="label"
                option-value="value"
                dense
                class="tw-grow"
                filled
                :rules="[
                  val => val !== null && val !== '' || 'Пожалуйста выбирите тип документа',
                ]"
                @update:model-value="disableCls"
                :options="classesOptions"
              >
                <template #append>
                  <q-icon @click="deleteCls(cls)" :name="mdiTrashCanOutline" />
                </template>
              </q-select>
            </div>
            <!--            <div class="w-1/3 ">-->
            <!--              <q-input-->
            <!--                v-model="cls.number"-->
            <!--                filled-->
            <!--                dense-->
            <!--                type="number"-->
            <!--                :rules="[-->
            <!--                  val => val !== null && val > 0 || `Напишите сколько необходимо`,-->
            <!--                ]"-->
            <!--              />-->
            <!--            </div>-->
          </div>
        </div>
        <div
          @click="addClass"
          class="tw-text-xl hover:tw-text-secondary tw-cursor-pointer"
        >+ добавить класс
        </div>
      </div>
      <div>
        <q-btn label="Выставить требования" no-caps @click="chooseRequirements" color="primary" />
        <q-btn label="Сбросить" type="reset" @click="resetRequirements" no-caps color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>
  </div>
</template>

<script setup>
import { mdiTrashCanOutline } from '@mdi/js';

function getRandomId() {
  return Math.random().toString(36).substr(2, 9);
}
const formRequirements = ref(null);
const requirements = useState('requirements', () => ({
  name: '',
  classes: [{
    id: getRandomId(),
    value: '',
    number: 1,
  }],
}));
const $q = useQuasar();
function resetRequirements() {
  requirements.value.classes = [];
  requirements.value.name = '';
  classesOptions.value = classesOptions.value.map((cls) => ({
    ...cls,
    disable: false,
  }
  ));
}
const tab = useState('tab');
function chooseRequirements() {
  if (requirements.value.classes.length > 0) {
    formRequirements.value.validate().then((success) => {
      if (success) {
        $q.notify({
          message: 'Требования успешно выставлены',
          color: 'green',
          position: 'top',
        });
        tab.value = 'common';
      }
    });
  } else {
    $q.notify({
      message: 'Пропишите требования к классам',
      color: 'red',
      position: 'top',
    });
  }
}
function deleteCls(cls) {
  console.log(cls);
  requirements.value.classes = requirements.value.classes.filter((item) => item.id !== cls.id);
  console.log(classesOptions.value.find((val) => val.label === cls.value.label).value);
  classesOptions.value.find((val) => val.label === cls.value.label).disable = false;
}
function disableCls(value) {
  console.log(value);
  const tempCls = classesOptions.value.find((val) => val.label === value.label);
  tempCls.disable = !tempCls.disable;
}
function addClass() {
  requirements.value.classes.push({
    id: getRandomId(),
    value: '',
    number: 1,
  });
}
const classesOptions = useState('classesTypes');

</script>
