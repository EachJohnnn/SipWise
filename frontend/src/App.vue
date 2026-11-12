<script setup>
import { onMounted, ref } from 'vue'
import { api } from './api/client'

const query = ref('Negroni')
const results = ref(null)
const selected = ref(null)
const busy = ref(false)
const error = ref('')
const connection = ref('正在检查 API…')

onMounted(async () => {
  try {
    const { data } = await api.get('/health')
    connection.value = data.catalog === 'fixture'
      ? 'FastAPI 与 SQLite 已连接 · 本地样例'
      : 'FastAPI 与 SQLite 已连接'
  } catch {
    connection.value = '无法连接 API，请启动 FastAPI 后刷新页面。'
  }
})

async function search() {
  if (!query.value.trim() || busy.value) return

  busy.value = true
  error.value = ''
  results.value = null
  selected.value = null
  try {
    const { data } = await api.get('/cocktails/search', {
      params: { name: query.value.trim() },
    })
    results.value = data
  } catch {
    error.value = '搜索失败。请检查 FastAPI 是否运行，再试一次。'
  } finally {
    busy.value = false
  }
}

async function openRecipe(id) {
  if (busy.value) return

  busy.value = true
  error.value = ''
  selected.value = null
  try {
    const { data } = await api.get(`/cocktails/${encodeURIComponent(id)}`)
    selected.value = data
  } catch {
    error.value = '无法加载配方。请重新搜索或稍后再试。'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <main>
    <header>
      <h1>SipWise</h1>
      <p role="status">{{ connection }}</p>
    </header>

    <form @submit.prevent="search">
      <label for="query">鸡尾酒名称</label>
      <div class="search-row">
        <input id="query" v-model="query" maxlength="100" required>
        <button type="submit" :disabled="busy || !query.trim()">搜索</button>
      </div>
    </form>

    <p v-if="busy" role="status">加载中…</p>
    <p v-if="error" role="alert">{{ error }}</p>
    <p v-if="results?.length === 0" role="status">没有匹配的配方。</p>
    <ul v-if="results?.length" class="results">
      <li v-for="recipe in results" :key="recipe.id">
        <button type="button" :disabled="busy" @click="openRecipe(recipe.id)">
          {{ recipe.name }}
        </button>
      </li>
    </ul>

    <article v-if="selected">
      <h2>{{ selected.name }}</h2>
      <img v-if="selected.image_url" :src="selected.image_url" :alt="selected.name">
      <p v-if="selected.glass">杯型 {{ selected.glass }}</p>
      <h3>配方</h3>
      <ul>
        <li v-for="(ingredient, index) in selected.ingredients" :key="index">
          {{ ingredient.name }} · {{ ingredient.measure ?? '用量未提供' }}
        </li>
      </ul>
      <p v-if="selected.instructions">{{ selected.instructions }}</p>
      <p><a :href="selected.recipe_source_url" target="_blank" rel="noopener noreferrer">TheCocktailDB 配方</a></p>
      <h3>背后的故事</h3>
      <template v-if="selected.story">
        <p>{{ selected.story.summary }}</p>
        <a :href="selected.story.source_url" target="_blank" rel="noopener noreferrer">
          {{ selected.story.source_title }}
        </a>
      </template>
      <p v-else>暂无经核实的背景故事。</p>
    </article>
  </main>
</template>

<style>
:root {
  font-family: Inter, system-ui, sans-serif;
  color: #1e2924;
  background: #f4f6f2;
  line-height: 1.55;
}
body { margin: 0; }
main { max-width: 44rem; margin: 3rem auto; padding: 0 1.25rem 2rem; }
h1 { margin-bottom: 0; font-size: 2.75rem; }
header p { margin-top: .25rem; color: #44534b; }
form { margin: 1.5rem 0 1rem; }
label { display: block; margin-bottom: .35rem; font-weight: 650; }
.search-row { display: flex; gap: .5rem; }
input, button { font: inherit; padding: .5rem .75rem; border: 1px solid #5e7567; border-radius: .35rem; }
input { flex: 1; min-width: 0; }
button { color: #fff; background: #214e38; cursor: pointer; }
button:disabled { opacity: .65; cursor: default; }
.results { display: flex; gap: .5rem; padding: 0; list-style: none; }
article { margin-top: 1.25rem; padding: 1rem 1.25rem; background: #fff; border: 1px solid #d2dbd2; border-radius: .5rem; }
article img { max-width: 100%; height: auto; }
a { color: #214e38; }
</style>
