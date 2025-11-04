<template>
  <button class="scroll-top-button" onclick="window.scrollTo({ top: 0, behavior: 'smooth' })">
    <span class="arrow-up">↑</span>
  </button>
</template>

<style scoped>
/* Scroll To Top Button */
.scroll-top-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background-color: #000;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 1000; /* make the scroll to top button draw on top of everything */
}

.arrow-up {
  font-size: 20px;
}
</style>