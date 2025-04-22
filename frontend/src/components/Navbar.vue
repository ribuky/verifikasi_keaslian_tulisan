<template>
  <!-- Navbar -->
  <nav
    class="shadow-md p-4 flex justify-between items-center"
    style="background-color: #b87876"
  >
    <!-- Logo -->
    <div class="flex items-center">
      <img src="../assets/logo2.png" alt="Logo" class="w-10 h-10" />
      <span class="ml-2 text-lg text-white font-semibold"
        >Sistem Verifikasi</span
      >
    </div>

    <!-- Hamburger Menu (Mobile) -->
    <button @click="toggleMenu" class="lg:hidden text-white">☰</button>

    <!-- Menu -->
    <ul
      :class="menuOpen ? 'block' : 'hidden'"
      class="absolute lg:static top-16 left-0 w-full lg:w-auto bg-white shadow-lg lg:shadow-none lg:flex space-y-2 lg:space-y-0 lg:space-x-4 p-4 lg:p-0"
    >
      <li>
        <router-link
          to="/dashboard"
          active-class="bg-gray-200"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-md"
        >
          Dashboard
        </router-link>
      </li>
      <li>
        <router-link
          to="/data-siswa"
          active-class="bg-gray-200"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-md"
        >
          Data Siswa
        </router-link>
      </li>
      <li>
        <router-link
          to="/upload-tugas"
          active-class="bg-gray-200"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-md"
        >
          Upload Tugas
        </router-link>
      </li>
      <li>
        <router-link
          to="/upload-sample"
          active-class="bg-gray-200"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-md"
        >
          Upload Sample
        </router-link>
      </li>
      <li>
        <router-link
          to="/history"
          active-class="bg-gray-200"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-md"
        >
          History
        </router-link>
      </li>
      <li v-if="role === 'admin'">
        <router-link
          to="/manajemen-pengguna"
          active-class="bg-gray-200"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-md"
        >
          Manajemen Pengguna
        </router-link>
      </li>
      <li class="border-t lg:border-none mt-2 pt-2 lg:mt-0 lg:pt-0">
        <button
          @click="logout"
          class="block w-full text-left px-4 py-2 text-red-600 hover:bg-gray-200 rounded-md"
        >
          Logout
        </button>
      </li>
    </ul>
  </nav>
</template>

<script>
import { watch, ref, onMounted } from "vue"; // ⬅️ tambahkan onMounted
import { useRoute, useRouter } from "vue-router";

export default {
  setup() {
    const menuOpen = ref(false);
    const role = ref(null); // Role admin/guru

    const route = useRoute();
    const router = useRouter();

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value;
    };

    const closeMenu = () => {
      menuOpen.value = false;
    };

    const logout = () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("role"); // pastikan ini sesuai key yang dipakai
      closeMenu();
      router.push("/login");
    };

    // Ambil role saat komponen dimount
    onMounted(() => {
      role.value = localStorage.getItem("role"); // ⬅️ ini penting
    });

    // Tutup menu saat berpindah halaman
    watch(route, () => {
      closeMenu();
    });

    return { menuOpen, toggleMenu, closeMenu, logout, role };
  },
};
</script>
