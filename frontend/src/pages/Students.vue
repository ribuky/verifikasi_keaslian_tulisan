<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div
      class="bg-white shadow-md p-4 flex justify-between items-center rounded-md"
    >
      <h1 class="text-xl font-semibold text-gray-700">Data Siswa</h1>
      <button
        @click="openAddModal"
        class="text-white font-bold px-4 py-2 rounded-md hover:bg-blue-600"
        id="main-color"
      >
        + Tambah Siswa
      </button>
    </div>

    <div class="bg-white shadow-md mt-4 p-4 rounded-md overflow-x-auto">
      <table class="w-full border-collapse">
        <thead>
          <tr class="text-black" id="t-color">
            <th class="p-2 border">No</th>
            <th class="p-2 border">Nama</th>
            <th class="p-2 border">Kelas</th>
            <th class="p-2 border">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(siswa, index) in siswaList"
            :key="siswa.student_id"
            class="text-center"
          >
            <td class="p-2 border">{{ index + 1 }}</td>
            <td class="p-2 border">{{ siswa.name }}</td>
            <td class="p-2 border">{{ siswa.class_name }}</td>
            <td class="p-2 border">
              <button
                @click="openEditModal(siswa)"
                class="bg-yellow-500 text-white px-3 py-1 rounded-md mr-2 hover:bg-yellow-600"
              >
                Edit
              </button>
              <button
                @click="confirmDelete(siswa.student_id)"
                class="bg-red-500 text-white px-3 py-1 mt-2 rounded-md hover:bg-red-600"
              >
                Hapus
              </button>
            </td>
          </tr>
          <tr v-if="siswaList.length === 0">
            <td colspan="4" class="p-4 text-center text-gray-500">
              Tidak ada data siswa
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="isAddModalOpen"
      class="fixed inset-0 bg-black/50 flex justify-center items-center"
    >
      <div class="bg-white p-6 rounded-md w-80">
        <h2 class="text-lg font-semibold mb-4">Tambah Siswa</h2>
        <input
          v-model="newSiswa.name"
          type="text"
          placeholder="Nama Siswa"
          class="w-full p-2 border rounded-md mb-5"
        />
        <input
          v-model="newSiswa.class_name"
          type="text"
          placeholder="Kelas Siswa"
          class="w-full p-2 border rounded-md mb-5"
        />
        <div class="flex justify-end space-x-2">
          <button
            @click="isAddModalOpen = false"
            class="px-4 py-2 border rounded-md"
          >
            Batal
          </button>
          <button
            @click="addSiswa"
            class="text-white font-bold px-4 py-2 rounded-md hover:bg-blue-600"
            id="main-color"
          >
            Tambah
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="isEditModalOpen"
      class="fixed inset-0 bg-black/50 flex justify-center items-center"
    >
      <div class="bg-white p-6 rounded-md w-80">
        <h2 class="text-lg font-semibold mb-4">Edit Siswa</h2>
        <input
          v-model="editSiswaData.name"
          type="text"
          placeholder="Nama Siswa"
          class="w-full p-2 border rounded-md mb-5"
        />
        <input
          v-model="editSiswaData.class_name"
          type="text"
          placeholder="Kelas Siswa"
          class="w-full p-2 border rounded-md mb-5"
        />
        <div class="flex justify-end space-x-2">
          <button
            @click="isEditModalOpen = false"
            class="px-4 py-2 border rounded-md"
          >
            Batal
          </button>
          <button
            @click="updateSiswa"
            class="text-white font-bold px-4 py-2 rounded-md hover:bg-blue-600"
            id="main-color"
          >
            Simpan
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="isConfirmDelete"
      class="fixed inset-0 bg-black/50 flex justify-center items-center"
    >
      <div class="bg-white p-6 rounded-md w-80 text-center">
        <p class="text-lg font-semibold">Hapus siswa ini?</p>
        <p class="mb-4 text-xs font-light text-red-600">Sample akan terhapus juga!</p>
        <div class="flex justify-center space-x-2">
          <button
            @click="isConfirmDelete = false"
            class="px-4 py-2 border rounded-md"
          >
            Batal
          </button>
          <button
            @click="deleteSiswa"
            class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
          >
            Hapus
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      siswaList: [],
      isAddModalOpen: false,
      isEditModalOpen: false,
      isConfirmDelete: false,
      newSiswa: { name: "", class_name: "" },
      editSiswaData: { student_id: null, name: "", class_name: "" },
      deleteId: null,
    };
  },
  mounted() {
    this.fetchSiswa();
  },
  methods: {
    async fetchSiswa() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://127.0.0.1:5000/api/students", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.siswaList = response.data.students;
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    openAddModal() {
      this.newSiswa = { name: "", class_name: "" };
      this.isAddModalOpen = true;
    },
    async addSiswa() {
      if (this.newSiswa.name && this.newSiswa.class_name) {
        try {
          const token = localStorage.getItem("access_token");
          await axios.post(
            "http://127.0.0.1:5000/api/students",
            this.newSiswa,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );
          this.fetchSiswa();
          this.isAddModalOpen = false;
        } catch (error) {
          console.error("Error adding student:", error);
        }
      }
    },
    openEditModal(siswa) {
      this.editSiswaData = { ...siswa };
      this.isEditModalOpen = true;
    },
    async updateSiswa() {
      try {
        const token = localStorage.getItem("access_token");
        await axios.put(
          `http://127.0.0.1:5000/api/students/${this.editSiswaData.student_id}`,
          this.editSiswaData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.fetchSiswa();
        this.isEditModalOpen = false;
      } catch (error) {
        console.error("Error updating student:", error);
      }
    },
    confirmDelete(id) {
      this.deleteId = id;
      this.isConfirmDelete = true;
    },
    async deleteSiswa() {
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(
          `http://127.0.0.1:5000/api/students/${this.deleteId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.fetchSiswa();
        this.isConfirmDelete = false;
        this.deleteId = null; // Reset deleteId setelah penghapusan berhasil
      } catch (error) {
        console.error("Error deleting student:", error);
        // Tambahkan penanganan kesalahan yang lebih spesifik jika diperlukan
        if (error.response) {
          // Server mengembalikan kode status selain 2xx
          console.error("Server response:", error.response.data);
          console.error("Server status:", error.response.status);
        } else if (error.request) {
          // Permintaan dibuat, tetapi tidak ada respons yang diterima
          console.error("Request error:", error.request);
        } else {
          // Terjadi kesalahan dalam menyiapkan permintaan
          console.error("Error message:", error.message);
        }
        alert("Gagal menghapus siswa. Silakan coba lagi."); // Beri tahu pengguna tentang kesalahan
      }
    },
  },
};
</script>
