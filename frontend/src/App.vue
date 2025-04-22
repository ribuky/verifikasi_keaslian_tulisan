<template>
  <div class="min-h-screen bg-gray-100">
    <Navbar v-if="showNavbar" />
    <router-view></router-view> <!-- Ini akan menampilkan halaman yang sesuai dengan routing -->
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import { useRoute } from 'vue-router';
import { computed } from 'vue';

export default {
  components: { Navbar },
  setup() {
    const route = useRoute();

    // Sembunyikan navbar di halaman login
    const showNavbar = computed(() => route.path !== "/login");
    return { showNavbar };
  },
  name: "App",
};
</script>

<style>
/* Bisa tambahkan styling global di sini jika perlu */
</style>
