<template>
    <div class="min-h-screen bg-gray-100 p-6">
      <!-- Header -->
      <div class="bg-white p-4 rounded-md shadow-md flex justify-between items-center">
        <h1 class="text-xl font-semibold text-gray-700">Manajemen Pengguna</h1>
        <button @click="openAddModal" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
          + Tambah Pengguna
        </button>
      </div>
  
      <!-- Daftar Pengguna -->
      <div class="bg-white mt-4 p-4 rounded-md shadow-md overflow-x-auto">
        <table class="w-full table-auto text-left border-collapse">
          <thead>
            <tr class="bg-gray-200 text-gray-700">
              <th class="p-2 border">#</th>
              <th class="p-2 border">Username</th>
              <th class="p-2 border">Role</th>
              <th class="p-2 border">Dibuat</th>
              <th class="p-2 border">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="user.user_id" class="text-sm text-center">
              <td class="p-2 border">{{ index + 1 }}</td>
              <td class="p-2 border">{{ user.username }}</td>
              <td class="p-2 border capitalize">{{ user.role }}</td>
              <td class="p-2 border">{{ user.created_at }}</td>
              <td class="p-2 border">
                <button @click="openEditModal(user)" class="bg-yellow-500 text-white px-3 py-1 rounded-md hover:bg-yellow-600 mr-2">
                  Edit
                </button>
                <button @click="confirmDelete(user.user_id)" class="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600">
                  Hapus
                </button>
              </td>
            </tr>
            <tr v-if="users.length === 0">
              <td colspan="5" class="p-4 text-center text-gray-500">Belum ada pengguna</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Modal Tambah/Edit -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex justify-center items-center">
        <div class="bg-white p-6 rounded-md w-80">
          <h2 class="text-lg font-semibold mb-4">{{ isEditing ? 'Edit Pengguna' : 'Tambah Pengguna' }}</h2>
          <input v-model="form.username" type="text" placeholder="Username" class="w-full p-2 border rounded-md mb-4" />
          <input v-model="form.password" type="password" placeholder="Password" class="w-full p-2 border rounded-md mb-4" />
          <select v-model="form.role" class="w-full p-2 border rounded-md mb-4">
            <option value="" disabled>Pilih Role</option>
            <option value="admin">Admin</option>
            <option value="guru">Guru</option>
          </select>
          <div class="flex justify-end space-x-2">
            <button @click="closeModal" class="px-4 py-2 border rounded-md">Batal</button>
            <button @click="submitForm" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
              {{ isEditing ? 'Update' : 'Tambah' }}
            </button>
          </div>
        </div>
      </div>
  
      <!-- Konfirmasi Hapus -->
      <div v-if="showConfirmDelete" class="fixed inset-0 bg-black/50 flex justify-center items-center">
        <div class="bg-white p-6 rounded-md w-80 text-center">
          <p class="text-lg font-semibold mb-4">Yakin ingin menghapus user ini?</p>
          <div class="flex justify-center space-x-2">
            <button @click="showConfirmDelete = false" class="px-4 py-2 border rounded-md">Batal</button>
            <button @click="deleteUser" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">Hapus</button>
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
        users: [],
        showModal: false,
        isEditing: false,
        form: {
          user_id: null,
          username: "",
          password: "",
          role: "",
        },
        showConfirmDelete: false,
        deleteUserId: null,
      };
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const token = localStorage.getItem("access_token");
          const response = await axios.get("http://127.0.0.1:5000/api/users", {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.users = response.data.users;
        } catch (error) {
          console.error("Gagal mengambil pengguna:", error);
        }
      },
      openAddModal() {
        this.isEditing = false;
        this.form = { user_id: null, username: "", password: "", role: "" };
        this.showModal = true;
      },
      openEditModal(user) {
        this.isEditing = true;
        this.form = { ...user, password: "" }; // kosongkan password
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      },
      async submitForm() {
        const token = localStorage.getItem("access_token");
  
        try {
          if (this.isEditing) {
            // Edit user (ubah username & password)
            await axios.put("http://127.0.0.1:5000/api/reset_user", {
              old_username: this.form.username, // gunakan username lama
              new_username: this.form.username,
              new_password: this.form.password,
            }, {
              headers: { Authorization: `Bearer ${token}` },
            });
          } else {
            // Tambah user
            await axios.post("http://127.0.0.1:5000/api/register", this.form, {
              headers: { Authorization: `Bearer ${token}` },
            });
          }
  
          this.closeModal();
          this.fetchUsers();
        } catch (error) {
          console.error("Gagal menyimpan user:", error);
        }
      },
      confirmDelete(userId) {
        this.deleteUserId = userId;
        this.showConfirmDelete = true;
      },
      async deleteUser() {
        const token = localStorage.getItem("access_token");
  
        try {
          await axios.delete(`http://127.0.0.1:5000/api/users/${this.deleteUserId}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
  
          this.fetchUsers();
          this.showConfirmDelete = false;
        } catch (error) {
          console.error("Gagal menghapus user:", error);
        }
      },
    },
  };
  </script>
  