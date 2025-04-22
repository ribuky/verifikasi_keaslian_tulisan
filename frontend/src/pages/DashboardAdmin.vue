<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Konten Dashboard -->
    <main
      class="flex flex-col overflow-hidden items-center justify-center h-[80vh] text-center px-4"
    >
      <h1 class="text-2xl font-semibold text-gray-700">
        Selamat Datang di Dashboard
      </h1>

      <!-- Teks tambahan -->
      <p class=" text-sm mt-2 text-gray-500 mb-4">
        Aplikasi ini membantu guru memverifikasi keaslian tulisan tangan siswa
        menggunakan teknologi Machine Learning dan mempermudah pengelolaan data
        siswa serta tugas.
      </p>

      <!-- Tombol upload tugas -->
      <button
        @click="goToUploadTugas"
        class="text-white font-bold px-6 py-2 rounded-lg hover:bg-blue-600 transition"
        id="main-color"
      >
        Upload Tugas
      </button>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    logout() {
      // Hapus token atau sesi
      localStorage.removeItem("access_token");
      this.$router.push("/login"); // Redirect ke login
    },
    goToUploadTugas() {
      this.$router.push("/upload-tugas");
    },
  },
};
</script>

<style>
/* Tambahkan animasi saat membuka/menutup menu */
@media (max-width: 1024px) {
  ul {
    transition: all 0.3s ease-in-out;
  }
}
</style>
