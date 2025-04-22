<template>
  <div
    class="flex flex-col items-center justify-start h-screen overflow-hidden bg-gray-100 relative pt-[200px] sm:pt-[230px] md:pt-[260px] lg:pt-[270px]"
  >
    <!-- Shape -->
    <div class="shape absolute top-0 left-0 w-full">
      <svg
        data-name="Layer 1"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 1200 120"
        preserveAspectRatio="none"
      >
        <path
          d="M0,0V7.23C0,65.52,268.63,112.77,600,112.77S1200,65.52,1200,7.23V0Z"
          class="shape-fill"
        ></path>
      </svg>
    </div>

    <!-- Logo -->
    <img src="../assets/logo2.png" alt="Logo" class="logo-shape" />

    <!-- Form Wrapper -->
    <div class="p-6 w-full max-w-[90%] sm:max-w-sm md:max-w-md lg:max-w-lg bg-white rounded-lg shadow-lg">
      <h1 class="font-bold text-center text-lg text-gray-700 mb-2">
        Selamat Datang Kembali
      </h1>
      <h1 class="font-normal text-center text-gray-700 mb-4">
        Masuk ke akun Anda
      </h1>
      <form @submit.prevent="login">
        <div class="mb-2">
          <label class="block text-gray-700">Username</label>
          <input
            type="text"
            v-model="username"
            placeholder="Username"
            class="w-full p-2 border rounded-md mb-2"
            required
          />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            placeholder="Password"
            class="w-full p-2 border rounded-md mb-2"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full button-login text-white p-2 rounded-md font-bold mt-6"
        >
          Login
        </button>
      </form>
      <p v-if="errorMessage" class="text-red-500 text-center mt-2">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        localStorage.setItem("role", response.data.role);
        this.$router.push("/dashboard");
      } catch (error) {
        this.errorMessage = "Login gagal! Periksa username dan password.";
      }
    },
  },
};
</script>
