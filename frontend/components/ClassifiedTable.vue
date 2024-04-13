<template>
  <div>
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
            <q-item-label caption class="tw-text-lg">{{ item.result }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-separator inset />
      </div>
      <q-item>
        <q-btn
          no-caps
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
const classes = useState('classes');
</script>
