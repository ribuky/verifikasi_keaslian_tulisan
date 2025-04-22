<template>
    <div class="min-h-screen bg-gray-100 p-6">
      <div class="bg-white p-4 shadow rounded-md flex justify-between items-center mb-4">
        <h1 class="text-xl font-semibold text-gray-700">Histori Verifikasi Tugas</h1>
      </div>
  
      <!-- Filter Tanggal -->
      <div class="bg-white p-4 rounded-md shadow mb-4">
        <div class="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-4">
          <div>
            <label class="text-gray-600">Tanggal Awal:</label>
            <input type="date" v-model="startDate" class="border p-2 rounded-md" />
          </div>
          <div>
            <label class="text-gray-600">Tanggal Akhir:</label>
            <input type="date" v-model="endDate" class="border p-2 rounded-md" />
          </div>
          <button @click="fetchHistory" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
            Filter
          </button>
        </div>
      </div>
  
      <!-- Tabel Histori -->
      <div class="bg-white p-4 rounded-md shadow">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-200 text-gray-700">
              <th class="p-2 border">#</th>
              <th class="p-2 border">Nama Siswa</th>
              <th class="p-2 border">Similarity Score</th>
              <th class="p-2 border">Status</th>
              <th class="p-2 border">Tanggal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(log, index) in historyList" :key="log.log_id" class="text-sm">
              <td class="p-2 border">{{ index + 1 }}</td>
              <td class="p-2 border">{{ log.student_id }}</td>
              <td class="p-2 border">{{ log.similarity_score }}</td>
              <td class="p-2 border">
                <span :class="statusClass(log.status)">
                  {{ log.status }}
                </span>
              </td>
              <td class="p-2 border">{{ log.created_at }}</td>
            </tr>
            <tr v-if="historyList.length === 0">
              <td colspan="5" class="p-4 text-center text-gray-500">Tidak ada histori ditemukan</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        historyList: [],
        startDate: "",
        endDate: "",
      };
    },
    mounted() {
      this.fetchHistory();
    },
    methods: {
      async fetchHistory() {
        try {
          const token = localStorage.getItem("access_token");
  
          const params = {};
          if (this.startDate) params.start_date = this.startDate;
          if (this.endDate) params.end_date = this.endDate;
  
          const response = await axios.get("http://127.0.0.1:5000/api/verification_logs", {
            headers: { Authorization: `Bearer ${token}` },
            params,
          });
  
          this.historyList = response.data.logs;
        } catch (error) {
          console.error("Gagal mengambil histori:", error);
        }
      },
      statusClass(status) {
        return {
          "text-yellow-500": status === "Pending",
          "text-green-500": status === "Cocok",
          "text-red-500": status === "Tidak Cocok",
        };
      },
    },
  };
  </script>
  