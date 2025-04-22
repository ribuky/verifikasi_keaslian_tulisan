<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div
      class="bg-white shadow-md p-4 flex justify-between items-center rounded-md"
    >
      <h1 class="text-xl font-semibold text-gray-700">Upload Tugas Siswa</h1>
    </div>

    <!-- Form Upload -->
    <div class="bg-white shadow-md mt-4 p-6 rounded-md">
      <label class="block text-gray-700">Pilih Siswa:</label>
      <select
        v-model="selectedStudent"
        class="w-full p-2 border rounded-md mb-4"
      >
        <option
          v-for="siswa in siswaList"
          :key="siswa.student_id"
          :value="siswa.student_id"
        >
          {{ siswa.name }} - {{ siswa.class_name }}
        </option>
      </select>

      <label class="block text-gray-700">Pilih Gambar Tugas:</label>
      <input
        type="file"
        @change="handleFileUpload"
        accept="image/png, image/jpeg"
        class="w-full p-2 border rounded-md mb-4"
      />

      <button
        @click="uploadAssignment"
        class="w-full text-white font-bold py-2 rounded-md hover:bg-blue-600"
        id="main-color"
      >
        Upload Tugas
      </button>
    </div>

    <!-- Daftar Tugas -->
    <div class="bg-white shadow-md mt-4 p-6 rounded-md">
      <h2 class="text-lg font-semibold mb-2">Daftar Tugas</h2>
      <ul>
        <li
          v-for="assignment in assignmentList"
          :key="assignment.assignment_id"
          class="p-2 border-b flex space-x-4 items-start"
        >
          <div class="w-32 shrink-0">
            <img
            :src="'http://127.0.0.1:5000' + assignment.image_path"
            class="w-full h-auto rounded object-cover cursor-pointer"
            @click="
              selectedImage = 'http://127.0.0.1:5000' + assignment.image_path
            "
          />
          <div
            v-if="verificationDetails[assignment.assignment_id]"
            class="text-sm text-gray-600 mt-1 text-center"
          >
            Similarity Score:
            <span class="font-semibold">
              {{
                verificationDetails[assignment.assignment_id].similarity_score
              }}
            </span>
          </div>
          </div>

          <div>
            <!-- <p>{{ assignment.image_path }}</p> -->
            <p class="text-gray-700">Siswa: {{ assignment.student_name }}</p>
            <p class="text-gray-700">
              Status:
              <span :class="statusClass(assignment.status)">{{
                assignment.status
              }}</span>
            </p>

            <!-- Tombol "Verifikasi" hanya muncul jika status masih "PENDING" -->
            <button
              v-if="assignment.status === 'Pending'"
              @click="verifyAssignment(assignment)"
              class="bg-blue-500 text-white px-3 py-1 rounded-md hover:bg-blue-600"
            >
              Verifikasi
            </button>
            <!-- Hanya tampil kalau assignment sudah diverifikasi -->
            <button
              v-if="assignment.status !== 'Pending'"
              @click="showVerificationDetail(assignment)"
              class="bg-gray-300 text-gray-700 px-3 py-1 rounded-md hover:bg-gray-400 ml-2"
            >
              Lihat Detail
            </button>
            <button
              @click="deleteAssignment(assignment)"
              class="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 ml-2"
            >
              Hapus
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Modal Gambar -->
    <div
      v-if="selectedImage"
      class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50"
      @click.self="selectedImage = null"
    >
      <div class="bg-white p-4 rounded shadow-lg relative max-w-3xl">
        <button
          class="absolute top-2 right-2 text-gray-600 hover:text-black"
          @click="selectedImage = null"
        >
          ❌
        </button>
        <img :src="selectedImage" class="max-h-[80vh] mx-auto" />
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
      assignmentList: [],
      selectedStudent: "",
      file: null,
      selectedImage: null,
      verificationDetails: [],
    };
  },
  mounted() {
    this.fetchSiswa();
    this.fetchAssignments();
  },
  methods: {
    async fetchSiswa() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://127.0.0.1:5000/api/students", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.siswaList = response.data.students;
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    async fetchAssignments() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:5000/api/assignments",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.assignmentList = response.data.assignments;
      } catch (error) {
        console.error("Error fetching assignments:", error);
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async uploadAssignment() {
      if (!this.selectedStudent || !this.file) {
        alert("Pilih siswa dan gambar tugas terlebih dahulu!");
        return;
      }

      const formData = new FormData();
      formData.append("student_id", this.selectedStudent);
      formData.append("file", this.file);

      try {
        const token = localStorage.getItem("access_token");
        await axios.post(
          "http://127.0.0.1:5000/api/upload_assignment",
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.fetchAssignments(); // Refresh daftar tugas
        this.selectedStudent = "";
        this.file = null;
        alert("Tugas berhasil diunggah!");
      } catch (error) {
        console.error("Error uploading assignment:", error);
      }
    },
    async verifyAssignment(assignment) {
      try {
        // Fetch gambar dari URL sebelum dikirim ke backend
        const response = await fetch(
          "http://127.0.0.1:5000" + assignment.image_path
        );
        if (!response.ok) throw new Error("Gagal mengambil gambar tugas!");

        const blob = await response.blob();
        const file = new File([blob], "assignment.jpg", { type: blob.type });

        // Buat FormData untuk dikirim ke backend
        const formData = new FormData();
        formData.append("file", file);
        formData.append("student_id", assignment.student_id);
        formData.append("assignment_id", assignment.assignment_id);

        const token = localStorage.getItem("access_token");
        const verifyResponse = await axios.post(
          "http://127.0.0.1:5000/api/verify",
          formData,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Backend akan mengembalikan status verifikasi
        const newStatus =
          verifyResponse.data.status === "Cocok" ? "Cocok" : "Tidak_Cocok";

        // Update status di database
        await axios.put(
          `http://127.0.0.1:5000/api/assignments/${assignment.assignment_id}`,
          { status: newStatus },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.fetchAssignments(); // Refresh daftar tugas
        alert(
          `✅ Verifikasi selesai!\nStatus: ${newStatus}\nSkor Kemiripan: ${verifyResponse.data.similarity_score}`
        );
      } catch (error) {
        console.error("Error verifying assignment:", error);
        alert("Terjadi kesalahan saat verifikasi tugas!");
      }
    },
    async deleteAssignment(assignment) {
      if (!confirm("Yakin ingin menghapus tugas ini?")) return;

      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(
          `http://127.0.0.1:5000/api/assignments/${assignment.assignment_id}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        this.fetchAssignments(); // Refresh daftar
        alert("Tugas berhasil dihapus!");
      } catch (error) {
        console.error("Error deleting assignment:", error);
        alert("Gagal menghapus tugas!");
      }
    },
    async showVerificationDetail(assignment) {
      const token = localStorage.getItem("access_token");
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/assignments/${assignment.assignment_id}/verification_log`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const log = response.data;
        this.verificationDetails[assignment.assignment_id] = log;
      } catch (error) {
        console.error("Gagal mengambil log verifikasi:", error);
        alert("Log verifikasi tidak ditemukan.");
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
