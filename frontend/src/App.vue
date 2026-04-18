<template>
  <div class="app-shell">
    <header class="app-header">
      <div>
        <RouterLink class="brand" to="/">B4-VibeCoding</RouterLink>
        <p class="muted">Idea -> Clarification -> Docs -> Tasks</p>
      </div>
      <nav class="top-nav">
        <RouterLink to="/">项目列表</RouterLink>
        <RouterLink to="/projects/new">新建项目</RouterLink>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>
