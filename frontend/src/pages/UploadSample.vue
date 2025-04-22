<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div
      class="bg-white shadow-md p-4 flex justify-between items-center rounded-md"
    >
      <h1 class="text-xl font-semibold text-gray-700">Upload Sample Tulisan</h1>
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

      <label class="block text-gray-700">Deskripsi (Opsional):</label>
      <textarea
        v-model="description"
        class="w-full p-2 border rounded-md mb-4"
      ></textarea>

      <label class="block text-gray-700">Pilih Gambar:</label>
      <input
        type="file"
        multiple
        @change="handleFileUpload"
        accept="image/png, image/jpeg"
        class="w-full p-2 border rounded-md mb-4"
      />

      <button
        @click="uploadSample"
        class="w-full text-white font-bold py-2 rounded-md hover:bg-blue-600"
        id="main-color"
      >
        Upload Sample
      </button>
    </div>

    <!-- Daftar Sample -->
    <div class="bg-white shadow-md mt-4 p-6 rounded-md">
      <h2 class="text-lg font-semibold mb-2">Daftar Sample Tulisan</h2>
      <ul>
        <li
          v-for="(samples, studentId) in groupedSamples"
          :key="studentId"
          class="border-b p-2"
        >
          <button
            @click="toggleDropdown(studentId)"
            class="w-full text-left font-semibold text-gray-800 p-2 bg-gray-200 rounded-md"
          >
            {{ getStudentName(studentId) }} ({{ samples.length }} Samples)
          </button>
          <ul v-if="openDropdown === studentId" class="mt-2">
            <li
              v-for="sample in samples"
              :key="sample.sample_id"
              class="flex items-center space-x-2 p-2"
            >
              <img
                :src="'http://127.0.0.1:5000/' + sample.image_path"
                class="w-16 h-16 object-cover rounded-md"
                @click="
                  selectedImage = 'http://127.0.0.1:5000/' + sample.image_path
                "
              />
              <p class="text-gray-700">
                {{ sample.description || "Tidak ada deskripsi" }}
              </p>
              <button @click="editSample(sample)" class="text-blue-500">
                Edit
              </button>
              |
              <button
                @click="deleteSample(sample.sample_id)"
                class="text-red-500"
              >
                Hapus
              </button>
            </li>
          </ul>
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
      siswaList: [], // Daftar siswa
      sampleList: [], // Daftar handwriting samples
      selectedStudent: "",
      description: "",
      file: [],
      openDropdown: null, // Untuk menyimpan dropdown yang terbuka
      selectedImage: null,
    };
  },
  mounted() {
    this.fetchSiswa(); // Ambil daftar siswa saat halaman dimuat
    this.fetchSamples(); // Ambil daftar sample yang sudah ada
  },
  computed: {
    groupedSamples() {
      const grouped = {};
      this.sampleList.forEach((sample) => {
        if (!grouped[sample.student_id]) {
          grouped[sample.student_id] = [];
        }
        grouped[sample.student_id].push(sample);
      });
      return grouped;
    },
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
    async fetchSamples() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:5000/api/handwriting_samples",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.sampleList = response.data.samples;
      } catch (error) {
        console.error("Error fetching samples:", error);
      }
    },
    handleFileUpload(event) {
      this.files = Array.from(event.target.files);
    },
    async uploadSample() {
      if (!this.selectedStudent || this.files.length === 0) {
        alert("Pilih siswa dan gambar terlebih dahulu!");
        return;
      }

      const formData = new FormData();
      formData.append("student_id", this.selectedStudent);
      formData.append("description", this.description);

      // Tambahkan semua file ke FormData
      this.files.forEach((file, index) => {
        formData.append("files", file); // key "files" untuk multiple file
      });

      try {
        const token = localStorage.getItem("access_token");
        await axios.post("http://127.0.0.1:5000/api/upload_sample", formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        });

        this.fetchSamples(); // Refresh daftar sample
        this.selectedStudent = "";
        this.description = "";
        this.files = [];
        alert("Sample berhasil diunggah!");
      } catch (error) {
        console.error("Error uploading sample:", error);
      }
    },

    async editSample(sample) {
      this.selectedStudent = sample.student_id;
      this.description = sample.description;
    },
    async deleteSample(sampleId) {
      const token = localStorage.getItem("access_token");
      await axios.delete(
        `http://127.0.0.1:5000/api/handwriting_samples/${sampleId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      this.fetchSamples();
    },
    toggleDropdown(studentId) {
      this.openDropdown = this.openDropdown === studentId ? null : studentId;
    },
    getStudentName(studentId) {
      const student = this.siswaList.find(
        (s) => s.student_id === parseInt(studentId)
      );
      return student ? student.name : "Unknown";
    },
  },
};
</script>
